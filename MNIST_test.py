import tensorflow as tf
#print(tf.__version__)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
 
# Load pre-shuffled MNIST data into train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()
#print (X_train.shape)
from matplotlib import pyplot as plt
#plt.imshow(X_train[0])

# 5. Preprocess input data
X_train /= 255
X_test /= 255

# Model architecture
model = Sequential()

#---Set up Layers---


# Compile model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

'''
# 9. Fit model on training data
model.fit(X_train, Y_train, 
          batch_size=32, nb_epoch=10, verbose=1)
 
# 10. Evaluate model on test data
score = model.evaluate(X_test, Y_test, verbose=0)
'''
#Saving trained Keras CNN model
#from keras.models import load_model
#model.save('mnist_trained_model.h5')  # creates a HDF5 file
#on Pi -> model = load_model('my_model.h5')
