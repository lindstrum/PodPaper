import numpy as np
import matplotlib.pyplot as plt
import glob 
import cv2

equation_pieces = []
text_pieces = []

for path in glob.glob("./equation_data/*.png"):
        print(path)
        img = cv2.imread(path)[:,:,0]
        print(img)
        equation_pieces.append(img)
        

for path in glob.glob("./text_data/*.png"):
        print(path)
        img = cv2.imread(path)[:,:,0]
        print(img)
        text_pieces.append(img)

np.save("equation_pieces", equation_pieces)
np.save("text_pieces", text_pieces)
