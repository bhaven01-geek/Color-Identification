import pandas as pd
import cv2
import tkinter as tk
from tkinter import filedialog



#Select image/image_path from system
tk.Tk().withdraw()

file_path = filedialog.askopenfilename(filetypes=[("image",".png")])

image_path = file_path

#reading csv file
dataframe = pd.read_csv('files/colors.csv', names=['color', 'color_name', 'hex', 'R', 'G', 'B'], header=None)

#reading image file and resizing it
image = cv2.imread(image_path)
image = cv2.resize(image, (800,600))

click = False
r = b = g = 0

#function to find color name.
def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(dataframe)):
        mins = abs(R - int(dataframe.loc[i,'R']))+abs(G - int(dataframe.loc[i,'G']))+abs(B - int(dataframe.loc[i,'B']))
        if mins<minimum:
            minimum = mins
            color_Name = dataframe.loc[i, 'color_name']
    return color_Name

#function to get particular color co-oridinate to be check/detect.
def function(event, x, y, flags,params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global click,r,b,g
        click = True
        b, g, r = image[y, x]
        b, g, r = int(b), int(g), int(r)

cv2.namedWindow('Color_Detection')
cv2.setMouseCallback('Color_Detection', function)

while True:
    cv2.imshow('Color_Detection', image)
    if click:
        cv2.rectangle(image, (20,20), (600,60), (b,g,r), -1)

        colors = get_color_name(r,g,b) + ' (R : ' + str(r) + ' G : ' + str(g) + ' B : ' + str(b) + ')'

        cv2.putText(image, colors, (30,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)

        if r+g+b >=600:
            cv2.putText(image, colors, (30,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

    # use ESC key to Quit
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()

#Un-Comment the camera section to capture images
'''
####### CAMERA section ###########

import os
import time

tk.Tk().withdraw()
fileName = filedialog.askdirectory()

cam = cv2.VideoCapture(0)
cv2.namedWindow("Capture_Image")

counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Capture_Image", frame)

    k = cv2.waitKey(1)
    
    if k%256 == 27: break                                       # use ESC key to Quit
    elif k%256 == 32:                                           # use SPACE key to Capture Image

        img_name = "opencv_frame_{}.png".format(counter)
        
        cv2.imwrite(os.path.join(fileName, img_name), frame)
        counter += 1
        print(fileName+"/"+img_name + "saved")

cam.release()
cv2.destroyAllWindows()
time.sleep(5)

####################################

'''