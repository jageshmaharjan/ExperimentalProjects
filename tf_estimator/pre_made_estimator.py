import tensorflow as tf
import numpy as np

# Enable and disable to see the effect
tf.enable_eager_execution()

dataset = tf.data.Dataset.from_tensor_slices([3,4,5,6,7,8])

it = iter(dataset)
# for i in enumerate(dataset):
print(next(it).numpy())

dataset1 = tf.data.Dataset.from_tensor_slices(tf.random.uniform([4,10]))
# it = iter(dataset1)
# print(next(it).numpy())
for z in dataset1:
    print(z.numpy())

dataset2 = tf.data.Dataset.from_tensor_slices((tf.random.uniform([4]), tf.random.uniform([4,10], maxval=100, dtype=tf.int32)))
# it = iter(dataset2)
# print(next(it).numpy())
for z in dataset2:
    for x in z:
        print(x.numpy())


dataset3 = tf.data.Dataset.zip((dataset1, dataset2))
it = iter(dataset3)
print(next(it))
for a, (b, c) in dataset3:
    print('shape of a is {a.shape}, b is {b.shape}, c is {c.shape}'.format(a=a, b=b, c=c))


train, test = tf.keras.datasets.fashion_mnist.load_data()
images, labels = train
images = images/255
dataset = tf.data.Dataset.from_tensor_slices((images, labels))


directory_url = "https://storage.googleapis.com/download.tensorflow.org/data/illiad/"
file_names = ['cowper.txt', 'derby.txt', 'butler.txt']
file_paths = [tf.keras.utils.get_file(file_name, directory_url+file_name) for file_name in file_names]

text_dataset = tf.data.TextLineDataset(file_paths)
for line in text_dataset.take(5):
    print(line.numpy())
print("Testing")

# def input_fn(dataset):
#
#     return feature_dict, labels