#%%
import urllib.request
import cv2
import numpy as np
import time
import HandTrackingModule as htm
import requests

url='http://192.168.0.105/cam-hi.jpg'

url_esp = "http://192.168.0.103"

#%%
def avg_circles(circles, b):
    avg_x=0
    avg_y=0
    avg_r=0
    for i in range(b):
        avg_x = avg_x + circles[0][i][0]
        avg_y = avg_y + circles[0][i][1]
        avg_r = avg_r + circles[0][i][2]
    avg_x = int(avg_x/(b))
    avg_y = int(avg_y/(b))
    avg_r = int(avg_r/(b))
    return avg_x, avg_y, avg_r

def dist_2_pts(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def take_measure(threshold_img, threshold_ln, minLineLength, maxLineGap, diff1LowerBound, diff1UpperBound, diff2LowerBound, diff2UpperBound):
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img2=cv2.imdecode(imgNp,-1)

    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20)

    if circles is not None:
        a, b, c = circles.shape
        x,y,r = avg_circles(circles, b)
        
        #Draw center and circle
        cv2.circle(img, (x, y), r, (0, 255, 0), 3, cv2.LINE_AA)  # draw circle
        cv2.circle(img, (x, y), 2, (0, 255, 0), 3, cv2.LINE_AA)  # draw center of circle
        
        separation = 10.0 #in degrees
        interval = int(360 / separation)
        p1 = np.zeros((interval,2))  #set empty arrays
        p2 = np.zeros((interval,2))
        p_text = np.zeros((interval,2))
        for i in range(0,interval):
            for j in range(0,2):
                if (j%2==0):
                    p1[i][j] = x + 0.9 * r * np.cos(separation * i * 3.14 / 180) #point for lines
                else:
                    p1[i][j] = y + 0.9 * r * np.sin(separation * i * 3.14 / 180)
        text_offset_x = 10
        text_offset_y = 5
        for i in range(0, interval):
            for j in range(0, 2):
                if (j % 2 == 0):
                    p2[i][j] = x + r * np.cos(separation * i * 3.14 / 180)
                    p_text[i][j] = x - text_offset_x + 1.2 * r * np.cos((separation) * (i+9) * 3.14 / 180) #point for text labels, i+9 rotates the labels by 90 degrees
                else:
                    p2[i][j] = y + r * np.sin(separation * i * 3.14 / 180)
                    p_text[i][j] = y + text_offset_y + 1.2* r * np.sin((separation) * (i+9) * 3.14 / 180)  # point for text labels, i+9 rotates the labels by 90 degrees

        #Lines and labels
        for i in range(0,interval):
            cv2.line(img, (int(p1[i][0]), int(p1[i][1])), (int(p2[i][0]), int(p2[i][1])),(0, 255, 0), 2)
            cv2.putText(img, '%s' %(int(i*separation)), (int(p_text[i][0]), int(p_text[i][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,0,0),1,cv2.LINE_AA)

        cv2.putText(img, "Gauge OK!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,255,0),2,cv2.LINE_AA)
        
        gray3 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        maxValue = 255
        
        # Threshold image to take better measurements
        th, dst2 = cv2.threshold(gray3, threshold_img, maxValue, cv2.THRESH_BINARY_INV);

        in_loop = 0
        lines = cv2.HoughLinesP(image=dst2, rho=3, theta=np.pi / 180, threshold=threshold_ln, minLineLength=minLineLength, maxLineGap=maxLineGap)
        final_line_list = []
        
        for i in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[i]:
                diff1 = dist_2_pts(x, y, x1, y1)  # x, y is center of circle
                diff2 = dist_2_pts(x, y, x2, y2)  # x, y is center of circle

                if (diff1 > diff2):
                    temp = diff1
                    diff1 = diff2
                    diff2 = temp
                    
                # Check if line is in range of circle
                if (((diff1<diff1UpperBound*r) and (diff1>diff1LowerBound*r) and (diff2<diff2UpperBound*r)) and (diff2>diff2LowerBound*r)):
                    line_length = dist_2_pts(x1, y1, x2, y2)
                    final_line_list.append([x1, y1, x2, y2])
                    in_loop = 1

        if (in_loop == 1):
            x1 = final_line_list[0][0]
            y1 = final_line_list[0][1]
            x2 = final_line_list[0][2]
            y2 = final_line_list[0][3]
            cv2.line(img2, (x1, y1), (x2, y2), (0, 255, 255), 2)
            dist_pt_0 = dist_2_pts(x, y, x1, y1)
            dist_pt_1 = dist_2_pts(x, y, x2, y2)
            if (dist_pt_0 > dist_pt_1):
                x_angle = x1 - x
                y_angle = y - y1
            else:
                x_angle = x2 - x
                y_angle = y - y2
                
            # Finding angle using the arc tan of y/x
            res = np.arctan(np.divide(float(y_angle), float(x_angle)))

            #Converting to degrees
            res = np.rad2deg(res)
            if x_angle > 0 and y_angle > 0:  #in quadrant I
                final_angle = 270 - res
            if x_angle < 0 and y_angle > 0:  #in quadrant II
                final_angle = 90 - res
            if x_angle < 0 and y_angle < 0:  #in quadrant III
                final_angle = 90 - res
            if x_angle > 0 and y_angle < 0:  #in quadrant IV
                final_angle = 270 - res

            cv2.putText(img2, "Indicator OK!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,255,0),2,cv2.LINE_AA)
            print ("Final Angle: ", final_angle)
        else:
            cv2.putText(img2, "Can't find the indicator!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,0,255),2,cv2.LINE_AA)
            
    else:
        cv2.putText(img, "Can't see the gauge!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,0,255),2,cv2.LINE_AA)
    return img, img2


#%%
def get_img_cam(url):
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img = cv2.rotate(img,cv2.cv2.ROTATE_90_CLOCKWISE)
    return img

# Criando o detector
detector = htm.handDetector(detectionCon=0.75)
# Índice dos pontos das mãos
tipIds = [4, #polegar
          8, #indicador 
          12, #meio
          16, #anelar
          20] #mindinho

pTime = 0

while True:
    
    img = get_img_cam(url)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    totalFingers = 1

    if len(lmList) != 0:
        # No site do media_pipe é indicad o índice de cada ponto das mãos https://google.github.io/mediapipe/solutions/hands.html
        # Registrando os dedos que estão abertos
        fingers = []
        # Polegar
        # if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)

        # 4 dedos
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(0)
            else:
                # Contando o numero de dedo baixados
                fingers.append(1)
    
        # print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)
    
    # print(lmList)
        old_motor_state = ""
        if 1 in fingers:
            motor_state = "back_AB"
        else:
            # print("Parei")
            motor_state = "CLOSE"
    
        if old_motor_state != motor_state:
            print("Novo estado")
            try:
                requests.get(f"{url_esp}/{motor_state}")
                print(motor_state)
                
            except:
                pass
            
            old_motor_state = motor_state
        else:
            print("Mesmo estado")

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

    cv2.imshow('test', img)

    if ord('q')==cv2.waitKey(10):
        exit(0)