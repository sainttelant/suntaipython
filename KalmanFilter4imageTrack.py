#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import numpy as np
 
class Kalman2D(object):
    '''
    A class for 2D Kalman filtering
    '''
 
    def __init__(self, processNoiseCovariance=1e-4, measurementNoiseCovariance=1e-1, errorCovariancePost=0.1):
        '''
        Constructs a new Kalman2D object.  
        For explanation of the error covariances see
        http://en.wikipedia.org/wiki/Kalman_filter
        '''
        # 状态空间：位置--2d,速度--2d
        
        self.kalman=cv.KalmanFilter(4,2,0)
        
        #self.kalman_state = cv.CreateMat(4, 1, cv.CV_32FC1)
        self.kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32)*0.03
        self.kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,1]],np.float32)
        self.kalman.transitionMatrix=np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
        
 
        self.predicted = None
        self.esitmated = None
 
    def update(self, x, y):
        '''
        Updates the filter with a new X,Y measurement
        '''
 
        self.kalman.measurementMatrix[0, 0] = x
        self.kalman.measurementMatrix[1, 0] = y
 
        #self.predicted = cv.KalmanFilter.predict(self.kalman)
        #self.corrected = cv.KalmanFilter.correct(self.kalman, self.kalman.measurementMatrix)
 
    def getEstimate(self):
        '''
        Returns the current X,Y estimate.
        '''
 
        return self.corrected[0,0], self.corrected[1,0]
 
    def getPrediction(self):
        '''
        Returns the current X,Y prediction.
        '''
 
        return self.predicted[0,0], self.predicted[1,0]


# In[ ]:




