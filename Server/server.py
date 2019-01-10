from flask import Flask 
from flask_socketio import SocketIO, send, emit
import base64,cv2
import numpy as np
import time
from tools.image_data_converter import Image_Data_Converter
from modules.description_generator import Description_Generator
from PIL import Image
from matplotlib import pyplot as plt
import io
import statistics
import calculate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
idc=Image_Data_Converter()
dg=Description_Generator()

#@socketio.on('message')
#def handleMessage(msg):

# msg='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAAZSURBVBhXY3gro/JfaaPPf8b/QMC4+CUDAFaLCdVW5z6rAAAAAElFTkSuQmCC'
# print('Message: ' + msg)
# print('\n')
# print('type',type(msg))
# print('\n')
# nmsg=msg[22:]
# print (nmsg)
# fh = open("imageToSave.png", "wb")
# cb=(base64.urlsafe_b64decode(nmsg + '=' * (4 - len(nmsg) % 4)))
# imgarr=idc.bytes_to_np_array(cb)
# imgarr = imgarr[:, :, 0:3]
# imgarr = np.stack([imgarr[:,:,2],imgarr[:,:,1],imgarr[:,:,0]],axis=2)
# imgarr = np.transpose(imgarr, (2, 0, 1))/255
# print (imgarr)
# print(imgarr.shape)
# fh.write(cb)
# fh.close()
#TODO: Update js
@socketio.on('imageprocessing')
def handleImageProcessing(msg):
    nmsg=msg[22:]
    cb=(base64.urlsafe_b64decode(nmsg + '=' * (4 - len(nmsg) % 4)))
    imgarr=idc.bytes_to_np_array(cb)
    imgarr = imgarr[:, :, 0:3]
    imgarr = np.stack([imgarr[:,:,2],imgarr[:,:,1],imgarr[:,:,0]],axis=2)
    imgarr = np.transpose(imgarr, (2, 0, 1))/255
    #bb: 416*416 dm:
    detections, classes, depthmap = calculate.calculate(imgarr)

    dist = np.sum(depthmap[64-10:64+10, 80-40:80+40])
    print(dist)
    if dist < 1800:
        emit('vibrate', '6')
    elif dist < 2000:
        emit('vibrate', '5')
    elif dist < 2100:
        emit('vibrate', '4')
    elif dist < 2300:
        emit('vibrate', '2')
    elif dist < 2700:
        emit('vibrate', '1')

    print(detections,'\n')
    for x1,y1,x2,y2,_,_,c in detections:
        cl = classes[int(c)]
        object_width = int(x2 - x1)
        object_length = int(y2 - y1)
        if object_width <= 0 or object_length <= 0:
            break
        x1, x2 = x1/416*128, x2/416*160
        # depthmap = depthmap[int(x1):int(x2), int(y1):int(y2)]
        # dist = numpy.sum(depthmap)/(x2-x1)/(y2-y1)
        print(dist)
        left, right = x1, 416 - x2
        if abs(left - right) > 20:
            if left > right and dist < 2100:
                emit('playsound', cl + ' is on your right side. And it\'s pretty close')
            if left < right and dist < 2100:
                emit('playsound', cl + ' is on your right side. And it\'s pretty close')

    # fig = plt.figure()
    # ii = plt.imshow(depthmap, interpolation='nearest')
    # fig.colorbar(ii)


    # print(depthmap.shape,'\n')
    # nmsg = msg[22:]
    # cb = (base64.urlsafe_b64decode(nmsg + '=' * (4 - len(nmsg) % 4)))
    # description_string=dg.analyze_image(cb,True)
    # send(description_string, broadcast=True)

@socketio.on('describe')
def handleDescription(msg):
    nmsg = msg[22:]
    print(nmsg[len(nmsg)-2:len(nmsg)])
    cb = (base64.urlsafe_b64decode(nmsg + '=' * (4 - len(nmsg) % 4)))
    description_string=dg.analyze_image(cb,True)
    emit('playsound', description_string)

if __name__ == '__main__':
    socketio.run(app)
