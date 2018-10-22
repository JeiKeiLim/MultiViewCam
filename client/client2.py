#!/usr/bin/python
import socket
import cv2
import numpy
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

#연결할 서버(수신단)의 ip주소와 port번호
TCP_IP = '192.168.0.7'
TCP_PORT = 5001
CAM_WIDTH = 640
CAM_HEIGHT = 480

#송신을 위한 socket 준비
camera = PiCamera()
camera.resolution = (CAM_WIDTH, CAM_HEIGHT)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(CAM_WIDTH, CAM_HEIGHT))

time.sleep(0.1)

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))
print("Socket Connected")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#    sock = socket.socket()
#    sock.connect((TCP_IP, TCP_PORT))

    image = frame.array
    rawCapture.truncate(0)

    #추출한 이미지를 String 형태로 변환(인코딩)시키는 과정
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', image, encode_param)
    data = numpy.array(imgencode)
    #stringData = str(data)

#    decimg = cv2.imdecode(data,1)
#    cv2.imshow('CLIENT', decimg)
#    cv2.waitKey(1)

    #String 형태로 변환한 이미지를 socket을 통해서 전송
    sock.send( str(data.shape[0]).ljust(16).encode() );
    sock.send( data );
#    break

sock.close()

#다시 이미지로 디코딩해서 화면에 출력. 그리고 종료
decimg=cv2.imdecode(data,1)
cv2.imshow('CLIENT',decimg)
cv2.waitKey(0)
cv2.destroyAllWindows() 

