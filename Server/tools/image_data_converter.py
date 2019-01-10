import cv2
import numpy as np
class Image_Data_Converter:
    def __init__(self):
        pass
    def bytes_to_np_array(self,image_bytes):
        return cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    def rgb2gray(rgb):
        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray