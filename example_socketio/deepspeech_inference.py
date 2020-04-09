import argparse
import sys
import os
from flask import Flask, Response, stream_with_context, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app=app, resources={r"/APIUsage": {"origins": "*"}})

ALLOWED_EXTENSIONS = ['wav']


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getExtension(filename):
    return filename.rsplit('.', 1)[1]


@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        yield request.args['name']
        yield '!'
    return Response(stream_with_context(generate()))

# @app.route('/stream_data')
# def stream_data():
#     def generate():
#         for i in range(10000):
#             yield str(i) + '\n'
#     return Response(stream_with_context(generate()))


@app.route('/deepinfer', methods=['POST', 'GET'])
def deepinfer():
    submitted_file = request.files['audio']
    if submitted_file and allowed_filename(submitted_file.filename):
        submitted_file.save(os.path.join('/home/ubuntu/audioreceived',submitted_file.filename))
        res = runCommand(submitted_file.filename)
        return res
    return 'try again with wav file'


# @app.route('/deepspeech', defaults={'audiopath' : '/data/delvifywork/DeepSpeech/data/smoke_test/LDC93S1_pcms16le_1_16000.wav'})
# @app.route('/deepspeech/<audiopath>')
def runCommand(audiopath):
    model = '/data/delvifywork/DeepSpeech/deepspeech-0.6.1-models/output_graph.pbmm'
    lm = '/data/delvifywork/DeepSpeech/deepspeech-0.6.1-models/lm.binary'
    trie = '/data/delvifywork/DeepSpeech/deepspeech-0.6.1-models/trie'
    audio = os.path.join('/home/ubuntu/audioreceived',audiopath)
    cmd = 'deepspeech --model ' + model + ' --lm ' + lm + ' --trie ' + trie + ' --audio ' + audio
    stream = os.popen(cmd)
    output = stream.read()
    return output


@app.route('/parameters', defaults={'audio': 'LDC93S1_pcms16le_1_16000.wav'})
@app.route('/parameters/<audio>/')
def parameter(audio):
    return "path to audio is: " + audio

@app.route('/')
def index():
    return "Inferernce on Deepspeech"


if __name__ == "__main__":
    # parser = argparse.ArgumentParser("input to deepspeech")
    # parser.add_argument('--model', default='/data/delvifywork/DeepSpeech/deepspeech-0.6.1-models/output_graph.pbmm', type=str)
    # parser.add_argument('--lm', default="/data/delvifywork/DeepSpeech/deepspeech-0.6.1-models/lm.binary", type=str)
    # parser.add_argument('--trie', default='/data/delvifywork/DeepSpeech/deepspeech-0.6.1-models/trie', type=str)
    # parser.add_argument('--audio', default='/data/delvifywork/DeepSpeech/data/smoke_test/LDC93S1_pcms16le_1_16000.wav', type=str)
    # args = parser.parse_args()
    # runCommand(args)
    app.run(debug=True, host='0.0.0.0', port=3005)