#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cv2 as cv
import numpy as np
import sys
import getopt


def main(argv):
    input_path=""
    output_path=""
    
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(" 请在程序结尾输入 -i <视频位置> -o <视频存储位置> ")
        sys.exit(2)
    
    for ots,args in opts:
        if ots=="-h":
            print(" 请在程序结尾输入 -i <视频位置> -o <视频存储位置> ")
            print(" 或者请在程序结尾输入 --input_path <视频位置> --output_path <视频存储位置> ")
            sys.exit()
        elif ots in ("-i","--input_path"):
            input_path=args
        elif ots in ("-o","--output_path"):
            output_path=args
       
    print("输入的文件为：",input_path)
    print("输出的文件为：",output_path)
    clipping_area=input("请输入需要裁剪的左右像素值：")
    print("监控裁剪掉左右%s个像素点"%clipping_area)
    
    cap=cv.VideoCapture(input_path)
    (ret, old_frame) = cap.read()
    
    feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

    
    # Parameters for lucas kanade optical flow 设置 lucas kanade 光流场的参数
    # maxLevel 为使用的图像金字塔层数
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    # Create some random colors 产生随机的颜色值
    color = np.random.randint(0, 255, (100, 3))
    # Take first frame and find corners in it 获取第一帧，并寻找其中的角点


    #print("old_frame'data'shape",old_frame.shape)
    #print("frame's shape:",old_frame.
    img_width=old_frame.shape[1]
    img_height=old_frame.shape[0]
  
    clipping_area=int(clipping_area)
    if clipping_area!=0:
        ROI=old_frame[clipping_area:img_height-clipping_area,clipping_area:img_width-clipping_area]
    elif clipping_area==0:
        ROI=old_frame
    
    
    old_gray = cv.cvtColor(ROI, cv.COLOR_BGR2GRAY)
    p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    # Create a mask image for drawing purposes 创建一个掩膜为了后面绘制角点的光流轨迹
    mask = np.zeros_like(old_frame)

    # 视频文件输出参数设置
    out_fps = 12.0  # 输出文件的帧率
    fourcc = cv.VideoWriter_fourcc('M', 'P', '4', '2')
    sizes = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    out = cv.VideoWriter(output_path, fourcc, out_fps, sizes)



    while True:
        (ret, frame) = cap.read()
        
        if clipping_area!=0:
            frame_roi=frame[clipping_area:img_height-clipping_area,clipping_area:img_width-clipping_area]
        elif clipping_area==0:
            frame_roi=frame
        

        #"""
        frame_gray = cv.cvtColor(frame_roi, cv.COLOR_BGR2GRAY)
        # calculate optical flow 能够获取点的新位置
        p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        # Select good points 取好的角点，并筛选出旧的角点对应的新的角点
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        # draw the tracks 绘制角点的轨迹
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            #print(help(cv.line))
            mask = cv.line(mask, (int(a+clipping_area), int(b+clipping_area)), (int(c+clipping_area), int(d+clipping_area)), color[i].tolist(), 2)
            #print("mask's shape",mask.shape)
            mask=cv.rectangle(mask,(clipping_area,clipping_area),(img_width-clipping_area,img_height-clipping_area),(0,255,0),4)
            frame = cv.circle(frame, (int(a+clipping_area),int(b+clipping_area)), 5, color[i].tolist(), -1)
        img = cv.add(frame, mask)
        cv.imshow('frame', img)
        out.write(img)
        k = cv.waitKey(200) & 0xff
        if k == 27:
            break
        # Now update the previous frame and previous points 更新当前帧和当前角点的位置
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)
        #"""
    out.release()
    cv.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    main(sys.argv[1:])
    
    
    


# In[5]:


from KalmanFilter4imageTrack import Kalman2D
import numpy as np
import cv2 as cv

es = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

cap=cv.VideoCapture("../../videoTest/test1.wmv")


frame1 = cap.read()[1]
prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
print("frame1'size",frame1.shape[1])
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

# 视频文件输出参数设置
out_fps = 12.0  # 输出文件的帧率
fourcc = cv.VideoWriter_fourcc('M', 'P', '4', '2')
sizes = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
out1 = cv.VideoWriter('E:/video/v6.avi', fourcc, out_fps, sizes)
out2 = cv.VideoWriter('E:/video/v8.avi', fourcc, out_fps, sizes)

#global parameters

kalman_est=[]
measure_point=[]
interval=20


class trackXY(object):
    '''
    A class to store X,Y points
    '''
 
    def __init__(self):
 
        self.x, self.y = -1, -1
 
    def __str__(self):
 
        return '%4d %4d' % (self.x, self.y)


kalman2d = Kalman2D()
obj_info=trackXY()



while True:
    (ret, frame2) = cap.read()
    next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)

    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    draw = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
    draw = cv.morphologyEx(draw, cv.MORPH_OPEN, kernel)
    draw = cv.threshold(draw, 25, 255, cv.THRESH_BINARY)[1]
    
    #help(cv.findContours)
    
    #opencv3.2 版本之后不在返回image的值，在此注意
    #image, contours, hierarchy = cv.findContours(draw.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    
    contours, hierarchy = cv.findContours(draw.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for c in contours:
        if cv.contourArea(c) < 500:
            continue
        (x, y, w, h) = cv.boundingRect(c)
        obj_info.x=x
        obj_info.y=y
        #measure=(obj_info.x,obj_info.y)
        #measure_point.append(measure)
        #print("currentpoint",obj_info.x)
        #kalman2d.update(obj_info.x, obj_info.y)
        
      
        
        # Get the current Kalman estimate and add it to the trajectory
        #estimated = [int (c) for c in kalman2d.getEstimate()]
        #kalman_est.append(estimated)
 

        
        
        cv.rectangle(frame2, (x, y), (x + w, y + h), (255, 255, 0), 2)

    #cv.imshow('frame2', bgr)

    #cv.imshow('draw', draw)
    cv.imshow('frame1', frame2)
    out1.write(bgr)
    out2.write(frame2)

    k = cv.waitKey(200) & 0xff
    if k == 27 or k == ord('q'):
        break
    elif k == ord('s'):
        cv.imwrite('opticalfb.png', frame2)
        cv.imwrite('opticalhsv.png', bgr)
    prvs = next
    
out1.release()
out2.release()
cap.release()
cv.destroyAllWindows()


# In[ ]:




