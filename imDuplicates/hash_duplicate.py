import os
import time
from os.path import join
import numpy as np #why is it underlined 
import cv2 
import shutil
import math
import imutils 
from skimage import metrics
import hashlib

#translate images to black and white
# def resize():
    
#     imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/images'
#     bwDir = 'bwDir'
#     # Iterate over all images in detected directory
#     for (j, imgName) in enumerate(os.listdir(imgDir)):
#         # Construct patch to single image
#         imgPath = join(imgDir, imgName)
#         #print(imgPath)
        
#         # Read image using OpenCV as grayscale
#         image = cv2.imread(imgPath)
        
#         # Check if we opened an image.
#         if image is not None:
#             # Resize opened image
#             resized_image = cv2.resize(image, (1500, 1500))
#             resized_image = np.array(resized_image)
#             # Save image to bwdir.
#             # Name should be the same as name in "detected" directory
#             cv2.imwrite(os.path.join(imgDir, imgName), resized_image)
#         else:
#             # remove a file that is not an image. I don't need it.
#             print(imgName + 'Deleted!!!!!!!!!')
#             os.remove(imgPath)

#insert the name if statement
def hash_duplicates(imgDir):
    files_list = os.listdir(imgDir)
    duplicates = []
    hash_keys = dict()
    for index, filename in enumerate(os.listdir(imgDir)):
        #print(filename)
        if os.path.isfile(imgDir + '/' + filename):
            with open(imgDir + '/' + filename, 'rb') as f:
                filehash = hashlib.md5(f.read()).hexdigest()
                #print(filehash)
            if filehash not in hash_keys:
                hash_keys[filehash] = index
            else:
                duplicates.append((index, hash_keys[filehash]))
                print(filename + 'is a coppppppyyyyyyyy')
        else:
            print('Didnt reach')
    #remove duplicates from images directory
    print(duplicates)

    for idx in duplicates:
        name = files_list[idx[0]]
        print(name + ' is removed')
        os.remove(imgDir + '/' + name)
       

def main():
    # Define working directory - direcotry with our dowloaded data images
    t0 = time.time()
    imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/Verified'
    bwDir = '/Users/nicolasdecapite/Desktop/imDuplicates/bwDir'
    
    #resize to same size for each image
    #resize()

    # Now lets iterate over all images in black and white dataset
    hash_duplicates(imgDir)
    
    t2 = time.time()
    print(t2 - t0)
if __name__ == '__main__':
    main()


