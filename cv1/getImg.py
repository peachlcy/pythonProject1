import numpy as np
import cv2 as cv
import os
import shutil

# 全局变量
EXTRACT_FOLDER = 'test'  # 存放帧图片的位置
EXTRACT_FREQUENCY = 10  # 帧提取频率


def extract_frames(dst_folder, index):
    # 实例化视频对象
    video = cv.VideoCapture("prac1-flap_test_video.mp4")
    frame_count = 0

    # 循环遍历视频中的所有帧
    while True:
        # 逐帧读取
        _, frame = video.read()
        if frame is None:
            break
        # 按照设置的频率保存图片
        if frame_count % EXTRACT_FREQUENCY == 0:
            # 设置保存文件名
            save_path = "{}/{:>03d}.jpg".format(dst_folder, index)
            # 保存图片
            cv.imwrite(save_path, frame)
            index += 1  # 保存图片数＋1
        frame_count += 1  # 读取视频帧数＋1

    # 视频总帧数
    print(f'the number of frames: {frame_count}')
    # 打印出所提取图片的总数
    print("Totally save {:d} imgs".format(index - 1))

    video.release()


def testImg(path):
    img = cv.imread("/Users/peach/PycharmProjects/pythonProject1/cv1/test/" + path, 0)
    obj = img[700:900, 1300:1600]
    img_blur = cv.GaussianBlur(obj, (3, 3), 0)
    edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)
    lines = cv.HoughLinesP(edges, 1, 1.0 * np.pi / 180, 120, minLineLength=10, maxLineGap=5)
    if lines is not None:
        for (x1, y1, x2, y2) in lines[:, 0]:
            k = (y1 - y2) / (x1 - x2)
            # print(x1, y1, ";", x2, y2)
            # print(k)
            # cv.line(obj, (x1, y1), (x2, y2), (0, 0, 255), 3)  # 画直线
            if k > -1:
                return k
    # cv.imshow("detection", obj)

    # cv.imshow('Canny Edge Detection', edges)
    # cv.waitKey(0）


def edgeImg():
    i = 0
    p = os.listdir('test')
    p.sort()
    k = []
    while i < 186:
        k.append(testImg(p[i]))
        i = i + 1
    j = 1
    while j < 186:
        img = cv.imread("/Users/peach/PycharmProjects/pythonProject1/cv1/test/" + p[j], 0)
        if abs(k[j] - k[j - 1]) > 0.015:
            txt = "move"
            imgmove = cv.putText(img, txt, (int(700), int(700)), cv.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 2)
            save_path = "{}/{:>03d}.jpg".format('fin', j)
            cv.imwrite(save_path, imgmove)
        else:
            save_path = "{}/{:>03d}.jpg".format('fin', j)
            cv.imwrite(save_path, img)
        j = j + 1




def main():
    # 递归删除之前存放帧图片的文件夹，并新建一个
    try:
        shutil.rmtree(EXTRACT_FOLDER)
    except OSError:
        pass
    os.mkdir(EXTRACT_FOLDER)
    # 抽取帧图片，并保存到指定路径
    extract_frames(EXTRACT_FOLDER, 1)
    edgeImg()


if __name__ == '__main__':
    main()
