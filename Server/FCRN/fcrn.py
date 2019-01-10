import argparse
import os
import numpy as np
import tensorflow as tf
from scipy.misc import imresize
from matplotlib import pyplot as plt
from PIL import Image
import torchvision.transforms.functional as F
import torch

import FCRN.models as models

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
saver.restore(sess, "FCRN/NYU_FCRN.ckpt")

def predict(img):
#     Default input size
#     Read image
    img = torch.tensor(img, dtype=torch.float32)
    img = F.to_pil_image(img)
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