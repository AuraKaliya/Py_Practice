# 导入相关的模块和库
import cv2  # OpenCV库
import HandTrackingModule as htm  # 自定义手部检测模块
import os  # 操作系统模块
import numpy as np  # 数据处理模块

# 设置画笔图片文件夹路径
folderPath = r"D:\vscode\vsCodeFile\Py_Project\PainterImg"

# 获取画笔图片列表
mylist = os.listdir(folderPath)

# 定义一个空列表，用于存储画笔图片
overlayList = []

# 遍历所有画笔图片，将其存储在overlayList列表中
for imPath in mylist:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

# 初始化画笔参数
header = overlayList[0]  # 默认先使用第一种画笔
color = [255, 0, 0]  # 画笔颜色（蓝色）
brushThickness = 15  # 画笔粗细
eraserThickness = 40  # 橡皮擦粗细

# 初始化摄像头参数
cap = cv2.VideoCapture(0)  # 读取本地视频或者摄像头，这里设置读取编号为0的摄像头
cap.set(3, 1280)  # 设置摄像头画面的宽度和高度
cap.set(4, 720)

# 初始化手部检测器
detector = htm.handDetector()

# 初始化变量
xp, yp = 0, 0  # 上一次手指的坐标
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # 新建一个画板

# 开始循环读取摄像头视频流
while True:
    
    # 获取视频流
    success, img = cap.read()
    # 将图像水平翻转
    img = cv2.flip(img, 1)

    # 对图像进行手部检测，得到手部关键点的位置
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=True)

    # 如果当前视频帧中存在手部关键点，则执行下列代码
    if len(lmList) != 0:
        # 提取手指的两个关键点的坐标
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 判断当前手指状态，选择对应的画笔类型
        fingers = detector.fingersUp()
        if fingers[1] and fingers[2]:
            # 选择不同类型的画笔或橡皮擦
            if y1 < 153:
                if 0 < x1 < 320:
                    header = overlayList[0]
                    color = [50, 128, 250]  # 浅蓝色
                elif 320 < x1 < 640:
                    header = overlayList[1]
                    color = [0, 0, 255]  # 红色
                elif 640 < x1 < 960:
                    header = overlayList[2]
                    color = [0, 255, 0]  # 绿色
                elif 960 < x1 < 1280:
                    header = overlayList[3]
                    color = [0, 0, 0]  # 黑色
            # 将选择的画笔覆盖到图像上
            img[0:1280][0:153] = header

        # 判断手指状态是否为绘画状态，然后在画板上绘制线条
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if color == [0, 0, 0]:
                # 如果选择的颜色为黑色，则使用橡皮擦画出线条
                cv2.line(img, (xp, yp), (x1, y1), color, eraserThickness)  
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, eraserThickness)
            else:
                # 否则使用普通画笔绘制线条
                cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)   
                cv2.line(imgCanvas, (xp, yp), (x1, y1), color, brushThickness)

            # 更新上一次手指位置的坐标
            xp, yp = x1, y1

    # 实时显示画板上已经绘制的线条
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)
    img[0:1280][0:153] = header

    # 在屏幕上实时显示图像
    cv2.imshow("Image", img)
    cv2.waitKey(1)