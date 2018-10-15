import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

def mnist_basic() :
    mnist = input_data.read_data_sets('mnist', one_hot=True)

    print(mnist.train.images.shape)
    print(mnist.validation.images.shape)
    print(mnist.test.images.shape)

    print(mnist.train.labels.shape)
    print(mnist.train.labels[:5])

    print(mnist.train.num_examples)

def show_accuracy(sess, hx, x, y, title, dataset) :
    pred_arg = tf.argmax(hx, axis=1)
    test_arg = tf.argmax(y, axis=1)

    equals = tf.equal(pred_arg, test_arg)
    equals_float = tf.cast(equals, tf.float32)
    mean = tf.reduce_mean(equals_float)
    print(title, sess.run(mean, {x: dataset.images,
                                   y: dataset.labels}))

def mnist_softmax(x):
    w = tf.Variable(tf.random_uniform([784, 10]))
    b = tf.Variable(tf.random_uniform([10]))

    # (55000, 10) = (55000, 784) @ (784, 10)
    return tf.matmul(x, w) + b
    # return tf.nn.softmax(z)


def mnist_multi_layers(x):
    w1 = tf.Variable(tf.truncated_normal([784, 256]))
    w2 = tf.Variable(tf.truncated_normal([256, 256]))
    w3 = tf.Variable(tf.truncated_normal([256, 10]))

    b1 = tf.Variable(tf.zeros([256]))
    b2 = tf.Variable(tf.zeros([256]))
    b3 = tf.Variable(tf.zeros([10]))

    z1 = tf.matmul(x, w1) + b1
    r1 = tf.nn.relu(z1)

    z2 = tf.matmul(r1, w2) + b2
    r2 = tf.nn.relu(z2)

    return tf.matmul(r2, w3) + b3


def show_model(model) :
    mnist = input_data.read_data_sets('mnist', one_hot=True)
    # train x (55000, 784) / y (55000, 10)

    x = tf.placeholder(tf.float32)
    y = tf.placeholder(tf.float32)

    z = model(x) #흠 .. ㅋ 의 해법 z 와 hx..

    loss_i = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=z)
    loss = tf.reduce_mean(loss_i)

    # optimizer = tf.train.GradientDescentOptimizer(0.1)
    optimizer = tf.train.AdamOptimizer(0.01)
    train = optimizer.minimize(loss)

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    
    epochs = 15
    batch_size = 100
    iteration = mnist.train.num_examples  // batch_size

    for i in range(epochs):
        total = 0
        for j in range(iteration):
            xx, yy = mnist.train.next_batch(batch_size)
            _, c = sess.run([train, loss], {x: xx, y: yy})
            total += c
        print(i, total / iteration)
    print('-' * 50)
    
    show_accuracy(sess, z, x, y, 'train :', mnist.train)
    show_accuracy(sess, z, x, y, 'valid :', mnist.validation)
    show_accuracy(sess, z, x, y, 'test :', mnist.test)

    sess.close()
    
# show_model(mnist_softmax)
show_model(mnist_multi_layers)
#