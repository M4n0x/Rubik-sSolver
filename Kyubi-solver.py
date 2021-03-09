import cv2, sys, os
import numpy as np
from imutils import contours

import random as rng
from matplotlib import pyplot as plt

morph = []

def apply_morph_operation(edges, type, size, it):
    kernel = np.ones(size, np.uint8)
    n_edges = cv2.morphologyEx(edges, type, kernel, iterations=it)
    morph.append(n_edges)
    return n_edges

image = cv2.imread('data\\1\\D.jpeg')

colors = {
    'gray': ([76, 0, 41], [179, 255, 70]),        # Gray
    'blue': ([69, 120, 100], [179, 255, 255]),    # Blue
    'yellow': ([21, 110, 117], [45, 255, 255]),   # Yellow
    'orange': ([0, 110, 125], [17, 255, 255])     # Orange
    }

original = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
imgray = cv2.GaussianBlur(imgray,(11,11),2)
edges = cv2.Canny(imgray,0,30)

#edges = apply_morph_operation(edges, cv2.MORPH_ERODE, size=(1,1), it=1)

edges = apply_morph_operation(edges, cv2.MORPH_CLOSE, size=(5,5), it=1)

edges = apply_morph_operation(edges, cv2.MORPH_DILATE, size=(4,4), it=5)

edges = apply_morph_operation(edges, cv2.MORPH_CLOSE, size=(7,7), it=10)

plt.subplot(1,len(morph)+1,1)
plt.imshow(imgray,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

for i in range(0,len(morph)):
    plt.subplot(1,len(morph)+1,i+2)
    plt.imshow(morph[i], cmap = 'gray')
    plt.title(f"Morph op {i+1}"), plt.xticks([]), plt.yticks([])

plt.show()

imageDraw = imgray.copy()

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.09*cv2.arcLength(cnt,True),True) # permet de compter le nombre de côtés

    if len(approx) == 4: #si on a 4 côtés c'est un rectangle on garde 
        rect = cv2.boundingRect(approx)
        cv2.rectangle(imageDraw, rect ,(0,255,0), 3)

#contours = sorted(contours, key=cv2.contourArea)[-9:]

#cv2.drawContours(imageDraw, contours, -1, (0,255,0), 3)
cv2.imshow('Contours', imageDraw)
cv2.waitKey()