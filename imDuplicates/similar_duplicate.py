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
from scipy.misc import imread
import scipy
import itertools


def hamming_distance(image, image2):
    score = scipy.spatial.distance.hamming(image, image2)
    return score

def resize(image, height=30, width=30):
    row_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten()
    col_res = cv2.resize(image,(height, width), interpolation = cv2.INTER_AREA).flatten('F')
    #print(row_res, col_res)
    return row_res, col_res

#gradient direction based on intensity 
def intensity_diff(row_res, col_res):
    difference_row = np.diff(row_res)
    difference_col = np.diff(col_res)
    difference_row = difference_row > 0
    difference_col = difference_col > 0
    return np.vstack((difference_row, difference_col)).flatten()

#First turn the image into a gray scale image
def img_gray(image, imgDir):
    image = cv2.imread(imgDir + '/' + image, cv2.IMREAD_GRAYSCALE)
    #print(image)
    return image


def difference_score(image, imgDir, height = 30, width = 30):
    
    gray = img_gray(image, imgDir)
    row_res, col_res = resize(gray, height, width)
    difference = intensity_diff(row_res, col_res)
    #print(difference)
    return difference

#insert the name if statement
def difference_score_dict():
    ds_dict = {}
    duplicates = []
    imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/Verified_check'
    image_list = os.listdir(imgDir)
    i =0
    for image in image_list:
        #print(image)
        if image != '.DS_Store':
            ds = difference_score(image, imgDir)
            #print(i)
            if image not in ds_dict:
                ds_dict[image] = ds
            else:
                duplicates.append((image, ds_dict[image]) )
            i+=1
    print(i)
    return duplicates, ds_dict

    #remove duplicate images
    '''
    for idx in duplicates:
        name = image_list[idx[0]]
        print(name + ' is removed')
        os.remove(imgDir + '/' + name)
    '''
       

def main():
    # Define working directory - direcotry with our dowloaded data images
    #datasetPath = os.getcwd()
    # #1: To clean data I wan to produce 32x32 pix images of data set.
    # And store them in "bwdir" in every class
    t0 = time.time()
    imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/Verified_check'


    duplicates, ds_dict = difference_score_dict()
    
    #go through all combinations
    ct = 0

    for k1,k2 in itertools.combinations(ds_dict, 2):
        #print(hamming_distance(ds_dict[k1], ds_dict[k2]))
        if hamming_distance(ds_dict[k1], ds_dict[k2])< .05:
            duplicates.append((k1,k2))
            print(k1, k2, hamming_distance(ds_dict[k1], ds_dict[k2]))
            ct +=1
    print(ct)
    print(duplicates)
    t2 = time.time()
    print(t2 - t0)
if __name__ == '__main__':
    main()


#translate images to black and white
'''
def resize():
    
    imgDir = '/Users/nicolasdecapite/Desktop/imDuplicates/images'
    bwDir = 'bwDir'
    # Iterate over all images in detected directory
    for (j, imgName) in enumerate(os.listdir(imgDir)):
        # Construct patch to single image
        imgPath = join(imgDir, imgName)
        #print(imgPath)
        
        # Read image using OpenCV as grayscale
        image = cv2.imread(imgPath)
        
        # Check if we opened an image.
        if image is not None:
            # Resize opened image
            resized_image = cv2.resize(image, (1500, 1500))
            resized_image = np.array(resized_image)
            # Save image to bwdir.
            # Name should be the same as name in "detected" directory
            cv2.imwrite(os.path.join(imgDir, imgName), resized_image)
        else:
            # remove a file that is not an image. I don't need it.
            print(imgName + 'Deleted!!!!!!!!!')
            os.remove(imgPath)
'''