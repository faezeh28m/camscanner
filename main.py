from email.mime import image
from itertools import count
import this
from tracemalloc import start
from typing import Counter
import cv2
from cv2 import imshow
from cv2 import destroyAllWindows
from cv2 import imread
from cv2 import THRESH_BINARY
from cv2 import THRESH_BINARY_INV
from cv2 import threshold
from cv2 import Canny
import numpy as np
from pip import main

def take_pic():
    # while True:

        choice = input ('1) camera\n2) URL\nYour choice: ')
        if choice == '1':
            cam = cv2.VideoCapture(0)
            result, image = cam.read()
            # print(image)
            # print(result)
            cv2.imshow("GeeksForGeeks", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # break

        elif choice == '2':
            url = input('enter URL (exampale: C:\\Users\\faezeh\\Desktop\\imagename.jpg) : ')
            image = cv2.imread( url )
            # print(image)
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # break

        # else:
        #     print('Your choice is incorrect')

        return image

def cordinate(image):
    y = image.shape[0]
    x = image.shape[1]
    corner1 = [0 , y]
    corner2 = [x , y]
    corner3 = [0 , 0]
    corner4 = [x , 0]

    return corner1 , corner2 , corner3 , corner4

def starting_point(image):
    img2 = image.copy()
    # img2 = 255 - image
    gray_img = cv2.cvtColor(img2 , cv2.COLOR_BGR2GRAY)
    # blur = cv2.blur(gray_img,(1,2))
   
    edges = cv2.Canny(gray_img,60,200)
    th3 = cv2.adaptiveThreshold(edges,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 5 , 5)
    # ret , th3 = cv2.threshold(edges, 0 , 255 , cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # kernel = np.ones((4,4),np.uint8)
    # dilation = cv2.erode(th3,kernel,iterations = 1)
    # _ , gray_img2 = cv2.threshold(th3 , 160 , 255 , cv2.THRESH_BINARY)

    contours , _ = cv2.findContours(th3 , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)
    # print(len(contours))
    
    my_contour = contours[0]
    count = len(contours)
    #choice biggest contour as my_countour for perspective
    for i in range(count - 1):
        if(cv2.contourArea(contours[i])) < (cv2.contourArea(contours [i+1])):
            my_contour = contours[i+1]

    
    area = cv2.approxPolyDP( my_contour, len(my_contour)*0.1, True) 
    
    hull = cv2.convexHull(area, _ , True, True)
    # cv2.drawContours(image, [my_contour], -1, (255,0,0), 3)
     
    cv2.imshow("image : ", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return hull

def distance(start_point , end_point):
    return ((((start_point[0] - end_point[0]) ** 2) + ((start_point[1] - end_point[1]) ** 2)) ** (1/2))

def transfer(starting_point , end_point , image): 
    arranged_starting_point = []  
    for i in range(4):
        end = end_point[i]
        for j in range(3):
            start = starting_point[0]
            print('start: ' , start , 'end = ',end)
            if(distance(starting_point[j],end_point[i])) < (distance(starting_point[j+1],end_point[i])):
                start = starting_point[j]

            arranged_starting_point.append(start)

    rows,cols,_=image.shape
    M=cv2.getPerspectiveTransform(starting_point,end_point)
    dst=cv2.warpPerspective(image,M,(cols,rows))

    return dst


def main(): 
    image = take_pic()
    # imread('image.png')
    scanned_img = transfer(starting_point(image) , cordinate(image) , image)

    cv2.imshow("image", scanned_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    starting_point(image)

# take_pic()


# cordinate(image)

main()
