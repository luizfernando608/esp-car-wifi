#%%
import cv2
import time
import os
import HandTrackingModule as htm

#%%
# Definindo dimensões da câmera
wCam, hCam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#%%
# Listando as imagens da pasta
folderPath = "images"
myList = os.listdir(folderPath)
print(myList)

# Iterando sob todas as imagens e salvando-as
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

pTime = 0

#%%
# Criando o detector
detector = htm.handDetector(detectionCon=0.75)
# Índice dos pontos das mãos
tipIds = [4, #polegar
          8, #indicador 
          12, #meio
          16, #anelar
          20] #mindinho

#%%
while True:
    # Capturando imagem da câmera
    success, img = cap.read()
    # A partir da imagem, desenhando os traços da mão
    img = detector.findHands(img)
    # Encontrando a posição da mão
    lmList = detector.findPosition(img, draw=False)
    totalFingers = 1
    if len(lmList) != 0:
        # No site do media_pipe é indicad o índice de cada ponto das mãos https://google.github.io/mediapipe/solutions/hands.html
        # Registrando os dedos que estão abertos
        fingers = []
        # Polegar
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 dedos
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)


    # Definindo que a imagem irá ficar no canto superior esquerdo
    h,w,c = overlayList[totalFingers].shape
    img[0:h,0:w] = overlayList[totalFingers]

    # Calculando o FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    # Exibindo na janela o FPS
    cv2.putText(img, 
                f'FPS: {int(fps)}', #Texto a ser exibido
                (400,70), #Posição do texto
                cv2.FONT_HERSHEY_PLAIN, #Font 
                3, #Tamanho da fonte
                (255,0,0), #Cor da fonte
                3) # "peso" da font

    # Mostrando imagem da câmera
    cv2.imshow("Image", img)
    # Opção para fechar a janela pressionar alguma tecla
    cv2.waitKey(1) 

