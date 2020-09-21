# !/usr/bin/python3
# -*- coding:utf-8 -*- 
# author: Ming Luo
# time: 2020/9/18 10:24

import cv2
from PIL import Image

data = cv2.imread("00.jpg")
a = cv2.resize(data, (319, 449))
image = Image.fromarray(cv2.cvtColor(a, cv2.COLOR_BGR2RGB))
image.save('result.jpg', dpi=(350.0, 350.0))

img = Image.open('00.jpg')




