import numpy as np
import argparse
import cv2

#load the image
image_path = '/Users/nicolasdecapite/Desktop/imDuplicates/blood_images/blood2.jpg'
image = cv2.imread(image_path)

#boundary of blood in L*A*B
boundaries = [ ([20, 40, 30], [30, 50, 40]) ]