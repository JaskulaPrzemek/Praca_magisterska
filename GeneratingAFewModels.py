import NN
import tensorflow as tf

"""

Generates a shiteton of models for comparison
"""

network = NN()
network.InputTrainNumber = 64 * 32 * 1
"2048 for training"
network.loadTrainingData()
network.epochs = 15
"""
inputs = tf.keras.layers.Input(shape=(445,))
x = tf.keras.layers.Dense(445, activation="elu")(inputs)
x = tf.keras.layers.Dense(1764, activation="elu")(x)
outputs = tf.keras.layers.Dense(1764, activation="elu")(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

"""

mse = tf.keras.losses.MeanSquaredError()
mape = tf.keras.losses.MeanAbsolutePercentageError()
msle = tf.keras.losses.MeanSquaredLogarithmicError()
csl = tf.keras.losses.CosineSimilarity()
lc = tf.keras.losses.LogCosh()
h = tf.keras.losses.Huber()
adam = "adam"
sqd = "sqd"
network.optimizer = adam
network.loss = mse
network.train()
network.save("AdamModelMSE.keras")
network.loss = mape
network.train()
network.save("AdamModelMape.keras")
network.loss = msle
network.train()
network.save("AdamModelMsle.keras")
network.loss = csl
network.train()
network.save("AdamModelCsl.keras")
network.loss = lc
network.train()
network.save("AdamModelLc.keras")
network.loss = h
network.train()
network.save("AdamModelH.keras")
network.optimizer = sqd
network.loss = mse
network.train()
network.save("SqdModelMSE.keras")
network.loss = mape
network.train()
network.save("SqdModelMape.keras")
network.loss = msle
network.train()
network.save("SqdModelMsle.keras")
network.loss = csl
network.train()
network.save("SqdModelCsl.keras")
network.loss = lc
network.train()
network.save("SqdModelLc.keras")
network.loss = h
network.train()
network.save("SqdModelH.keras")
