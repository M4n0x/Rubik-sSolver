from Kyubi_solver import *
import os 

'''
directory = r'data\\1'
for filename in os.listdir(directory):
    if filename.endswith(".jpeg"):
        file_path = os.path.join(directory, filename)
        #print(file_path, get_face_colors_from_file(file_path=file_path, debug=False))
'''

'''
frame, face = get_face_colors_from_file(file_path="data\\webcam\\img_2_976.jpg", debug=True)
cv2.imshow('frame', frame)
cv2.waitKey()
'''

# VIDEO
import cv2
import time

cap = cv2.VideoCapture(0)
OFFSET_TIME = 0
timeout = time.time() + OFFSET_TIME # + OFFSET_TIME secondes

count = 1

while(True):
    # Capture frame-by-frame

    if (time.time() > timeout):
        ret, frame = cap.read()

        #cv2.imwrite(f"data\\webcam\\img_2_{count}.jpg", frame)
        count += 1

        frame, faces = get_face_colors(frame, debug=False)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
        timeout = time.time() + OFFSET_TIME # + next OFFSET_TIME secondes

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
