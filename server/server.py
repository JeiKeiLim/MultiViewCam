#!/usr/bin/python
import socket
import cv2
import numpy
import time
import threading
from matplotlib import pyplot as plt

# Global Variable
image_left = numpy.zeros((480, 640, 3), dtype='uint8')
image_right = numpy.zeros((480, 640, 3), dtype='uint8')

#socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def getFrame(conn, idx=1):
	while(True):
		global image_left
		global image_right
		#String형의 이미지를 수신받아서 이미지로 변환 하고 화면에 출력
		length = recvall(conn, 16)
		while(length is None):
			length = recvall(conn, 16)

		stringData = recvall(conn, int(length))
		data = numpy.fromstring(stringData, dtype='uint8')
		#s.close()
		decimg=cv2.imdecode(data,1)
		if idx == 1:
			image_left = decimg
		else:
			image_right = decimg
	#	image_combined = numpy.concatenate((image_left, image_right), axis=1)
	#	print(idx, end="")

	#	cv2.imshow("SERVER" + str(idx),image_combined)
	#	in_key = cv2.waitKey(1)
	#	if(in_key == 'q'):
	#		break

#수신에 사용될 내 ip와 내 port번호
TCP_IP = ''
TCP_PORT1 = 5001
TCP_PORT2 = 5002

#TCP소켓 열고 수신 대기
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((TCP_IP, TCP_PORT1))
s1.listen(True)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((TCP_IP, TCP_PORT2))
s2.listen(True)

print("Waiting for connection 1")
conn1, addr1 = s1.accept()
print("Waiting for connection 2")
conn2, addr2 = s2.accept()

print("All Connected!")

t1 = threading.Thread(target=getFrame, args=(conn1, 1))
t1.start()

t2 = threading.Thread(target=getFrame, args=(conn2, 2))
t2.start()

while(True):
	image_combined = numpy.concatenate((image_left, image_right), axis=1)
	cv2.imshow("SERVER",image_combined)
	in_key = cv2.waitKey(1)
	if(in_key == 'q'):
		break

t1.join()
t2.join()

s1.close()
s2.close()
