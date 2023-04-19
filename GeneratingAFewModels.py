import NN as n
import tensorflow as tf

"""

Generates a lot of models for comparison
"""

network = n.NN()
network.InputTrainNumber = 64 * 64 * 4
"2048 for training"
network.loadTrainingData()
network.epochs = 55
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
sqd =tf.keras.optimizers.experimental.SGD() 
network.optimizer = adam
network.loss = mse
network.train()
network.save_model("AdamModelMSEBig.keras")
#network.loss = mape
#network.train()
#network.save_model("AdamModelMape.keras")
#network.loss = msle
#network.train()
#network.save_model("AdamModelMsle.keras")
#network.loss = csl
#network.train()
#network.save_model("AdamModelCsl.keras")
#network.loss = lc
#network.train()
#network.save_model("AdamModelLc.keras")
#network.loss = h
#network.train()
#network.save_model("AdamModelH.keras")
network.optimizer = sqd
network.loss = mse
network.train()
network.save_model("SqdModelMSEBig.keras")
#network.loss = mape
#network.train()
#network.save_model("SqdModelMape.keras")
#network.loss = msle
#network.train()
#network.save_model("SqdModelMsle.keras")
#network.loss = csl
#network.train()
#network.save_model("SqdModelCsl.keras")
#network.loss = lc
#network.train()
#network.save_model("SqdModelLc.keras")
#network.loss = h
#network.train()
#network.save_model("SqdModelH.keras")
