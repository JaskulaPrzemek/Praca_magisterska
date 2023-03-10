import numpy as np
import random
import math
from interfaces import InitializationInterface
import Qlearning as Q
import Mapa as mp
import tensorflow as tf
class NN(InitializationInterface):

    class CustomModel(tf.keras.Model):
        def __init__(self,model):
            super().__init__()
            self.Qlearning=Q.Qlearning()
            self.Qlearning.setEpsilon(0.05)
            self.Qlearning.setDisableInit()
            self.model=model
        def call(self, x):
            # Equivalent to `call()` of the wrapped keras.Model
            x = self.model(x)
            return x
    
        def train_step(self, data):
            # Unpack the data. Its structure depends on your model and
            # on what you pass to `fit()`.
            x, y = data

            with tf.GradientTape() as tape:
                y_test= self(x, training=True)  # Forward pass
                # Compute the loss value
                # (the loss function is configured in `compile()`)
                self.Qlearning.map.loadListRep((x.numpy()).tolist()[0])
                y_pred= self.run_average_steps(1,y_test.numpy())
                #print(y)
                #print(y_pred)
                loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses)

            # Compute gradients
            trainable_vars = self.trainable_variables
            gradients = tape.gradient(loss, trainable_vars)
            # Update weights
            self.optimizer.apply_gradients(zip(gradients, trainable_vars))
            # Update metrics (includes the metric that tracks the loss)
            self.compiled_metrics.update_state(y, y_pred)
            # Return a dict mapping metric names to current value
            return {m.name: m.result() for m in self.metrics}
        
        def run_average_steps(self,n,Q_list):
            avg=[]
            for Q in Q_list:
                suma=0
                Q=np.reshape(Q,(400,4))
                for i in range(n):
                    print(f"Run {i}")
                    self.Qlearning.Q=Q
                    #print(Q)
                    self.Qlearning.learn()
                    steps=self.Qlearning.steps
                    #print(steps)
                    suma+=sum(steps)
                avg.append(suma/n)
                #print(avg)
            avg=tf.constant(avg)
            return avg
            

        

    def __init__(self):
        self.model = tf.keras.Sequential([
            #map is 21*21,start is 2, finish is 2
        tf.keras.layers.InputLayer(input_shape=(445,)),
        tf.keras.layers.Dense(445, activation='relu'),
        tf.keras.layers.Dense(445, activation='relu'),
            #output is the Q which is 20*20*4
        tf.keras.layers.Dense(1600,activation='softmax')
        ])
        self.InputTrainNumber= 64*1
        self.model=self.CustomModel(self.model)

    def getTrainData(self):
        xdata=[]
        ydata=[22*100]*self.InputTrainNumber
        mapa=mp.Map()
        with open("Training_maps.txt",'a') as file:
            for i in range(self.InputTrainNumber):
                mapa.createRandomMap()
                v=mapa.getListRep()
                file.write(f"{str(v)} \n")
                xdata.append(v)
            
        self.TrainX=xdata
        self.TrainY=ydata
        print("Finished generating")
    def loadTrainingData(self):
        xdata=[]
        with open("Training_maps.txt",'r') as file:
            for line in file:
                xdata.append(eval(line))
            #print(xdata)
        ydata=[22*100]*len(xdata)
        self.TrainX=xdata
        self.TrainY=ydata
        print("Finished loading")
    def train(self):
        self.model.compile(tf.keras.optimizers.SGD(),run_eagerly=True,metrics=['mse'],loss=tf.keras.losses.MeanAbsoluteError())
        self.model.fit(self.TrainX,self.TrainY,epochs=5, batch_size=4,verbose=1)
    def save(self,path="model"):
        self.model.save(path)
    def load(self,path="model"):
        self.model=tf.keras.models.load_model(path)
    def initialize(self,map,gazebo):
        pass
    def save(self,path="data.txt",full=True,Q=True):
        pass

network=NN()
network.InputTrainNumber= 64*64*8
network.loadTrainingData()
network.train()