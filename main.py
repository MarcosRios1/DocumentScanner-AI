import cv2
import numpy as np

widthImg = 640
heightImg = 480

cap = cv2.VideoCapture(0)
cap.set(3, widthImg)
cap.set(4, heightImg)
cap.set(10, 150) # brightness

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5,5), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThresh = cv2.erode(imgDial, kernel)

    return imgThresh

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 4000:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest

def getWarp(img, biggest):
    pts1 = np.float32([[111, 219], [287, 188], [154, 482], [352, 440]])
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    

while True:
    success, img = cap.read()
    cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThresh = preProcessing(img)
    biggest = getContours(imgThresh)
    print(biggest)
    getWarp(img, biggest)

    getContours(imgThresh)
    cv2.imshow('Video', imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

