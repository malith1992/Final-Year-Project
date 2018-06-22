import cv2
import numpy as np
import os
import glob

myDataList = []

class Data:
    def __init__(self, pageNo, lineNo, status, image):
        self.pageNo = pageNo
        self.lineNo = lineNo
        self.status = status
        self.image = image


    def __str__(self):
        return self


def lineseperate(image_list):
    for page, img in enumerate(image_list):
        page = page+1
        line = 0
        #print(page, img.replace("\\", "/"))
        large = cv2.imread(img.replace("\\", "/"))
        rgb = large
        #print('rgb shape ',rgb.shape)
        small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

        _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 6))
        connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

        # using RETR_EXTERNAL instead of RETR_CCOMP
        image, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        mask = np.zeros(bw.shape, dtype=np.uint8)
        contours = list(reversed(contours))

        for idx in range(len(contours)):

            x, y, w, h = cv2.boundingRect(contours[idx])
            mask[y:y + h, x:x + w] = 0
            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
            r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)
            if r > 0.45 and w > 20 and h > 8:
                rgb = cv2.rectangle(rgb, (x, y), (x + w - 1, y + h - 1), (0, 0, 255), 1)
                roi = small[y:y + h, x:x + w]
                cv2.imshow('rec', rgb)
                cv2.waitKey(0)

                if h > 8 and h < 30:


                    status = ''
                    #print('img shape ', roi.shape)
                    data = Data(page, line, status, roi)
                    myDataList.append(data)


                if h > 30:
                    #print('line no into paraseperate ',line)
                    line_no = paraseperate(roi,page,line)
                    line = line_no


            line = line + 1

        #cv2.imshow('contours', roi)
        #cv2.waitKey(0)

    for elements in myDataList:
        name = "page_%d_line_%d_%s.jpg" % (elements.pageNo, elements.lineNo, elements.status)
        path = 'C:/Users/Malith/PycharmProjects/untitled/output'
        cv2.imwrite(os.path.join(path, name), elements.image)
    print("Seperation completed")
    os.startfile(path)

def paraseperate(img,page,line):

    small1 = img
    rgb1 = img
    #smallph = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small1, cv2.MORPH_GRADIENT, kernel)

    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    # using RETR_EXTERNAL instead of RETR_CCOMP
    image, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(bw.shape, dtype=np.uint8)
    contours = list(reversed(contours))
    #cv2.imshow('roi w', img)
    #cv2.waitKey(0)
    length = len(contours)
    for idx in range(len(contours)):

        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y + h, x:x + w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y + h, x:x + w])) / (w * h)
        if r > 0.45 and w > 20 and h > 8:
            status = ''
            rgb1 = cv2.rectangle(rgb1, (x, y), (x + w - 1, y + h - 1), (255, 255, 255), 0)
            roi1 = small1[y:y + h, x:x + w]
            if idx == 0:
                status = 'P'

            if idx == length :
                status = '<closeP'

            data = Data(page, line, status, roi1)
            myDataList.append(data)
            line = line + 1

    #cv2.imshow('contours3', img)
    #cv2.waitKey(0)
    #print('line no pass',line)
    return line



def main(folder):
    image_list = (glob.glob(folder + "/*.jpg"))
    #print(image_list)
    lineseperate(image_list)

