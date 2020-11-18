from easytello import tello
import cv2
import time
import random
import numpy as np
import threading

LOCAL_IP = '192.168.10.1'
LOCAL_PORT_VIDEO = '11111'
addr = 'udp://' + LOCAL_IP + ':' + str(LOCAL_PORT_VIDEO)
tello = tello.Tello()

order_list = ["up 40", "down 30", "left 40", "right 40", "forward 40", "back 40", "cw 360", "ccw 360"]
waiting_second = 5
is_wait = [True]

tello.takeoff()
tello.send_command("up 40")
tello.send_command("streamon")

def ohara_detect(image):
	low_threshold = (0, 0, 40)
	high_threshold = (20, 20, 255)
	red_per_max = 5

	red_mask = cv2.inRange(image, low_threshold, high_threshold)
	red_white_pixels = cv2.countNonZero(red_mask)
	red_black_pixels = red_mask.size - red_white_pixels
	red_per = round(red_white_pixels / (red_white_pixels + red_black_pixels) * 100, 2)
	print("red_per: ", str(red_per))

	cv2.imshow("ohara_130mask", cv2.resize(red_mask, dsize=(480, 360)))

	return True if red_per >= red_per_max else False

alive = True
def keep_alive(d, iw):
  while alive:
    d.send_command('command')
    iw[0] = True
    time.sleep(5)

aliver = threading.Thread(target=keep_alive, args=(tello, is_wait))
aliver.start()

cap = cv2.VideoCapture(addr)

try:
	while(cap.isOpened()):

		ret, frame = cap.read()
		print("is_wait: ", is_wait[0])
		if ret == True:
			is_red_ditect = ohara_detect(frame)
			print("is_red_ditect: ", is_red_ditect)

			if is_red_ditect and is_wait[0]:
				is_wait[0] = False
				tello.send_command(order_list[random.randint(0, len(order_list) - 1)])

			cv2.imshow("ohara_130frame", cv2.resize(frame, dsize=(480, 360)))
			cv2.waitKey(1)

except KeyboardInterrupt:
	tello.land()
	tello.send_command('streamoff')

finally:
	alive = False
	aliver.join()
	cap.release()
	cv2.destroyAllWindows()