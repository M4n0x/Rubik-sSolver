''' 
    Kyubi.py
    Ce script permet de capturer une camera et d'effectuer la detection
    des faces d'un rubiks cube
    He-arc 2021, INF-DLMb
    Maxime Welcklen & Steve Mendes Reis
'''

from Kyubi_solver import *
from rubik_solver import utils
import os 
import keyboard
from PIL import ImageFont, ImageDraw, Image

sequences = [
    ('U', "Face U(pper) : Show yellow center with blue one on your right"),
    ('F', "Face F(ront) : go ↓ (show Red center)"),
    ('L', "Face L(eft) : go → (show Blue center)"),
    ('D', "Face D(own) : go ← ↓ (show White center"),
    ('R', "Face R(ight) : go ↑ ← ← (show Green center)"),
    ('B', "Face B(ack) : go ← (show Orange center)"),
]

cube = []

# VIDEO
import cv2
import time

cap = cv2.VideoCapture(0)
OFFSET_TIME = 0 # allow to take an image every X secondes (set to 0 to take as many images as possible)
timeout = time.time() + OFFSET_TIME # + OFFSET_TIME secondes

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

font = ImageFont.truetype("notosansjp.otf", 21)

stop = False
iter_faces = iter(sequences)
face_id, text = next(iter_faces)

while(True):
    if (time.time() > timeout):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not stop:
            analyse_frame, faces = get_face_colors(frame, debug=False)
            pil_im = Image.fromarray(analyse_frame)  
            draw = ImageDraw.Draw(pil_im)
            draw.text((20,20), text, font=font)
            
            draw.text((20,height-50), "Press q: quit, s: stop, c: continue, v: validate", font=font)
            cv2.imshow('frame', np.array(pil_im))
            cv2.waitKey(1)
        
        # managing key pressing
        if keyboard.is_pressed('q'):
            break
        elif keyboard.is_pressed('s'):
            stop = True
        elif stop and keyboard.is_pressed('c'):
            stop = False
        elif stop and keyboard.is_pressed('v'):
            stop = False
            print(faces)
            cube.append(faces)
            try:
                face_id, text = next(iter_faces)
            except StopIteration:
                break
        
        timeout = time.time() + OFFSET_TIME # + next OFFSET_TIME secondes

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

str_cube = ""

if len(cube) == 6: 
    # swap faces to match solver pattern
    cube[2], cube[1] = cube[1], cube[2]
    cube[4], cube[5] = cube[5], cube[4]
    cube[3], cube[5] = cube[5], cube[3]

    for face in cube:
        for letter in face:
            str_cube += letter

    print("cube :", str_cube)

    print("solution :", utils.solve(str_cube, 'Kociemba'))
