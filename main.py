import cv2
import threading
import RPi.GPIO as GPIO
import time
#import motor

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
LED = 27
GPIO.setup(LED, GPIO.OUT)


thres = 0.45 # Threshold to detect object

SCREEN_WIDTH = 1280#320
SCREEN_HEIGHT = 720# 240


cap = cv2.VideoCapture(0)
cap.set(3,SCREEN_WIDTH)
cap.set(4,SCREEN_HEIGHT)
cap.set(10,70)

classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
escapeCheck = 0

classIds = []
confs = None
bbox = None

midPoint = [SCREEN_WIDTH/2 - 1.5, SCREEN_HEIGHT/2 - 1.5, 1.5, 1.5]

detected = False
detectFlag = False
positioned = False



#=====LED BLINK=====
def ledBlink():
    global positioned
    while(positioned):
        GPIO.output(LED, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(LED, GPIO.LOW)
        time.sleep(0.25)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(0.25)

#ledThread = threading.Thread(target=ledBlink)
#ledThread.start()

#def motorPos(x, y):
#    motor.position(x, y) #motor position

#posThread = threading.Thread(target=motorPos, args=(0,0))

while escapeCheck != 27:
    success,img = cap.read()
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    
    #print(classIds,bbox)
    if detectFlag == False:
        #motor.set_loop_search(1) #motor search on
        detectFlag = True
        positioned = False
        #motor.reseting() #motor reset
        #motor.search() #motor searching

    cv2.rectangle(img,midPoint,color=(0,125,125),thickness=3)

    if len(classIds) != 0:
        #motor.set_loop_search(0) #motor search off
        targetId = None
        targetConf = None
        targetBox = [0, 0, 0, 0]

        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            if classId == 1:
                #print(bbox)
                if targetBox[2]*targetBox[3] < box[2]*box[3]:
                    targetId = classId
                    targetConf = confidence
                    targetBox = box

        if targetId != None:
            cv2.rectangle(img,targetBox,color=(0,255,0),thickness=2)
                
            aimPoint = targetBox 
            aimPoint[0] = targetBox[0] + targetBox[2]/2 - 2.5 
            aimPoint[1] = targetBox[1] + targetBox[3]/2 - 2.5 
            aimPoint[2] = 5                       
            aimPoint[3] = 5                      

            cv2.rectangle(img,aimPoint,color=(0,0,255),thickness=3)
            print('x: ' + str(aimPoint[0] - SCREEN_WIDTH/2) + ' y: ' + str(aimPoint[1] - SCREEN_HEIGHT/2))
            #motor.position(aimPoint[0] - SCREEN_WIDTH/2, aimPoint[1] - SCREEN_HEIGHT/2) #motor position
            #posThread = threading.Thread(target=motorPos, args=(aimPoint[0] - SCREEN_WIDTH/2, aimPoint[1] - SCREEN_HEIGHT/2))
            #posThread.start()
            positioned = True

    elif positioned == True:
        detectFlag = False
    
    if positioned == True:
        GPIO.output(LED, GPIO.HIGH)
        print('YES')
    elif positioned == False:
        GPIO.output(LED, GPIO.LOW)
        print('NO')

    img = cv2.flip(img, 0)
    cv2.imshow("Output",img)
    escapeCheck = cv2.waitKey(1)
GPIO.cleanup()
