import os
import numpy as np
import tensorflow as tf
from PIL import Image

import models as models

height = 228
width = 304
channels = 3
batch_size = 1

# Create a placeholder for the input image
input_node = tf.placeholder(tf.float32, shape=(None, height, width, channels))

# Construct the network
net = models.ResNet50UpProj({'data': input_node}, batch_size, 1, False)

sess = tf.Session()

saver = tf.train.Saver()
saver.restore(sess, "NYU_FCRN.ckpt")

def predict(img):
#     Default input size
#     Read image
    img = Image.from_array(img)
    img = img.resize([width, height], Image.ANTIALIAS)
    img = np.array(img).astype('float32')
    img = np.expand_dims(np.asarray(img), axis = 0)

#     Use to load from npy file
#     net.load(model_data_path, sess)
#     Evalute the network for the given image

    pred = sess.run(net.get_output(), feed_dict={input_node: img})
    return pred
                
def get_depth(pic):
    return predict(pic)

if __name__ == "__main__":
    import cv2
    import time
    image = cv2.imread("1.png")
    for i in range(100):
        t = time.time()
        get_depth(image)
        print("FPS: %.2f" %(1/(time.time()-t)))
    sess.close()