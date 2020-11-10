from easytello import tello
import cv2
import time
import numpy as np
import threading

LOCAL_IP = '192.168.10.1'
LOCAL_PORT_VIDEO = '11111'
addr = 'udp://' + LOCAL_IP + ':' + str(LOCAL_PORT_VIDEO)
tello = tello.Tello()
tello.send_command('streamon')

def ohara_detect(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hsv_min = np.array([0,127,0])
	hsv_max = np.array([30,255,255])
	mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

	hsv_min = np.array([150,127,0])
	hsv_max = np.array([179,255,255])
	mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

	return mask1+mask2

def analysis_blob(bin_image):
	label = cv2.connectedComponentsWithStats(bin_image)
	n = label[0] - 1
	data = np.delete(label[2], 0, 0)
	center = np.delete(label[3], 0, 0)

	max_index = np.argmax(data[:,4])
	maxblob = {}

	maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
	maxblob["width"] = data[:, 2][max_index]  # 幅
	maxblob["height"] = data[:, 3][max_index]  # 高さ
	maxblob["area"] = data[:, 4][max_index]   # 面積
	maxblob["center"] = center[max_index]  # 中心座標

	return maxblob


alive = True
def keep_alive(d):
  while True and alive:
    d.send_command('command')
    time.sleep(5)

aliver = threading.Thread(target=keep_alive, args=(tello, ))
aliver.start()

cap = cv2.VideoCapture(addr)
try:
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			mask = ohara_detect(frame)
			target = analysis_blob(mask)

			center_x = int(target["center"][0])
			center_y = int(target["center"][1])
			print("center: ({}, {})".format(center_x, center_y))

			cv2.circle(frame, (center_x, center_y), 30, (255, 255, 0), thickness=3, lineType=cv2.LINE_AA)


			cv2.imshow("ohara-130-frame", cv2.resize(frame, dsize=(480, 360)))
			cv2.imshow("ohara-130-mask", cv2.resize(mask, dsize=(480, 360)))
			cv2.waitKey(1)
except KeyboardInterrupt:
	tello.land()
	tello.send_command('streamoff')
finally:
	alive = False
	aliver.join()
	cap.release()
	cv2.destroyAllWindows()