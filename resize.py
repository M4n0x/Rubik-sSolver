#!/usr/bin/python
from PIL import Image
import os, sys
import cv2

path = "data\\1\\"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((int(im.size[0]*0.5),int(im.size[1]*0.5)), Image.ANTIALIAS)
            imResize.save(f + ' resized.jpg', 'JPEG', quality=90)

resize()
