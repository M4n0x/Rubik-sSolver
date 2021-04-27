from rubik_solver import utils
import os 
import keyboard
from PIL import ImageFont, ImageDraw, Image

# cube = 'wowgybwyogygybyoggrowbrgywrborwggybrbwororbwborgowryby'

# print(utils.solve(cube, 'Kociemba'))

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
OFFSET_TIME = 0
timeout = time.time() + OFFSET_TIME # + OFFSET_TIME secondes

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

font = ImageFont.truetype("notosansjp.otf", 21)

stop = False
iter_faces = iter(sequences)
face_id, text = next(iter_faces)

while(True):
    # Capture frame-by-frame

    if (time.time() > timeout):
        ret, frame = cap.read()

        if not stop:
            analyse_frame, faces = get_face_colors(frame, debug=False)
            pil_im = Image.fromarray(analyse_frame)  
            draw = ImageDraw.Draw(pil_im)
            draw.text((20,20), text, font=font, )
            
            draw.text((20,height-50), "Press q: quit, s: stop, c: continue, v: validate", font=font)
            cv2.imshow('frame', np.array(pil_im))
            cv2.waitKey(1)

        # Display the resulting frame

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
                print('no more iter')
                break
        
        timeout = time.time() + OFFSET_TIME # + next OFFSET_TIME secondes

for face in cube:
    print(face)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
