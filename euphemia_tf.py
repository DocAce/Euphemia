import tensorflow as tf # pylint: disable=import-error

def tf_test():
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    return sess.run(hello)
