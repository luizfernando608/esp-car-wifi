#%%
import urllib.request
import cv2
import numpy as np
import time

from requests.api import post, request
from requests.sessions import session
import HandTrackingModule as htm
import requests

import aiohttp
import asyncio

url='http://192.168.0.107/cam-hi.jpg'

url_esp = "http://192.168.0.103"
#%%
def get_img_cam(url):
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img = cv2.rotate(img,cv2.cv2.ROTATE_90_CLOCKWISE)
    return img

async def send_comand(comand:str):
    # comand = "("http://192.168.0.103/+0/+0/9.0/5.0")"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(comand) as resp:
                print(resp)
        except:
            pass

def there_is_a_hand():
    if len(lmList) != 0:
        return True
    else:
        return False

def is_hand_closed():
    if not there_is_a_hand():
        return False
    fingers = []
    # 4 dedos
    for id in range(1,5):
        # Verificando se mão está fechada
        if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
            # Adicionando zero se o dedo estiver aberto
            fingers.append(0)
        else:
            # Adicionando um se o dedo estiver fechado
            fingers.append(1)
    if 1 in fingers:
        return True
    else:
        return False
        

# Criando o detector
detector = htm.handDetector(detectionCon=0.75)
# Índice dos pontos das mãos
tipIds = [4, #polegar
          8, #indicador 
          12, #meio
          16, #anelar
          20] #mindinho

ponto_central = 9

pTime = 0
old_get_command_motor = "/+2/+2/5.0/5.0"
get_command_motor = "/+2/+2/5.0/5.0"

hand_state_closed = False
old_hand_state_closed = False

img = get_img_cam(url)
img_dimension = np.array(img.shape[0:2])
center = np.array(img.shape[0:2])/2
servo_position = np.array([5.5,5.5])
old_servo_position = servo_position.copy()
get_command_servo = "/5.0/5.0"
#%%
while True:
    # Obtendo a imagem da câmera
    img = get_img_cam(url)
    # Adicionando imagem dos pontos das mãos
    img = detector.findHands(img)
    # Obtendo a posição de todos os pontos das mãos
    lmList = detector.findPosition(img, draw=False) 
    if is_hand_closed():
        get_command_motor = "/+5/+5"
        hand_state_closed = True
    else:
        get_command_motor = "/+0/+0"
        hand_state_closed = False

    if hand_state_closed != old_hand_state_closed:
        old_hand_state_closed = hand_state_closed
        # asyncio.run(send_comand(f"{url_esp}{get_command_motor}{get_command_servo}"))
    
    # cv2.line(img,[300,0],[300,800], (0, 255, 0))
    # cv2.line(img,[0,400],[600,400], (0, 255, 0))
    # cv2.circle(img,[300,400], radius=5, color=(255,0,0), thickness=5)
    if there_is_a_hand():
        # print(img_dimension)
        # poistion = ((lmList[9][1:]-center)/img_dimension)*10
        # print(poistion)
        # servo_position[0] += poistion[0]
        # servo_position[1] += poistion[1]
        # print(servo_position)
        # get_command_servo =  "/{:.1f}/{:.1f}".format(poistion[0], poistion[1])
        # print(get_command_servo)
        # print(poistion)
        # asyncio.run(send_comand(f"{url_esp}{get_command_motor}{get_command_servo}"))
        # print(old_servo_position-servo_position)
        pass
        
    # print(get_command_servo)
    

    cv2.imshow('test', img)
    if ord('q')==cv2.waitKey(10):
        exit(0)
