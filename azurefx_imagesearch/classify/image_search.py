import os
import json
import tensorflow as tf
import numpy as np
from scipy import spatial
import random, json, glob, os, codecs, random
from annoy import AnnoyIndex

def create_graph(model_path):
    with tf.gfile.FastGFile(os.path.join(model_path, 'classify_image_graph_def.pb'), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def find_similar_image(image, model_path, vector_path):
    create_graph(model_path)
    with tf.Session() as sess:
        # softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        with tf.gfile.FastGFile(image, "rb") as f:
            image_data = f.read()
            # predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0' : image_data})
            # predictions = np.squeeze(predictions)
            feature_tensor = sess.graph.get_tensor_by_name('pool_3:0')
            feature_set = sess.run(feature_tensor, {'DecodeJpeg/contents:0':image_data})
            feature_vector = np.squeeze(feature_set)
            print(feature_vector)

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

            named_nearest_neighbour = {}
            for i in file_index_to_file_name.keys():
                master_file = file_index_to_file_name[i]
                master_vector = file_index_to_file_vector[i]
                similarity = 1 - spatial.distance.cosine(master_vector, feature_vector)
                rounded_similarity = int((similarity * 10000)) / 10000.0
                named_nearest_neighbour[master_file] = rounded_similarity
                # print(named_nearest_neighbour)
            return named_nearest_neighbour


def image_search(imagepath = '/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/SKU878296.jpg',
                           trained_model='/tmp/pretrainmodel/',
                           vector_directory='/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/'):
    # result = find_similar_image('/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/SKU878296.jpg',
    #                             '/tmp/pretrainmodel/',
    #                             '/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/')
    result = find_similar_image(imagepath, trained_model, vector_directory)
    result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    result = [str(l[0]) + '.jpg' for l in result]
    return result


'''
imagepath = '/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/SKU878296.jpg',
                           trained_model='/tmp/pretrainmodel/',
                           vector_directory='/home/jugs/PycharmProjects/ExperimentalProjects/imageSearch/imgvec/'
'''