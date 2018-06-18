import cv2
import numpy as np

large = cv2.imread('skewcorreect.jpg')
rgb = large
small1 = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
small = cv2.medianBlur(small1,5)
cv2.imshow('rects2',small )
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

_, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#ret, = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
#cv2.imshow('rect0', connected)

_ , contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


mask = np.zeros(bw.shape, dtype=np.uint8)
for idx in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[idx])
    mask[y:y+h, x:x+w] = 0
    new = cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
    #print(mask)

    #cv2.imshow('rect1', new)
    r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

    if r > 0.45 and w > 8 and h > 8:
        rgb = cv2.rectangle(rgb, (x, y), (x+w-1, y+h-1), (0, 0, 255), 1)

cv2.imshow('rects',rgb )
cv2.waitKey(0)
cv2.destroyAllWindows()