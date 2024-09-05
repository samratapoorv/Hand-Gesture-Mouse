import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui

frameR = 100
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr,hScr = autopy.screen.size()
while True:
    # 1 find hand land mark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if(len(lmList))!=0:
        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        #print(x1,x2,y1,y2)
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (640 - frameR, 480 - frameR), (255, 0, 0), 2)
        if fingers[1]==1 and fingers[2]==0:
            x3 = np.interp(x1,(frameR,640-frameR),(0,wScr))
            y3 = np.interp(y1,(frameR,480-frameR),(0,hScr))
            clocX = plocX + (x3-plocX)/smoothening
            clocY = plocY + (y3-plocY)/smoothening
            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
            plocX , plocY= clocX, clocY

        if fingers[1]==1 and fingers[2]==1:
            length, img, lineinfo = detector.findDistance(8,12,img)
            # print(length)
            if length<40:
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,255),cv2.FILLED)
                autopy.mouse.click()
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
            pyautogui.scroll(10)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)












