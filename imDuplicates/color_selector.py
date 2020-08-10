from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

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
    idx = 0
    maxim = 0
    total = sum(counts.values())
    for count, val in counts.items():
        test = val/total
        if (test > maxim):
            maxim = test
            idx = count 
            maximum = val
    
    hex_majority = hex_colors[idx]
    global rgb_majority
    rgb_majority = ordered_colors[idx]
    # print(hex_majority, rgb_majority)
    
    return rgb_majority

def match_image_by_color(rgb_majority, threshold = 65, number_of_colors = 4): 
    global COLORS
    COLORS = {
    'Vivid pink': [253, 121, 146],
    'Strong pink': [244, 143, 160],
    'Deep pink': [230, 105, 128],
    'Light pink': [248, 195, 206],
    'Moderate pink': [226, 163, 174],
    'Dark pink': [197, 128, 138],
    'Pale pink': [239, 209, 220],
    'Grayish pink': [203, 173, 183],
    'Pinkish white': [239, 221, 229],
    'Pinkish gray': [199, 182, 289],
    'Vivid red': [213, 28, 60],
    'Strong red': [191, 52, 75],
    'Deep red': [135, 18, 45],
    'Very deep red': [92, 6, 37],
    'Moderate red': [177, 73, 85],
    'Dark red': [116, 36, 52],
    'Very dark red': [72, 17, 39],
    'Light grayish red': [180, 136, 141],
    'Grayish red': [152, 93, 98],
    'Dark grayish red': [83, 56, 62],
    'Blackish red': [51, 33, 39],
    'Reddish gray': [146, 129, 134],
    'Dark reddish gray': [93, 78, 83],
    'Reddish black': [48, 38, 43],
    'Vivid yellowish pink': [253, 126, 93],
    'Strong yellowish pink': [245, 144, 128],
    'Deep yellowish pink': [239, 99, 102],
    'Light yellowish pink': [248, 196, 182],
    'Moderate yellowish pink': [226, 166, 152],
    'Dark yellowish pink': [201, 128, 126],
    'Pale yellowish pink': [241, 211, 209],
    'Grayish yellowish pink': [203, 172, 172],
    'Brownish pink': [203, 175, 167],
    'Vivid reddish orange': [232, 59, 27],
    'Strong reddish orange': [219, 93, 59],
    'Deep reddish orange': [175, 51, 24],
    'Moderate reddish orange': [205, 105, 82],
    'Dark reddish orange': [162, 64, 43],
    'Grayish reddish orange': [185, 117, 101],
    'Strong reddish brown': [139, 28, 14],
    'Deep reddish brown': [97, 15, 18],
    'Light reddish brown': [172, 122, 115],
    'Moderate reddish brown': [125, 66, 59],
    'Dark reddish brown': [70, 29, 30],
    'Light grayish reddish brown': [158, 127, 122],
    'Grayish reddish brown': [108, 77, 75],
    'Dark grayish reddish brown': [67, 41, 42],
    'Vivid orange': [247, 118, 11],
    'Brilliant orange': [253, 148, 63],
    'Strong orange': [234, 129, 39],
    'Deep orange': [194, 96, 18],
    'Light orange': [251, 175, 130],
    'Moderate orange': [222, 141, 92],
    'Brownish orange': [178, 102, 51],
    'Strong brown': [138, 68, 22],
    'Deep brown': [87, 26, 7],
    'Light brown': [173, 124, 99],
    'Moderate brown': [114, 74, 56],
    'Dark brown': [68, 33, 18],
    'Light grayish brown': [153, 127, 117],
    'Grayish brown': [103, 79, 72],
    'Dark grayish brown': [62, 44, 40],
    'Light brownish gray': [146, 130, 129],
    'Brownish gray': [96, 82, 81],
    'Brownish black': [43, 33, 30],
    'Vivid orange yellow': [246, 166, 0],
    'Brilliant orange yellow': [255, 190, 80],
    'Strong orange yellow': [240, 161, 33],
    'Deep orange yellow': [208, 133, 17],
    'Light orange yellow': [252, 194, 124],
    'Moderate orange yellow': [231, 167, 93],
    'Dark orange yellow': [195, 134, 57],
    'Pale orange yellow': [238, 198, 166],
    'Strong yellowish orange': [158, 103, 29],
    'Deep yellowish brown': [103, 63, 11],
    'Light yellowish brown': [196, 154, 116],
    'Moderate yellowish brown': [136, 102, 72],
    'Dark yellowish brown': [80, 52, 26],
    'Light grayish yellowish brown': [180, 155, 141],
    'Grayish yellowish brown': [126, 105, 93],
    'Dark grayish yellowish brown': [77, 61, 51],
    'Vivid yellow': [241, 191, 21],
    'Brilliant yellow': [247, 206, 80],
    'Strong yellow': [217, 174, 47],
    'Deep yellow': [184, 143, 22],
    'Light yellow': [244, 210, 132],
    'Moderate yellow': [210, 175, 99],
    'Dark yellow': [176, 143, 66],
    'Pale yellow': [239, 215, 178],
    'Grayish yellow': [200, 177, 139],
    'Dark grayish yellow': [169, 144, 102],
    'Yellowish white': [238, 223, 218],
    'Yellowish gray': [198, 185, 177],
    'Light olive brown': [153, 119, 54],
    'Moderate olive brown': [112, 84, 32],
    'Dark olive brown': [63, 44, 16],
    'Vivid greenish yellow': [235, 221, 33],
    'Brilliant greenish yellow': [233, 220, 85],
    'Strong greenish yellow': [196, 184, 39],
    'Deep greenish yellow': [162, 152, 18],
    'Light greenish yellow': [233, 221, 138],
    'Moderate greenish yellow': [192, 181, 94],
    'Dark greenish yellow': [158, 149, 60],
    'Pale greenish yellow': [230, 220, 171],
    'Grayish greenish yellow': [190, 181, 132],
    'Light olive': [139, 125, 46],
    'Moderate olive': [100, 89, 26],
    'Dark olive': [53, 46, 10],
    'Light grayish olive': [142, 133, 111],
    'Grayish olive': [93, 85, 63],
    'Dark grayish olive': [53, 48, 28],
    'Light olive gray': [143, 135, 127],
    'Olive gray': [88, 81, 74],
    'Olive black': [35, 33, 28],
    'Vivid yellow green': [167, 220, 38],
    'Brilliant yellow green': [195, 223, 105],
    'Strong yellow green': [130, 161, 43],
    'Deep yellow green': [72, 108, 14],
    'Light yellow green': [206, 219, 159],
    'Moderate yellow green': [139, 154, 95],
    'Pale yellow green': [215, 215, 193],
    'Grayish yellow green': [151, 154, 133],
    'Strong olive green': [44, 85, 6], 
    'Deep olive green': [35, 47, 0], 
    'Moderate olive green': [73, 91, 34],
    'Dark olive green': [32, 52, 11],
    'Grayish olive green': [84, 89, 71],
    'Dark grayish olive green': [47, 51, 38],
    'Vivid yellowish green': [63, 215, 64],
    'Brilliant yellowish green': [135, 217, 137],
    'Strong yellowish green': [57, 150, 74],
    'Deep yellowish green': [23, 106, 30],
    'Very deep yellowish green': [5, 66, 8],
    'Very light yellowish green': [197, 237, 196],
    'Light yellowish green': [156, 198, 156],
    'Moderate yellowish green': [102, 144, 105],
    'Dark yellowish green': [47, 93, 58],
    'Very dark yellowish green': [16, 54, 26],
    'Vivid green': [35, 234, 165],
    'Brilliant green': [73, 208, 163],
    'Strong green': [21, 138, 102],
    'Deep green': [0, 84, 61],
    'Very light green': [166, 226, 202],
    'Light green': [111, 172, 149],
    'Moderate green': [51, 119, 98],
    'Dark green': [22, 78, 61],
    'Very dark green': [12, 46, 36],
    'Very pale green': [199, 217, 214],
    'Pale green': [148, 166, 163],
    'Grayish green': [97, 113, 110],
    'Dark grayish green': [57, 71, 70],
    'Blackish green': [31, 42, 42],
    'Greenish white': [224, 226, 229],
    'Light greenish gray': [186, 190, 193],
    'Greenish gray': [132, 136, 136],
    'Dark greenish gray': [84, 88, 88],
    'Greenish black': [33, 38, 38],
    'Vivid bluish green': [19, 252, 213],
    'Brilliant bluish green': [53, 215, 206],
    'Strong bluish green': [13, 143, 130],
    'Deep bluish green': [0, 68, 63],
    'Very light bluish green': [152, 225, 224],
    'Light bluish green': [95, 171, 171],
    'Moderate bluish green': [41, 122, 123],
    'Dark bluish green': [21, 75, 77],
    'Very dark bluish green': [10, 45, 46],
    'Vivid greenish blue': [0, 133, 161],
    'Brilliant greenish blue': [45, 188, 226],
    'Strong greenish blue': [19, 133, 175],
    'Deep greenish blue': [46, 132, 149], 
    'Very light greenish blue': [148, 214, 239],
    'Light greenish blue': [101, 168, 195],
    'Moderate greenish blue': [42, 118, 145],
    'Dark greenish blue': [19, 74, 96],
    'Very dark greenish blue': [11, 44, 59],
    'Vivid blue': [27, 92, 215],
    'Brilliant blue': [65, 157, 237],
    'Strong blue': [39, 108, 189],
    'Deep blue': [17, 48, 116],
    'Very light blue': [153, 198, 249],
    'Light blue': [115, 164, 220],
    'Moderate blue': [52, 104, 158],
    'Dark blue': [23, 52, 89],
    'Very pale blue': [194, 210, 236],
    'Pale blue': [145, 162, 187],
    'Grayish blue': [84, 104, 127],
    'Dark grayish blue': [50, 63, 78],
    'Blackish blue': [30, 37, 49],
    'Bluish white': [225, 225, 241],
    'Light bluish gray': [183, 184, 198],
    'Bluish gray': [131, 135, 147],
    'Dark bluish gray': [80, 84, 95],
    'Bluish black': [36, 39, 46],
    'Vivid purplish blue': [68, 54, 209],
    'Brilliant purplish blue': [128, 136, 226],
    'Strong purplish blue': [83, 89, 181],
    'Deep purplish blue': [42, 40, 111],
    'Very light purplish blue': [183, 192, 248],
    'Light purplish blue': [137, 145, 203],
    'Moderate purplish blue': [77, 78, 135],
    'Dark purplish blue': [34, 34, 72],
    'Very pale purplish blue': [197, 201, 240],
    'Pale purplish blue': [142, 146, 183],
    'Grayish purplish blue': [73, 77, 113],
    'Vivid violet': [121, 49, 211],
    'Brilliant violet': [152, 127, 220],
    'Strong violet': [97, 65, 156],
    'Deep violet': [60, 22, 104],
    'Very light violet': [201, 186, 248],
    'Light violet': [155, 140, 202],
    'Moderate violet': [92, 73, 133],
    'Dark violet': [52, 37, 77],
    'Very pale violet': [208, 198, 239],
    'Pale violet': [154, 144, 181],
    'Grayish violet': [88, 78, 114],
    'Vivid purple': [185, 53, 213],
    'Brilliant purple': [206, 140, 227],
    'Strong purple': [147, 82, 168],
    'Deep purple': [101, 34, 119],
    'Very deep purple': [70, 10, 85],
    'Very light purple': [228, 185, 243],
    'Light purple': [188, 147, 204],
    'Moderate purple': [135, 94, 150],
    'Dark purple': [86, 55, 98],
    'Very dark purple': [55, 27, 65],
    'Very pale purple': [224, 203, 235],
    'Pale purple': [173, 151, 179],
    'Grayish purple': [123, 102, 126],
    'Dark grayish purple': [81, 63, 81],
    'Blackish purple': [47, 34, 49],
    'Purplish white': [235, 223, 239],
    'Light purplish gray': [195, 183, 198],
    'Purplish gray': [143, 132, 144],
    'Dark purplish gray': [92, 82, 94],
    'Purplish black': [43, 38, 48],
    'Vivid reddish purple': [212, 41, 185],
    'Strong reddish purple': [167, 73, 148],
    'Deep reddish purple': [118, 26, 106],
    'Very deep reddish purple': [79, 9, 74],
    'Light reddish purple': [189, 128, 174],
    'Moderate reddish purple': [150, 88, 136],
    'Dark reddish purple': [95, 52, 88],
    'Very dark reddish purple': [63, 24, 60],
    'Pale reddish purple': [173, 137, 165],
    'Grayish reddish purple': [134, 98, 126],
    'Briliant purplish pink': [252, 161, 231],
    'Strong purplish pink': [244, 131, 205],
    'Deep purplish pink': [223, 106, 172],
    'Light purplish pink': [245, 178, 219],
    'Moderate purplish pink': [222, 152, 191],
    'Dark purplish pink': [198, 125, 157],
    'Pale purplish pink': [235, 200, 223],
    'Grayish purplish pink': [199, 163, 185],
    'Vivid purplish red': [221, 35, 136],
    'Strong purplish red': [184, 55, 115],
    'Deep purplish red': [136, 16, 85],
    'Very deep purplish red': [84, 6, 60],
    'Moderate purplish red': [171, 75, 116],
    'Dark purplish red': [110, 41, 76],
    'Very dark purplish red': [67, 20, 50],
    'Light grayish purplish red': [178, 135, 155],
    'Grayish purplish red': [148, 92, 115],
    'White': [231, 225, 233],
    'Light gray': [189, 183, 191],
    'Medium gray': [138, 132, 137],
    'Dark gray': [88, 84, 88],
    'Black': [43, 41, 43]
    }
    majority_lab_color = rgb2lab(np.uint8(np.asarray(rgb_majority)))
    diff_start = 100
    global val 
    for poss_color in COLORS.values():
        curr_color = rgb2lab(np.uint8(np.asarray(poss_color)))
        diff_real = deltaE_cie76(majority_lab_color, curr_color)
        #print(poss_color)
        if (diff_real < diff_start):
            diff_start = diff_real
            val = poss_color
    #print(val)
    return val, COLORS

def get_key(val, COLORS):
    global color 

    key_list = list(COLORS.keys()) 
    val_list = list(COLORS.values()) 

    color = key_list[val_list.index(val)]
    print('Majority color is: ' + color)
    return color



if __name__ == '__main__':
    image_path = '/Users/nicolasdecapite/Desktop/imDuplicates/blood_images/blood2.jpg'
    # 8 is for the amount of color clusters
    get_colors(get_image(image_path), 4, True)
    print(rgb_majority)
    match_image_by_color(rgb_majority)

    get_key(val, COLORS)