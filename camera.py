# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_BEDlHOdtbAEWSvPgI5Lp00ZydRk48QX
"""

# ! git clone

import cv2
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pickle
from pathlib import Path
from datetime import datetime




class VIDEO :

  _defaults = {
        "id": 0,
        "save": False,
        "anotate": False,
        "save_path" :'./images/from_video/',
        "path" : "./videos/challenge_video.mp4",
        "period" : 0.1
        }

  @classmethod
  def get_defaults(cls, n):
      if n in cls._defaults:
          return cls._defaults[n]
      else:
          return "Unrecognized attribute name '" + n + "'"  

  def __init__(self, **kwargs):
    self.save : bool  
    self.period : float
    self.save_path : str  
    self.anotate : bool 
    self.fps : int
    self.path : str
    self.__dict__.update(self._defaults) # set up default values
    self.__dict__.update(kwargs) # and update with user overrides
    self.video = None 
    self.fps :  int 
    self.step :  int
    # self.extract_frames()

  def extract_frames(self):
    self.video =  cv2.VideoCapture(self.path) 
    self.fps =  self.video.get(cv2.CAP_PROP_FPS)
    # self.step =  int(self.period* self.fps)
    count = 0
    success = 1

    while success: 
      success, image = self.video.read() 
      fn = int(datetime.utcnow().timestamp()*10000)
      cv2.imwrite(self.save_path+str(fn)+".jpg",image)
      count += 1
    print(count, self.fps)




class CAMERA :
  
  def __init__(self):
    self.callibration_done  = False
    self.cam_matrix = None
    self.dist_coeffs= None
    self.img_size = None
    self.rvecs = None
    self.tvecs = None
    # self.callibrate()
    
  
  def callibrate(self , folder = 'camera_cal',n_x = 7, n_y = 7, verbose =   False):
    objp = np.zeros((n_y*n_x, 3), np.float32)
    objp[:, :2] = np.mgrid[0:n_x, 0:n_y].T.reshape(-1, 2)
    image_points = []
    object_points = []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    directory =  Path(folder)
    for image_file in directory.glob("*.jpg"):
      img = cv2.imread(str( image_file))
      img= cv2.resize(img, (400,300))
      img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
      found, corners = cv2.findChessboardCorners(img_gray, (n_x, n_y))
      if found:
          self.callibration_done = True
          corners2 = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
          image_points.append(corners2)
          object_points.append(objp)
          if verbose:
              cv2.drawChessboardCorners(img, (n_x, n_y), corners, found)
              plt.imshow(img)
              plt.show()

    # pefrorm the calibration
    ret, self.cam_matrix, self.dist_coeffs, self.rvecs, self.tvecs = cv2.calibrateCamera(object_points, image_points, img_gray.shape[::-1], None, None)
    self.img_size  = img.shape
    
  def undistort(self, image) :
    if self.callibration_done :
      image = cv2.undistort(image, self.cam_matrix, self.dist_coeffs)
    return image



class EVENT :
  def __init__(self):
    # TAILGAITING ,  FCAS WARNING , LANE CHANGING, TRAFFIC LIGHT JUMP
    self.time_stamp : int
    self.image_path : str
    self.type : int
    self.speed : float
    self.coordinates : [float, float]

if __name__ == "__main__":
    video = VIDEO(path = "./videos/challenge_video.mp4", save=True,period = 1)
    video.extract_frames()
