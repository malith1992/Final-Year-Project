import numpy as np
import cv2
import os


def createClahe(img):
    # Contrast Limited Adaptive Histogram Equalization
    # reduce the image information loss than global Histrogram equalization
    # image devide into small block and each block are histrogram equalized as usual
    # contrast limiting is applied for avoid noise amplified
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    c_img = clahe.apply(img)
    cv2.imshow('small',c_img)
    cv2.waitKey(0)
    return c_img


def smoothing(cImg):
    # para-1 = input image
    # para-2 = output image
    # para-3 = regulating filter strength; big value remove noise and img details
    # para-4 = Size in pixels of the template patch that is used to compute weights(7)
    # para-5 = Size in pixels of the window that is used to compute weighted average for given pixel(21)
    s_img1 = cv2.fastNlMeansDenoising(cImg, None, 10, 7, 21)
    s_img2 = cv2.medianBlur(s_img1, 3)
    return s_img2


def convertToBinary(smooth_img):

    ret, binary_img = cv2.threshold(smooth_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_img


def skewCorrection(binary_img):
    # find all x,y cordinates of text in image(binary_img) , 255 = white background
    coords = np.column_stack(np.where(binary_img < 255))
    # define rectangle for entire text and calculate minimum rotation angle of that rectangle
    # angle range [-90,0] and mesure inorder to clockwise
    # when angle come to 0 then recorrect it into -90
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        print("Angle < -45 = %d" % (angle))
        angle = -(90 + angle)

    else:
        print("Angle else = %d" % (angle))
        angle = -angle


    # find center x,y coordinate
    (h, w) = binary_img.shape[:2]
    center = (w // 2, h // 2)
    # give rotation angle and center cordinates get rotation matrix (M)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # do the rotation
    skiw_img = cv2.warpAffine(binary_img, M, (w, h),
                              flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # checking output image match with rotation angle
    cv2.putText(skiw_img, '', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
   # cv2.imshow('rect1', skiw_img)
    return skiw_img


def main():
    img = cv2.imread('107.jpg', 0)
    c_img = createClahe(img)
    #smooth_img = smoothing(c_img)
    binary_img = convertToBinary(c_img)
    skiw_img = skewCorrection(binary_img)
    #return skiw_img

    #line_img_no = lineSegmantation(skiw_img)

    cv2.imwrite('skewCorrect.jpg',skiw_img)
    cv2.imshow('original.jpg', img)
    cv2.waitKey(0)

main()


cv2.destroyAllWindows()