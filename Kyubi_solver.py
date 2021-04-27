import cv2
import numpy as np

from matplotlib import pyplot as plt

SIZE_CUBE = 3

colors = {
    'white': ([0, 0, 168], [172,100,255]),         # white
    'blue': ([85, 80, 100], [135, 255, 255]),     # Blue
    'yellow': ([26, 110, 117], [40, 255, 255]),   # Yellow
    'orange': ([8, 110, 125], [20, 255, 255]),    # Orange
    'green' : ([40, 52, 72], [80, 255, 255]),     # Green
    'red' : ([160, 100, 84], [179, 255, 255]),    # Red
}

labels_to_colors = {
    'W' : (255,255,255),
    'B' : (8,69,201),
    'Y' : (245,224,0),
    'O' : (245,102,0),
    'G' : (30,255,5),
    'R' : (255,20,20)
}

def detect_color(image, debug=False):
    for (key, (lower,upper)) in colors.items():
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)

        nonzero_normalized = np.count_nonzero(output) / output.size

        if debug:
            pass
            #cv2.imshow(key,np.hstack([image, output]))
            #cv2.waitKey(0)

        if nonzero_normalized > 0.3:
            if debug:
                print(f"{key} detected : accuracy {int(nonzero_normalized*100)}%")
            return key[:1].upper()

    if debug:
        print("no color detected")
    raise Exception("No color has been detected !")


def apply_morph_operation(edges, type, size, it):
    kernel = np.ones(size, np.uint8)
    n_edges = cv2.morphologyEx(edges, type, kernel, iterations=it)
    return n_edges

def get_face_colors_from_file(file_path, debug=False):
    image = cv2.imread(file_path)
    return get_face_colors(image, debug)


def get_face_colors(image, debug=False):
    morph = []

    original = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray,(11,11),2)
    edges = cv2.Canny(imgray,0,30)

    edges = apply_morph_operation(edges, cv2.MORPH_CLOSE, size=(5,5), it=1)
    morph.append(edges)
    edges = apply_morph_operation(edges, cv2.MORPH_DILATE, size=(4,4), it=5)
    morph.append(edges)
    edges = apply_morph_operation(edges, cv2.MORPH_CLOSE, size=(7,7), it=10)
    morph.append(edges)

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

    face = []

    list_pos = list()

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.09*cv2.arcLength(cnt,True),True) # permet de compter le nombre de côtés

        if len(approx) == 4: #si on a 4 côtés c'est un rectangle on garde 
            rect = cv2.boundingRect(approx)
            x1,y1,w,h = rect
            x2,y2 = x1+w, y1+h
            area = w*h

            list_pos.append((x1,y1,x2,y2,area))

    # get rid of the big square if any 
    if len(list_pos) > SIZE_CUBE**2:
        list_pos = sorted(list_pos, key=lambda k: k[4], reverse=True)
        list_pos.pop(0)

    list_pos = sorted(list_pos, key=lambda k: k[1])

    for i in range(0, len(list_pos), SIZE_CUBE):
        list_pos[i:i+SIZE_CUBE]= sorted(list_pos[i:i+SIZE_CUBE], key=lambda k: k[0])

    for (x1,y1,x2,y2,area) in list_pos:
        try:
            detected_color = detect_color(image[y1:y2, x1:x2], debug=debug)
            cv2.rectangle(original, (x1,y1), (x2,y2), labels_to_colors[detected_color], 2)
            face.append(detected_color)
        except:
            if debug:
                print("something get wrong during detection !")
        finally:
            if debug:
                print("")


    if debug:
        print(f"Detected {face}")

    return (original, face)