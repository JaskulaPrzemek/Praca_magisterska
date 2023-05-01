import NN as n
import tensorflow as tf

"""

Generates a lot of models for comparison
"""

network = n.NN()
network.InputTrainNumber = 256 * 4
"2048 for training"
network.epochs = 115
"""
inputs = tf.keras.layers.Input(shape=(445,))
x = tf.keras.layers.Dense(445, activation="elu")(inputs)
x = tf.keras.layers.Dense(1764, activation="elu")(x)
outputs = tf.keras.layers.Dense(1764, activation="elu")(x)
model = tf.keras.Model(inputs=inputs, outputs=outputs)

"""

mse = tf.keras.losses.MeanSquaredError()
adam = "adam"
sqd = tf.keras.optimizers.experimental.SGD()
network.optimizer = adam
network.loss = mse
network.loadTrainingData("TrainingWrapFpa")
network.train()
network.save_model("NewTest/MseAdamWrapF.keras")
network.loadTrainingData("TrainingWrapWoa")
network.train()
network.save_model("NewTest/MseAdamWrapW.keras")
network.loadTrainingData("TrainingNormal")
network.train()
network.save_model("NewTest/MseAdamNorm.keras")
network.optimizer = sqd
network.loss = mse
network.loadTrainingData("TrainingWrapFpa")
network.train()
network.save_model("NewTest/MseSqdWrapF.keras")
network.loadTrainingData("TrainingWrapWoa")
network.train()
network.save_model("NewTest/MseSqdWrapW.keras")
network.loadTrainingData("TrainingNormal")
network.train()
network.save_model("NewTest/MseSqdNorm.keras")
