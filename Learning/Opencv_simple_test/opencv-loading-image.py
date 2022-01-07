import cv2
import numpy as np
#Carregando uma imagem no opencv
img = cv2.imread("download.png", cv2.IMREAD_COLOR)
cv2.namedWindow("Hello World")
cv2.imshow("Hello World", img)
cv2.waitKey()

 