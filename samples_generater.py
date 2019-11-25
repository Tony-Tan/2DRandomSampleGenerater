"""
This is a tool for generating 2-D random samples for different class, what users should do is:
more detials can be found: https://brainbomb.org/
1. draw class in picture with different colors
2. each class should be represented by a closed sharp(line width should less than 3 pixels))
3. input image should be of the format '.png'
4. output csv file has the same name with the input and the same path
6. can only deal with at most 100 inputs, and reboot the script will restart
"""
import cv2
import numpy as np
import copy
import random
import csv
from sty import  fg


def colors_kinds_detect(image):
    """
    :param image: origin image
    :return: color dictionary that contain all kinds of class color
    """
    color_dic = {}
    height,width,_=np.shape(image)
    for j in range(height):
        for i in range(width):
            if image[j,i][0] == 255 and image[j,i][1] == 255 and image[j,i][2] == 255:
                continue
            if str(image[j,i]) not in color_dic.keys():
                color_dic[str(image[j,i])] = image[j,i]
    return color_dic


def split_color(image,color):
    """
    :param image: origin image
    :param color: which color should be segment from origin image
    :return: the available points from which the samples could be sampled
    """
    height, width, _ = np.shape(image)
    image_ = copy.deepcopy(image)
    image_binary = np.zeros([height, width], np.uint8)
    available_sample_points=[]
    for j in range(height):
        for i in range(width):
            if image_[j, i][0] == color[0] and image_[j, i][1] == color[1] and image_[j, i][2] == color[2]:
                image_binary[j,i]=255
            else:
                image_binary[j, i]=0
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    image_binary = cv2.dilate(image_binary,kernel,iterations=2)
    for j in range(height):
        for i in range(width):
            if image_binary[j, i] == 255:
                image_[j,i] = color
            else:
                image_[j,i] =[255,255,255]
    mask = np.zeros([height + 2, width + 2], np.uint8)
    cv2.floodFill(image_,mask,(0,0),(0,0,0))
    for j in range(height):
        for i in range(width):
            if image_[j, i][0] == 255 and image_[j, i][1] == 255 and image_[j, i][2] == 255:
                available_sample_points.append((j,i))
    return available_sample_points


def generate_samples(available_sample_points,sample_size):
    """
    :param available_sample_points:  the available points from which the samples could be sampled
    :param sample_size: how many samples are needed
    :return: samples
    """
    samples=[]
    for i in range(sample_size):
        samples.append(random.choice(available_sample_points))
    return samples


# main loop of the script
for loop in range(100):
    image_path = input('Samples map image(default:./1.png,q for quit):')
    print('result is stored in the same path with the map image and the same name(.csv)')
    if image_path == 'q':
        break
    if image_path == '':
        image_path = './1.png'
    image = cv2.imread(image_path,1)
    if image is None:
        print('Samples map image have not been found!')
        continue
    height, width, _ = np.shape(image)
    color_dic = colors_kinds_detect(image)
    print(str(len(color_dic.keys()))+ ' kind(s) of color had been detected:')
    i = 1
    image_dst = copy.deepcopy(image)
    samples_file = open(image_path.replace('png','csv'),'w+')
    csv_write = csv.writer(samples_file)
    csv_write.writerow(['x_1','x_2','Label'])
    for key in color_dic.keys():
        # print rgb color in terminal some terminal app may fail.
        print(fg(color_dic[key][2],color_dic[key][1],color_dic[key][0]) + str(color_dic[key]) + ' has been detected!' + fg.rs)
        available_sample_points = split_color(image,color_dic[key])
        sample_num = input('How many samples in this class do you want: ')
        samples = generate_samples(available_sample_points,int(sample_num))
        for sample in samples:
            csv_write.writerow([sample[1],height-sample[0],i])
        i += 1
    samples_file.close()
print('Good luck')
