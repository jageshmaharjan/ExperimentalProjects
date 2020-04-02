'''
  Inception Pretrained_model
  http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
'''

import os
import json
import tensorflow as tf
import numpy as np
from gevent.pywsgi import WSGIServer
from scipy import spatial
import random, json, glob, os, codecs, random
from annoy import AnnoyIndex

import glob
from flask import Flask, request, render_template
from flask.json import jsonify
from werkzeug.utils import secure_filename
from gevent import pywsgi
from waitress import serve

app = Flask(__name__)

uploaded_filepath = str(os.getcwd()) + '/uploads/'  #'/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/uploads/'
vector_path =  str(os.getcwd()) + '/imgvec/'  #'/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/'
file_index_to_file_name = {}
file_index_to_file_vector = {}
t = AnnoyIndex(2048, 'angular')
infiles = glob.glob(vector_path + '/*.npz')
for file_index, i in enumerate(infiles):
    file_vector = np.loadtxt(i)
    file_name = os.path.basename(i).split('.')[0]
    file_index_to_file_name[file_index] = file_name
    file_index_to_file_vector[file_index] = file_vector
    t.add_item(file_index, file_vector)
t.build(20000)


def create_graph(model_path):
    with tf.io.gfile.GFile(os.path.join(model_path, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.compat.v1.GraphDef() #tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def find_similar_image(image): # image, model_path, vector_path
    # image = request.args.get('img')
    # image = '/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/SKU878296.jpg'
    model_path = '/tmp/pretrainmodel/'
    create_graph(model_path)
    with tf.compat.v1.Session() as sess:  # tf.Session() as sess:
        # softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        with tf.io.gfile.GFile(os.path.join(uploaded_filepath, image), "rb") as f:
            image_data = f.read()
            # predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0' : image_data})
            # predictions = np.squeeze(predictions)
            feature_tensor = sess.graph.get_tensor_by_name('pool_3:0')
            feature_set = sess.run(feature_tensor, {'DecodeJpeg/contents:0':image_data})
            feature_vector = np.squeeze(feature_set)

            named_nearest_neighbour = {}
            for i in file_index_to_file_name.keys():
                master_file = file_index_to_file_name[i]
                master_vector = file_index_to_file_vector[i]
                similarity = 1 - spatial.distance.cosine(master_vector, feature_vector)
                rounded_similarity = int((similarity * 10000)) / 10000.0
                named_nearest_neighbour[master_file] = rounded_similarity
                # print(named_nearest_neighbour)
    return named_nearest_neighbour


def getExtension(filename):
    return filename.rsplit('.', 1)[1]


@app.route('/get_imageskus/', methods=['GET', 'POST'])
def get_imageskus():
    image = request.files['file']
    ext = getExtension(image.filename)
    if ext in ['jpg', 'jepg', 'png']:
        filename = secure_filename(image.filename)
        image.save(os.path.join(uploaded_filepath, filename))
        result = find_similar_image(filename)
        result = sorted(result.items(), key=lambda item: item[1], reverse=True)
        result = [str(l[0]) + '.jpg' for l in result]
        return jsonify({"skus": result})


if __name__ == "__main__":
    # app.run("0.0.0.0")
    serve(app, host='0.0.0.0', port=5000)