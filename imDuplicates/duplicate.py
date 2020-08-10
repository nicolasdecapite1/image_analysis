import os
import time
from os.path import join
import numpy as np #why is it underlined 
import cv2 
import shutil
import math
import imutils 
from skimage import metrics

#translate images to black and white
def getBwLittleImgs():
    
    imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/images'
    bwDir = 'bwDir'
    #make diirectory if it does not exist
    if not os.path.exists(bwDir):
        os.makedirs(bwDir)
    else:
        shutil.rmtree(bwDir)
        os.makedirs(bwDir)
  
    # Iterate over all images in detected directory
    for (j, imgName) in enumerate(os.listdir(imgDir)):
        # Construct patch to single image
        imgPath = join(imgDir, imgName)
        #print(imgPath)
        
        # Read image using OpenCV as grayscale
        image = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        
        # Check if we opened an image.
        if image is not None:
            # Resize opened image
            resized_image = cv2.resize(image, (2400, 2400))
            resized_image = np.array(resized_image)
            # Save image to bwdir.
            # Name should be the same as name in "detected" directory
            cv2.imwrite(os.path.join(bwDir, imgName), resized_image)
        else:
            # remove a file that is not an image. I don't need it.
            print(imgName + 'Deleted!!!!!!!!!')
            os.remove(imgPath)

#insert the name if statement
def findDelDuplBw(searchedName, bwDir):
        # Join path to orginal image that we are looking duplicates
        searchedImg = join(bwDir, searchedName)
        imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/images'
        imgPath = join(imgDir, searchedName)
        img1 = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        
        if img1 is not None:
            # Resize opened image
            imSize1 = os.path.getsize(imgPath)
            img1 = cv2.resize(img1, (2400,2400))
        i =  0
        for (j, cmpImageName) in enumerate(os.listdir(bwDir)):
            imgPathb = join(imgDir, cmpImageName)
            img2 = cv2.imread(imgPathb, cv2.IMREAD_GRAYSCALE)
            s = 0
            
            img1 = cv2.resize(img1, (2400,2400))
            if img2 is not None:
                # Resize opened image
                imSize2 = os.path.getsize(imgPathb)
                #print(str(imSize2))
                img2 = cv2.resize(img2, (2400,2400))
            cmpImageBw = join(bwDir, cmpImageName)
            cmpImage = join('images', cmpImageName)
            s = 0
            comp = abs(imSize1 - imSize2) 
            if cmpImageName == searchedName:
                #print(cmpImageName)
                pass
            elif (comp < 1500):
                s = metrics.structural_similarity(img1, img2)
                #print(s)
            #delete similar image
            if s >0.97:
                i += 1
                #remove image from ImageBw and Image folder
                os.remove(cmpImageBw)
                os.remove(cmpImage)
                print (searchedImg, cmpImageName, s, 'deleted')  

def main():
    # Define working directory - direcotry with our dowloaded data images
    #datasetPath = os.getcwd()
    # #1: To clean data I wan to produce 32x32 pix images of data set.
    # And store them in "bwdir" in every class
    t0 = time.time()
    imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/images'
    bwDir = '/Users/nicolasdecapite/Desktop/imDuplicates/bwDir'
    getBwLittleImgs()
    # Now lets iterate over all images in black and white dataset
    for (i, img) in enumerate(os.listdir(bwDir)):

        print(img + str(i))
        findDelDuplBw(img,'bwDir')
        
    #remove bwDir
    shutil.rmtree('/Users/nicolasdecapite/Desktop/imDuplicates/bwDir')
    t2 = time.time()
    print(t2 - t0)
if __name__ == '__main__':
    main()


