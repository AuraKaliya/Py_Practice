# 《AIVirtualPainter》项目介绍

​		本项目是一个实训项目，是一个基于Python的OpenCV库和MediaPipe 库的学习和使用。以下将分为两节分别介绍程序执行流程和技术点。

## 程序流程

本项目共有两个代码文件，AiVirtualPainter.py负责构建虚拟画板和根据识别的手势执行画笔切换、绘制、消除等操作；HandTrackingModule.py描述了一个关于手的类handDetector，在该类中使用cv2提供的函数编写出找到手并返回骨架信息、坐标列表图像的方法，同时根据坐标点在摄像捕获图的位置关系判断手指屈伸情况。

## 技术点



* 通过while True循环读取摄像头视频流并实时更新画板，通过waitKey(1)达到持续显示捕获图像的功能。

* 通过cv2.bitwise_and将画板和线条共同显示，通过cv2.bitwise_or模拟橡皮擦进行擦除，（橡皮擦数值调整为255黑色），在循环内进行线路更新。

* 

* 一些语法解释：

    ```python
    cap = cv2.VideoCapture(0)  # 读取本地视频或者摄像头，这里设置读取编号为0的摄像头
    cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED) #作圆填充
    ```

    