''' 
    Kyubi_solver.py
    Ce module permet la detection des faces d'un rubiks cube, 
    il permet aussi de recuperer les couleurs associees a une
    face d'un cube 
    He-arc 2021, INF-DLMb
    Maxime Welcklen & Steve Mendes Reis
'''

import cv2
import numpy as np
import statistics as stat
from matplotlib import pyplot as plt

SIZE_CUBE = 3

colors = {
    'orange': ([7, 110, 125], [20, 255, 255]),    # Orange
    'yellow': ([26, 110, 100], [40, 255, 255]),   # Yellow
    'green' : ([40, 52, 72], [80, 255, 255]),     # Green
    'red' : ([160, 100, 84], [179, 255, 255]),    # Red
    'red2' : ([0, 100, 84], [6, 255, 255]),       # Red
    'white': ([0, 0, 168], [160, 200, 255]),      # White
    'blue': ([85, 90, 100], [125, 255, 255]),     # Blue
}

labels_to_colors = {
    'W' : (255,255,255),
    'B' : (201,69,8),
    'Y' : (0,224,245),
    'O' : (0,102,245),
    'G' : (5,255,30),
    'R' : (20,20,255)
}


def detect_color(image, origin, threshold=0.3, debug=False):
    '''
        Permet la detection d'une couleur sur une portion d'une image 
        Cette fonction retourne la premiere couleur qui depasse un taux de précision de 30%
        (Amelioration : calculer la precision pour chaque couleur, prendre la plus haute)
    '''
    for (key, (lower,upper)) in colors.items():
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)

        # count the number of pixel matching and normalize it (value between 0 and 1)
        nonzero_normalized = np.count_nonzero(output) / output.size
        
        if debug:
            print(f"{key} accuracy : {int(nonzero_normalized*100)}, median : {cv2.mean(image)}")

        # if the accuracy is over the threshold we return the color
        if nonzero_normalized > threshold:
            if debug:
                print(f"{key} detected : accuracy {int(nonzero_normalized*100)}%")
            return key[:1].upper()

    if debug:
        print("no color detected")
    raise Exception("No color has been detected !")


def apply_morph_operation(edges, type, size, it):
    '''
        Internal function used to apply morphology operations
        and keep tracks of them
    '''
    kernel = np.ones(size, np.uint8)
    n_edges = cv2.morphologyEx(edges, type, kernel, iterations=it)
    return n_edges

def get_face_colors_from_file(file_path, debug=False):
    '''
        Convinent wrapper to get_face_colors with an static image
    '''
    image = cv2.imread(file_path)
    return get_face_colors(image, debug)


def get_face_colors(image, debug=False):
    '''
        Main function
        used to detect square and color inside them, 
        the function return the image with annoted information about detection
        and the square detection in a list in a row major representation :
        1 2 3
        4 5 6
        7 8 9
    '''
    morph = []

    original = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur the image to remove smalls artefacts 
    imgray = cv2.GaussianBlur(imgray,(13,13),10)
    
    #get contours
    edges = cv2.Canny(imgray,0,30)

    # Apply morphologies
    edges = apply_morph_operation(edges, cv2.MORPH_CLOSE, size=(5,5), it=1)
    morph.append(edges)
    edges = apply_morph_operation(edges, cv2.MORPH_DILATE, size=(4,4), it=5)
    morph.append(edges)
    edges = apply_morph_operation(edges, cv2.MORPH_CLOSE, size=(6,6), it=8)
    morph.append(edges)

    # offset used for debug purpose
    offset = 1

    if debug:
        plt.subplot(1,len(morph)+offset,1)
        plt.imshow(imgray,cmap = 'gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])

        for i in range(0,len(morph)):
            plt.subplot(1,len(morph)+offset,i+offset+1)
            plt.imshow(morph[i], cmap = 'gray')
            plt.title(f"Morph op {i+1}"), plt.xticks([]), plt.yticks([])

        plt.show()

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    squares = []

    list_pos = list()

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.08*cv2.arcLength(cnt,True),True) # used to count the number of sides

        if len(approx) == 4: # if there is exactly 4 sides we keep it
            rect = cv2.boundingRect(approx)
            x1,y1,w,h = rect
            x2,y2 = x1+w, y1+h
            area = w*h

            list_pos.append((x1,y1,x2,y2,area))

    # Determine the media area of all the square as we looking for 9 similars squares
    median = 0 if (len(list_pos)==0) else stat.median([k[4] for k in list_pos])

    for (x1,y1,x2,y2,area) in list_pos:
        try:
            #cv2.rectangle(original, (x1,y1), (x2,y2), (125,125,125), 2) # used to mark all square
            detected_color = detect_color(image[y1:y2, x1:x2], original[y1:y2, x1:x2], debug=debug)
            
            ratio = median/area
            if (ratio > 0.4 and ratio < 1.5):
                cv2.rectangle(original, (x1,y1), (x2,y2), labels_to_colors[detected_color], 2) # draw colored square
                squares.append((x1,y1,detected_color,area))
        except:
            if debug:
                print("something get wrong during detection !")
        finally:
            if debug:
                print("")

    # Sorting square to keep row major order

    # first we sort by coordinate X
    squares = sorted(squares, key=lambda k: k[1])

    # And then by Y (3 by 3)
    for i in range(0, len(squares), SIZE_CUBE):
        squares[i:i+SIZE_CUBE]= sorted(squares[i:i+SIZE_CUBE], key=lambda k: k[0])

    # comprehension list to get only the color values k contains (x1,y1,detected_color,area)
    face = [k[2] for k in squares]

    if debug:
        print(f"Detected {face}")

    return (original, face)