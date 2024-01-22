import cv2
import numpy as np
import math
import os
from comtypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import mediapipe as mp

# สร้าง object สำหรับการตรวจจับมือ
class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon / 2)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lmList

# กำหนดขนาดของหน้าจอ
wCam, hCam = 640, 480

# สร้าง object สำหรับการตรวจจับมือ
detector = HandDetector()

# เปิดกล้อง
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# กำหนดระดับเสียง
minVol, maxVol = -65.0, 0.0
vol = 0
volBar = 400
volPer = 0

# ระดับเสียงเริ่มต้น
volume = cast(AudioUtilities.GetSpeakers().ActiveEndpoint.QueryInterface(IAudioEndpointVolume), POINTER(IAudioEndpointVolume))
volume.SetMasterVolumeLevel(vol, None)

print('Program is Ready')

while True:
    success, img = cap.read()

    # ตรวจจับมือและหาตำแหน่ง
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # แสดงผลลัพธ์
    cv2.imshow("Hand Tracking", img)

    # หยุดโปรแกรมเมื่อกด 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดกล้องและปิดหน้าต่าง
cap.release()
cv2.destroyAllWindows()
