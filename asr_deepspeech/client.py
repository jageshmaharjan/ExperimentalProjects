
from __future__ import absolute_import, division, print_function

import argparse
import numpy as np
import shlex
import subprocess
import sys
import wave
import json

from passlib.utils import timer

try:
    from shhlex import quote
except:
    from pipes import quote

def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --enconding signed_int --ending little --compression 0.0 --no-dither -'\
        .format(quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('Sox returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno, 'sox not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)

def metadata_to_string(metadata):
    return ''.join(item.character for item in metadata.items)

def words_from_metadata(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    for i in range(0, metadata.num_items):
        item = metadata.items[i]
        if item.character != " ":
            word = word + item.character
        if item.character == " " or i == metadata.num_items -1:
            word_duration = item.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time "] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            word = ""
            word_start_time = 0
        else:
            if len(word) == 1:
                word_start_time = item.start_time

    return word_list


def metadata_json_output(metadata):
    json_result = dict()
    json_result["words"] = words_from_metadata(metadata)
    json_result["confidence"] = metadata.confidence
    return json.dumps(json_result)


class VersionAction(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(VersionAction, self).__init__(nargs=0, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        printVersions()
        exit(0)

def main():
    parser = argparse.ArgumentParser(description='Running DeepSpeecg inference')
    parser.add_argument('--model', required=True)
    parser.add_argument('--lm', required=True)
    parser.add_argument('--trie', required=True)
    parser.add_argument('--audio', required=True)
    parser.add_argument('--beam_width', type=int, default=500)
    parser.add_argument('--lm_alpha', default=0.75)
    parser.add_argument('--lm_beta', default=1.85)
    parser.add_argument('--version', action=VersionAction)
    parser.add_argument('--extended', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    print('loading model from files {}'.format(args.model), file=sys.stderr)
    model_load_start = timer()
    ds = Model(args.model, args.beam_width)
    model_load_end = timer() - model_load_start
    print('Loaded model in {:.3}s'.format(model_load_end), file=sys.stderr)

    desired_sample_rate = ds.sampleRate()

    if args.lm and args.trie:
        print('Loading language model from files {} {}'.format(args.lm, args.trie), file=sys.stderr)
        lm_load_start = timer()
        ds.enableDecoderWithLM(args.lm, args.trie, args.lm_alpha, args.lm_beta)
        lm_load_end = timer() - lm_load_start

