from PIL import Image
import  cv2, re, sys
import matplotlib.pyplot as plt
import Stereo_conv_net_Mac as stc
from scipy.misc import imresize, imread
from PIL import ImageOps
import scipy as sp
import scipy.ndimage.morphology
import matplotlib.cm as cm
import numpy as np

pred_fn = stc.get_pred_fn()
offset,scale,y_offset,y_scale = stc.get_offset()

def pred():

    dirpath='/home/tanuj/Desktop'

    path = ('{}/DepthMap_{}.png').format(dirpath,1)
    with open(path, 'rb') as f:
        depthM = imread(f)
        size_depthM = depthM.shape
        depthM = Image.open(path)
        depthM = depthM.convert('L')
        depthM = np.array(depthM.getdata(),dtype=np.uint8)
        depthM = depthM.reshape(1,1,100,150)
        

    path = ('{}/Stereoscopic_{}.png').format(dirpath,1)
    with open(path, 'rb') as f:
        StereoIm = imread(f)
        size_StereoIm = StereoIm.shape
        StereoIm = Image.open(path)
        StereoIm = StereoIm.convert('L')
        StereoIm = np.array(StereoIm.getdata(),dtype=np.uint8).reshape(1, size_StereoIm[0], size_StereoIm[1])
        Im_left = StereoIm[0,...,0:size_StereoIm[1]/2]
        Im_right = StereoIm[0,...,size_StereoIm[1]/2:size_StereoIm[1]]
        Im_left = Im_left.reshape(1,1,100,150)
        Im_right = Im_right.reshape(1,1,100,150)
        Inp = np.concatenate((Im_left,Im_right),1)
    Inp = (Inp - offset) / scale
    depthM = (depthM - y_offset)/y_scale
    # print depthM.shape, Inp.shape
    op = pred_fn(Inp)[0]
    f, axarr = plt.subplots(1,3,sharey='col')
    f.set_figheight(10)
    f.set_figwidth(35)
    axarr[0].imshow(Inp[0,0,...],cmap = cm.Greys_r)
    axarr[0].set_title('Left eye grayscale image')
    axarr[1].imshow(depthM[0,0,...])
    axarr[1].set_title('DepthMap ground truth')
    axarr[2].imshow(op[0,0,...])
    axarr[2].set_title('DepthMap prediction')
    f.tight_layout()
    f.show()

