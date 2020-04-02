from __future__ import absolute_import, division, print_function, unicode_literals
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

tf.enable_eager_execution()

URL = "https://storage.googleapis.com/applied-dl/heart.csv"
dataframe = pd.read_csv(URL)
dataframe.head()

train, test = train_test_split(dataframe, test_size=0.2)
train, val = train_test_split(train, test_size=0.2)
print("train len: " , len(train))
print("test len: " , len(test))
print("val len: " , len(val))


def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop('target')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds

batch_size = 5
train_ds = df_to_dataset(train, batch_size=batch_size)
val_ds = df_to_dataset(val, shuffle=False, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

# for feature_batch, lable_batch in train_ds.take(1):
#     print(list(feature_batch.keys()))
#     print(feature_batch['age'])
#     print(lable_batch)

example_batch = next(iter(train_ds))[0]


def demo(feature_column):
   feature_layer = tf.keras.layers.DenseFeatures(feature_column)
   print(feature_layer(example_batch).numpy())


age = tf.feature_column.numeric_column("age")
demo(age)

# price = tf.feature_column.numeric_column('price')
# buketized_price = tf.feature_column.bucketized_column(price, boundaries=[0, 10, 100])
# columns = [buketized_price, ]
# features = tf.io.parse_example( .., features=tf.feature_column.make_parse_example_spec(columns))
# dense_tensor = tf.keras.layers.DenseFeatures(columns)(features)

age_bucket = tf.feature_column.bucketized_column(age, boundaries=[18, 25, 30, 35, 40, 45, 50, 55, 60, 65])
demo(age_bucket)

thal = tf.feature_column.categorical_column_with_vocabulary_list(
    "thal", ["fixed", "normal", "reversible"])
thal_one_hot = tf.feature_column.indicator_column(thal)
demo(thal_one_hot)

that_embedding = tf.feature_column.embedding_column(thal, dimension=8)
demo(that_embedding)

print("Tested OK!")