from Kyubi_solver import *
import os 

directory = r'data\\1'
for filename in os.listdir(directory):
    if filename.endswith(".jpeg"):
        file_path = os.path.join(directory, filename)
        #print(file_path, get_face_colors(file_path=file_path, debug=False))

print(get_face_colors(file_path="data\\1\\R.jpeg", debug=False))