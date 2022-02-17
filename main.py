
import cv2
import numpy as np
from pip import main

def take_pic():

    while True:

        choice = input ('1) camera\n2) URL\nYour choice: ')
        if choice == '1':
            cam = cv2.VideoCapture(0)
            result, image = cam.read()
            # print(image)
            # print(result)
            cv2.imshow("GeeksForGeeks", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            return image

        elif choice == '2':

            """If you want to enter your address, leave the following two lines uncomment"""
            # url = input("print your url: ")
            # image = cv2.imread( url )
            """If you want to use the default address run next line"""
            image = cv2.imread( 'image.png' )
            
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            return image

        else:
            print('Your choice is incorrect')


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
    gray_img = cv2.cvtColor(img2 , cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray_img,(2,2))
   
    edges = cv2.Canny(blur,60,200)
    kernel = np.ones((4,4),np.uint8)
    dialted = cv2.dilate(edges , kernel , iterations= 2)



    # th3 = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 5 , 5)
    # th3 = 255 - th3
    # inv_edge = 255 - edges
    # erode = cv2.erode(edges,kernel,iterations = 1)


    # ret , th3 = cv2.threshold(edges, 0 , 255 , cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # _ , gray_img2 = cv2.threshold(th3 , 160 , 255 , cv2.THRESH_BINARY)

    contours , _ = cv2.findContours(dialted , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)

    max_area = 0
    max_contour= []

    for cont in contours:
        area = cv2.contourArea(cont)
        
        if area > max_area :
            max_area = area
            max_contour = cont
    
    epsilon = 0.1*cv2.arcLength(max_contour,True)
    aprox_contours = cv2.approxPolyDP( max_contour, epsilon , True)
    hull = cv2.convexHull(aprox_contours, _ , True, True)

    cv2.drawContours(image,[hull] , -1, (255,0,0), 3)
    cv2.imshow("image : ", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return hull.reshape((4,2))   # Changing the shape of the output convex hull

def distance(start_point , end_point):
    return ((((start_point[0] - end_point[0]) ** 2) + ((start_point[1] - end_point[1]) ** 2)) ** (1/2))

def transfer(starting_point , end_point , image): 
    
    arranged_end_point = []  
    
    for org_point in starting_point:
        min_distance = 1000000000
        min_point = []

        for dest_point in end_point:
            cur_distance = distance(dest_point , org_point)

            if cur_distance < min_distance:
                min_point = dest_point
                min_distance = cur_distance

        arranged_end_point.append(min_point)

    arranged_end_point = np.array(arranged_end_point)

    src = np.expand_dims(starting_point , axis= 0).astype(np.float32)
    dest = np.expand_dims(arranged_end_point , axis= 0).astype(np.float32)

    rows, cols, _ = image.shape
    M = cv2.getPerspectiveTransform( src, dest)
    # print(M)
    final_img = cv2.warpPerspective(image,M,(cols,rows))

    return final_img


def main(): 
    image = take_pic()
    # imread('image.png')
    st_point = starting_point(image)
    # print(st_point)
    cord =  cordinate(image)
    scanned_img = transfer(st_point , cord , image)

    cv2.imshow("image", scanned_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
