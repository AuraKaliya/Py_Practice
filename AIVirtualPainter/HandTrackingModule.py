import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(self.detectionCon), int(self.trackCon))
        self.mpDraw = mp.solutions.drawing_utils
        #手指末端关键点索引的列表
        self.tipIds = [4, 8, 12, 16, 20]

#找到手并返回带有骨架和关键点信息的图像
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        print(self.results.multi_handedness)  # 获取检测结果中的左右手标签并打印

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #绘制关键点和骨架信息，传入参数为图-手部关键点信息列表-预定义连接点
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

#找到关键点并返回点的坐标（列表）
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)
        return self.lmList

#手指屈伸情况
#坐标列表和索引列表从0开始，坐标值在图像y轴上递增
#若相邻俩索引对应点坐标的大小情况相同，则是伸手指，若相反则是弯曲手指
#由于手指列表的索引，该方法适用于右手
    def fingersUp(self):
        #存储列表
        fingers = []
        # 大拇指
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 其余手指
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

#用于计算两个指尖的距离
#传入参数为俩指尖的索引
    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)        # 检测手势并画上骨架信息

        lmList = detector.findPosition(img)  # 获取得到坐标点的列表
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        print(cap.get(cv2.CAP_PROP_FPS))    
        cv2.putText(img, 'fps:' + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
