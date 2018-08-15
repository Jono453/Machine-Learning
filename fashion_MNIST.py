#TensorFlow: Basic Image Classification
#Using Fashion MINST set

import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

print(tf._version_)

#load fashion mnist data set

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels),(test_images, test_labels) = fashion_mnist.load_data()

#training set = data the model uses to learn
#test set = data the model is tested against
#images are 28x28 numpy arrays, labels are integers (0-9) for the different types of clothig
#clothing

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images.shape #(60000,28,28)
len(train_labels) #60000
train_labels #array([9,0,0,....,3,0,5])

#preprocessing data
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.gca().grid(False)

train_images = train_images / 255.0
test_images = test_images / 255.0

#checking test data
plt.figure(figsie = (10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid('off')
    plt.imshow(train_images[1], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])

#BUILD model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)), #2d array to 1d array
    keras.layers.Dense(128,activation=tf.nn.relu),
    keras.layers.Dense(10,activation=tf.nn.softmax) #array of 10 probability scores an object belongs
    #to a class of clothing
    ])

model.compile(optimizer=tf.train.AdamOptimzer(),
                loss='spare_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images,train_labels,epochs=5)

#Evaluate accuracy

test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test accuracy: ', test_acc)

#Predictions
predications = model.predict(test_images)
predictions[0] #array of 10 numbers
np.argmax(predictions[0]) #indicates category 9 was highest
#matches with test data

#plotting 
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid('off')
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    predicted_label = np.argmax(predictions[i])
    true_label = test_labels[i]
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    plt.xlabel("{} ({})".format(class_names[predicted_label), class_names[true_label]),color=color)
