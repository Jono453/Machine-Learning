import tensorflow as tf
print(tf.__version__)

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

#data set contains 55000 data for training. 10000 for test and 5000 for validation
#every data point has two parts. image of handwritten digit (x) + label (y)

#28x28 image
#mnist.train.images flattened. pixel array of 28*28 = 784
#every image is a digit between 0 and 9. 

x = tf.placeholder(tf.float32,[None, 784]) #value to input any number of MNIST images

#Weights and Bias]
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

#implement model
y = tf.nn.softmax(tf.matmul(x,W)+b)

#training
y_ = tf.placeholder(tf.float32,[None,10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

#reduce_mean calculates the mean over all examples in batch
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

#rrun training steps
#at each step in for loop. get batch of one hundred random points from train set. 
for _ in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  
#Evaluating model
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print("Accuracy was: ", sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

#Saving trained CNN model for use on hardware
save_path = saver.save(sess, "/tmp/model.ckpt")
print("Model saved in path: %s" % save_path)
print('Trained Model Saved.')

