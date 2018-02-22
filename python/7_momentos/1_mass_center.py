# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 12:27:58 2018

@author: Romualdo Villalobos
"""

import numpy as np
import cv2

# calibration factor
c = 3
n = 75 # using n fotograms

captura = cv2.VideoCapture("video2.mp4")
imgfondo = cv2.imread("background.jpg")

# Creates the window where slider will be placed
cv2.namedWindow("Salida")

h_avg = 0
h_stddev = 0
s_avg = 0
s_stddev = 0

h_min = 0
h_max = 0
s_min = 0
s_max = 0

isCalibrating = True
i = 1
fctr = 1 / n
while(True):
    isDisponible, fotograma = captura.read()
    
    
    if (isDisponible == True):
        print(fotograma.shape)
        alto, ancho, chanels = fotograma.shape
        alto = alto
        ancho = ancho
        
        hsv_frame = cv2.cvtColor(fotograma, cv2.COLOR_BGR2HSV)        
        h, s, v = cv2.split(hsv_frame)
        
        if (isCalibrating):
            #h_f64 = h.astype(np.float64)
            tmp_h_avg, tmp_h_stddev = cv2.meanStdDev(h)                                                  
            h_avg = h_avg + tmp_h_avg[0][0] * fctr
            h_stddev = h_stddev + tmp_h_stddev[0][0] * fctr
            print(h_stddev)
            
            tmp_s_avg, tmp_s_stddev = cv2.meanStdDev(s)
            s_avg = s_avg + tmp_s_avg[0][0] * fctr
            s_stddev = s_stddev + tmp_s_stddev[0][0] * fctr
            
            if (i < n):                
                i += 1
            else:
                h_dist = c * h_stddev
                h_min = h_avg - h_dist
                h_max = h_avg + h_dist
                
                s_dist = c * s_stddev
                s_min = s_avg - s_dist
                s_max = s_avg + s_dist                
                
                isCalibrating = False
                i = 0                
        
        mask_nobin = cv2.inRange(hsv_frame, (h_min, s_min, 20), (h_max, s_max, 255))
        ret, mask = cv2.threshold(mask_nobin, 126, 1, cv2.THRESH_BINARY)
        #ret, mask_inv = cv2.threshold(mask_nobin, 126, 1, cv2.THRESH_BINARY_INV)
        
        fondo = cv2.bitwise_and(imgfondo, imgfondo, mask=mask)
        focus = cv2.bitwise_and(fotograma, fotograma, mask=1-mask)
        
        # calculate moments; read more at:
        # https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=moments#moments
        
        mu = cv2.moments(255-mask_nobin)
        if mu["m00"] <= 1:
            continue;
        print(mu)
        
        shader = 255-mask_nobin#cv2.add(fondo, focus)   
        
        # basic drawing in opencv; read more at:
        # https://docs.opencv.org/2.4/doc/tutorials/core/basic_geometric_drawing/basic_geometric_drawing.html           
        
        #cv2.rectangle(shader, (10, 10), (int(alto), int(ancho)), (255, 255, 255), 5)
        cv2.circle(fotograma, (int(mu["m10"]/mu["m00"]), int(mu["m01"]/mu["m00"]))  , 10, (255, 0, 0), 15)
        #cv2.rectangle()
        
        #res = shader.astype(np.uint8)
        cv2.imshow('Original', fotograma)
        cv2.imshow('Mask', shader)        
        
    else:
        print('Camera not available')
    
    # Waits for 25ms
    wait = 0xFF & cv2.waitKey(10)
    if (wait == ord('q') or wait == ord('Q')):
        print('Here we go')
        break

captura.release()
cv2.destroyAllWindows()
