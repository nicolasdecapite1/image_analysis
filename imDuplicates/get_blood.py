from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
'''
    The goal is to 
        1. find the cluster mean averages for colors in image
        2. compare to a mean value of blood that will be used to compare (could change to a range instead of mean)
        3. use Euclidian distance to determine if blood is in picture or not
            - will compare with each cluster color value to the optimal (blood)
        4. Return success/message to indicate success or failure
'''

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items()))
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    global rgb_colors
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        plt.show()
    #print(rgb_colors)
    return rgb_colors

def match_image_by_color(image, color, threshold = 65, number_of_colors = 4): 
    
    image_colors = get_colors(image, number_of_colors, True)
    selected_color = rgb2lab(np.uint8(np.asarray([[color]])))

    select_image = False
    for i in range(number_of_colors):
        curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
        diff = deltaE_cie76(selected_color, curr_color)
        print(diff)
        if (diff < threshold):
            select_image = True
            print("blood is in image")
            #show image with blood
        # plt.figure(figsize = (8, 6))
        # plt.imshow(image)

    
    return select_image

def hex_to_rgb(rgb_colors):
    global red, green, blue
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]


    return red, green, blue

def delta(red = 1.0, green = 0, blue = 0, delta_b = 50, distance =3.5):
    #blood is color 1
    #need to find the exact rgb i am using, it is fake rn

    global success
    success = False

    
    color1_rgb = sRGBColor(red, green, blue, is_upscaled = True)
    color2_rgb = sRGBColor(106, 51, 51, is_upscaled = True)
    #print(color2_rgb)
    #convert to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)
    #print(color1_lab, color2_lab)
    delta_b = delta_e_cie2000(color1_lab, color2_lab)
    print(delta_b)
    if (delta_b < distance):
        success = True
    else: 
        pass
    return success

def range(red, green, blue):
    color1_rgb = sRGBColor(red, green, blue, is_upscaled = True)
    #convert to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)

    #find L*A*B range
    color1_lab = str(color1_lab)
    l1 = color1_lab[16:23]
    a1 = color1_lab[30:37]
    b1 = color1_lab[44:49]
    l1 = float(l1)
    a1 = float(a1)
    b1 = float(b1)
    print(l1, a1, b1)

    global blood
    blood = True
    #boundary of blood in L*A*B
    boundaries = [([15, 10, 10], [30, 25, 40])]
    for (lower, upper) in boundaries:
        low_l = lower[0]
        low_a = lower[1]
        low_b = lower[2]
        upper_l = lower[0]
        upper_a = lower[1]
        upper_b = lower[2]

    if ( (low_l <= l1) and (l1 <= upper_l)):
        pass
    else:
        blood = False
    if ( (low_a <=  a1) and (a1 <= upper_a)):
        pass
    else:
        blood = False
    if ( (low_b <= b1) and (b1 <= upper_b)):
        pass
    else:
        blood = False
    print("blood is " + str(blood))
    return blood





if __name__ == '__main__':
    image_path = '/Users/nicolasdecapite/Desktop/imDuplicates/blood_images/blood1.jpg'
    # 8 is for the amount of color clusters
    get_colors(get_image(image_path), 10, True)

    
    #distance is benchmark for what we consider "good enough" to be considered blood
    # distance = 25
    # global delta_b
    # for rgb in rgb_colors:
    #     hex_to_rgb(rgb)
        
    #     #calculate delta
    #     #delta(red, green,  blue)

    #     #range of L*A*B
    #     range(red, green, blue)
        
        # if (success): break
    # if (success):
    #     print("Blood in stool")
    # else:
    #     print("No blood in the stool")

    #match_image_by_color(get_image(image_path), [255, 0, 0])