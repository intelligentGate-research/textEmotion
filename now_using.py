# -*- coding: utf-8 -*-
"""now using.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KHvHA8LQwnQWdMuirRL6CCOGo2Jj36mw
"""


def train():
    import tensorflow as tf
    import string
    import re
    import numpy as np

    def split_line(text):
        # Generate list of lines from text data
        return text.split('\n')

    def split_class(text):
        # split data and class from line list
        return [c.split(';')[0] for c in text], [c.split(';')[-1] for c in text]

    def strip_html(text):
        return re.sub('<[^<]+?>', '', text)

    def convert_to_batch(data, class_label, batch_size, buffer_size):
        # Create batch with prefetch feature
        return tf.data.Dataset.from_tensor_slices((data, class_label)).batch(batch_size, drop_remainder=True).shuffle(
            buffer_size).prefetch(tf.data.AUTOTUNE)

    def preprocess_dataset(path):
        text = open(path, 'r').read()
        data = strip_html(text)
        data = split_line(data)
        return split_class(data)

    train_text, train_class_text = preprocess_dataset('train.txt')
    validation_text, validation_class_text = preprocess_dataset('val.txt')

    VOCAB_SIZE = 4000

    encoder_data = tf.keras.layers.experimental.preprocessing.TextVectorization(max_tokens=VOCAB_SIZE,
                                                                                output_mode='int')
    encoder_data.adapt(train_text)

    encoder_class = tf.keras.layers.experimental.preprocessing.TextVectorization(output_mode='int')
    encoder_class.adapt(train_class_text)

    train_data_index = encoder_data(train_text)
    train_class_index = encoder_class(train_class_text)
    validation_data_index = encoder_data(validation_text)
    validation_class_index = encoder_class(validation_class_text)

    BATCH_SIZE = 64
    BUFFER_SIZE = 10000

    train_data_batch = convert_to_batch(train_data_index, train_class_index, BATCH_SIZE, BUFFER_SIZE)
    validation_data_batch = convert_to_batch(validation_data_index, validation_class_index, BATCH_SIZE, BUFFER_SIZE)

    encoder_data

    len(encoder_data.get_vocabulary())

    len(encoder_class.get_vocabulary())

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=len(encoder_data.get_vocabulary()),
            output_dim=300,
            mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.GRU(80)),
        tf.keras.layers.Dense(200, activation=tf.nn.leaky_relu),
        tf.keras.layers.Dense(len(encoder_class.get_vocabulary()))
    ])

    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(0.001),
                  metrics=['accuracy'])

    return "trading is done"


# history = model.fit(train_data_batch, epochs=10, validation_data=validation_data_batch, validation_steps=30)
#
# test = model(encoder_data([
#                               "i feel a bit rude writing to an elderly gentleman to ask for gifts because i feel a bit greedy but what is christmas about if not mild greed"]))
#
# test
#
# vocab = encoder_class.get_vocabulary()
#
# vocab
#
# vocab[tf.random.categorical(test, num_samples=1).numpy()[0][0]]
#
# test_data_text, test_class_text = preprocess_dataset('test.txt')
#
# test_data_index = encoder_data(test_data_text)
# test_class_index = encoder_class(test_class_text)
#
# test_data_batch = convert_to_batch(test_data_index, test_class_index, BATCH_SIZE, BUFFER_SIZE)
#
# result = model.evaluate(test_data_batch)
# print(result)
#
# model.save_weights('text_model.h5')
#
# model.load_weights('text_model.h5')
