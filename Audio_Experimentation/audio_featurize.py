# import tensorflow as tf
import numpy as np
import soundfile
from numpy.lib.stride_tricks import as_strided
from scipy import signal


def spectrogram(samples, fft_length=256, sample_rate=2, hop_length=128):
    # assert not np.iscomplex(samples), "Complex numbers are not supportes"
    window = np.hanning(fft_length)[:, None]
    window_norm = np.sum(window**2)
    scale = window_norm * sample_rate
    trunc = (len(samples) - fft_length) % hop_length
    x = samples[:len(samples) - trunc]
    nshape = (fft_length, (len(x)- fft_length) // hop_length + 1)
    nstrides = (x.strides[0], x.strides[0] * hop_length)
    x = as_strided(x, shape=nshape, strides=nstrides)
    # assert np.all(x[:, 1] == samples[hop_length + fft_length])
    x = np.fft.rfft(x * window, axis=0)
    x = np.absolute(x) ** 2
    x[1:-1, :] *= (2.0 /scale)
    x[(0,-1), :] /= scale
    freqs = float(sample_rate) / fft_length * np.arange(x.shape[0])
    return x, freqs


def spectrogram_from_file(filename, step=10, window=20, max_freq=None, eps=1e014):
    with soundfile.SoundFile(filename) as sf:
        audio = sf.read(dtype='float32')
        sample_rate = sf.samplerate
        if audio.ndim >= 2:
            audio = np.mean(audio, 1)
        if max_freq is None:
            max_freq = sample_rate /2
        if max_freq > sample_rate /2:
            raise ValueError("max freq cannnot be > than 0.5 of sample rate")
        if step > window:
            raise ValueError("step size cannot be > the windows size")
        hop_length = int(0.001 * step * sample_rate)
        fft_length = int(0.001 * window * sample_rate)
        pxx, freqs = spectrogram(audio, fft_length=fft_length,
                                 sample_rate=sample_rate, hop_length=hop_length)
        ind = np.where(freqs <= max_freq[0][-1]  + 1)
        return np.transpose(np.log(pxx[:ind, :] + eps))

# spectrogram_from_file(filename='/home/jugs/Desktop/p257_431.wav')


def log_spectrogram_feature(samples, sample_rate, window_size=20, step_size=10, eps=1e-14):
    nperseg = int(round(window_size * sample_rate / 1e3))
    noverlap = int(round(step_size * sample_rate / 1e3))
    freqs, times, spec = signal.spectrogram(samples,
                                            fs=sample_rate, window='hann',
                                            nperseg=nperseg, noverlap=noverlap,
                                            detrend=False)
    freqs = (freqs*2)
    return freqs, times, np.log(spec.T.astype(np.float64) + eps)

