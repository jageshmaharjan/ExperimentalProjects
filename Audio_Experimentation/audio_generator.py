import numpy as np
import tensorflow as tf
import soundfile
import random

np.random.seed(95)
RNG_SEED = 95


class AudioGenerator():
    def __init__(self, step=10, window=20, max_freq=8000, mfcc_dim=13,
                 minibatch_size=20, desc_file=None, spectrogram=True,
                 max_duration=10.0):
        self.feat_dim = calc_feat_dim(window, max_freq)
        self.mfcc_dim = mfcc_dim
        self.feats_mean = np.zeros((self.feat_dim, ))
        self.feats_std = np.ones((self.feat_dim))
        self.rng = random.Random(RNG_SEED)
        if desc_file is not None:
            self.load_metadata_from_desc_file(desc_file)
        self.step = step
        self.window = window
        self.max_freq = max_freq
        self.cur_train_index = 0
        self.cur_valid_index = 0
        self.cur_test_index = 0
        self.max_duration = max_duration
        self.minibatch_size = minibatch_size
        self.spectrogram = spectrogram
        self.sort_by_duration = sort_by_duration

    def get_batch(self, partition):
        if partition == "train":
            audio_paths = self.train_audio_paths
            cur_index = self.cur_train_index
            texts = self.train_texts
        elif partition == 'valid':
            audio_paths = self.valid_audio_paths
            cur_index = self.cur_valid_index
            texts = self.valid_texts
        elif partition == 'test':
            audio_paths = self.test_audio_paths
            cur_index = self.cur_test_index
            texts = self.test_texts
        else:
            raise Exception("Invalid partition. Musr be train/test/valid")

        features = [self.normalize(self.featurize(a)) for a in
                    audio_paths[cur_index:cur_index+self.minibatch_size]]
        max_length = max([features[i].shape[0] for i in range(0, self.minibatch_size)])
        max_string_length = max([len(texts[cur_index+i])
                                 for i in range(0, self.minibatch_size)])

        X_data = np.zeros([self.minibatch_size, max_length,
                           self.feat_dim*self.spectrogram + self.mfcc_dim*(not self.spectrogram)])
        labels = np.ones([self.minibatch_size, max_string_length]) * 28
        input_length = np.zeros([self.minibatch_size, 1])
        label_length = np.zeros([self.minibatch_size, 1])

        for i in range(0, self.minibatch_size):
            feat = features[i]
            input_length[i] = feat.shape[0]
            X_data[i, :feat.shape[0], :] = feat

            label = np.array(text_to_int_seq(texts[cur_index+i]))
            labels[i, :len(labels)] = label
            label_length[i] = len(label)

        outputs = {'ctc' : np.zeros([self.minibatch_size])}
        inputs = {'the_input': X_data,
                  'the_labels': labels,
                  'input_length': input_length,
                  'label_length': label_length}
        return  (inputs, outputs)


