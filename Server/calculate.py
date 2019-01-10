from YOLOV3.detect import get_classes, get_bounding_box
from FCRN.fcrn import get_depth
import numpy as np

# Input numpy array [RGB-channel, width, height] range from (0, 1)
# Output detection_numpy: list of numpy array [7]
# Output classes: name list of string
# Output depthmap: numpy array [width, length] range from (0, 1)

def calculate(pic):
    detections = get_bounding_box(pic)
    detections_numpy = []
    if not detections == [] and detections is not None:
        for tensor in detections:
            if tensor is None:
                break
            array = tensor.numpy().squeeze()
            if array.shape[0] == 7:
                detections_numpy.append(array)
    classes = get_classes()
    depthmap = get_depth(pic)
    depthmap = np.squeeze(depthmap)
    return detections_numpy, classes, depthmap


#### DEBUG

# import numpy as np
# import torch

# pic = torch.randn(3, 300, 300)
# pic = pic.numpy()

# import time
# start_time = time.time()
# for i in range(10):
#     a, b, c = calculate(pic)

# print(time.time() - start_time)