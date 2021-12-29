import cv2
import time
import numpy as np
import HandTrackingModule as htm
import pyautogui
import math

wCam, hCam = 1280, 720
wScr, hScr = pyautogui.size()
frameR = 100
xp,yp=0,0
cap = cv2.VideoCapture(0)
pTime = 0
smooth = 7
plocX, plocY = 0,0
clocX, clocY = 0,0
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam-frameR,hCam-2 *frameR),(255,0,255),2)
        if fingers[1]==1 and fingers[2] ==0:

            x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,hCam-2*frameR),(0,hScr))

            clocX = plocX + (x3-plocX)/smooth
            clocY = plocY + (y3-plocY)/smooth

            pyautogui.moveTo(clocX, clocY)
            cv2.circle(img,(x1,y1), 15, (255,0,255),cv2.FILLED)
            plocX,plocY = clocX, clocY
        if fingers[1]==1 and fingers[2] ==1:
            cx,cy = (x1+x2)//2, (y1+y2)//2

            cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1),(x2,y2),(255,0,255),3)
            cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

            length = math.hypot(x2-x1,y2-y1)
            print(length)
            if length<50:
                cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)
                pyautogui.click()


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
