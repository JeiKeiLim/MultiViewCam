#!/usr/bin/python
import socket
import cv2
import numpy
import time

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
		#String형의 이미지를 수신받아서 이미지로 변환 하고 화면에 출력
		length = recvall(conn, 16)
		while(length is None):
			length = recvall(conn, 16)

		stringData = recvall(conn, int(length))
		data = numpy.fromstring(stringData, dtype='uint8')
		#s.close()
		decimg=cv2.imdecode(data,1)
		cv2.imshow("SERVER" + str(idx),decimg)
		in_key = cv2.waitKey(1)
		if(in_key == 'q'):
			break

#수신에 사용될 내 ip와 내 port번호
TCP_IP = ''
TCP_PORT = 5001

#TCP소켓 열고 수신 대기
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(True)

conn, addr = s.accept()

getFrame(conn, 1)

s.close()
