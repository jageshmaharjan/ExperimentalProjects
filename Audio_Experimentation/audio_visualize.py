import numpy as np
import matplotlib.pyplot as plt


def plot_raw_audio(sample_rate, samples):
    time = np.arange(0, float(samples.shape[0]), 1) / sample_rate
    fig = plt.figure(figsize=(12,5))
    ax = fig.add_subplot(111)
    ax.plot(time, samples, linewidth=1, alpha=0.7, color='#76b900')
    plt.title('Raw Audio Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.show()

# plot_raw_audio(sample_rate, samples)