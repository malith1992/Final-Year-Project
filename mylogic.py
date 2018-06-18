import cv2
import numpy as np
import os
import glob


class Data :
    def __init__(self, pageNo , lineNo, image):
        self.pageNo = pageNo
        self.lineNo = lineNo
        self.image = image

    def __str__(self):
        return self


def lineseperate(image_list):
    myDataList = []
    for page,img in enumerate(image_list):
        print (page,img.replace("\\","/"))
        large = cv2.imread(img.replace("\\","/"))
        rgb = large
        small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

        _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
        connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

        # using RETR_EXTERNAL instead of RETR_CCOMP
        image, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        mask = np.zeros(bw.shape, dtype=np.uint8)
        contours= list(reversed(contours))

        for idx in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[idx])
            mask[y:y+h, x:x+w] = 0
            cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
            r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
            if r > 0.45 and w > 20 and h > 8:
                rgb = cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 0, 255), 1)
                roi = small[y:y + h, x:x + w]
                data = Data(page,idx,roi)
                myDataList.append(data)


        cv2.imshow('contours', rgb)
        cv2.waitKey(0)



    for elements in myDataList:
        name = "box%d_%d.jpg" % (elements.pageNo, elements.lineNo)
        path = 'C:/Users/Malith/PycharmProjects/untitled/output'
        cv2.imwrite(os.path.join(path, name), elements.image)
    print("Seperation completed")

def main():
    image_list = (glob.glob("C:/Users/Malith/PycharmProjects/untitled/bulk/*.jpg"))
    lineseperate(image_list)

main()