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

tello.takeoff()
tello.send_command("up 40")
tello.send_command("streamon")

red_low = (0, 0, 40)
red_high = (120, 120, 255)
blue_low = (40, 0, 0)
blue_high = (255, 150, 150)
red_per_max = 70
blue_per_max = 60


is_wait = [True]
def camera_red(image):
	red_mask = cv2.inRange(image, red_low, red_high)
	red_white_pixels = cv2.countNonZero(red_mask)
	red_black_pixels = red_mask.size - red_white_pixels
	red_per = round(red_white_pixels / (red_white_pixels + red_black_pixels) * 100, 2)

	cv2.imshow("camera_red", cv2.resize(red_mask, dsize=(480, 360)))
	return True if red_per >= red_per_max else False

def camera_blue(image):
	blue_mask = cv2.inRange(image, blue_low, blue_high)
	blue_white_pixels = cv2.countNonZero(blue_mask)
	blue_black_pixels = blue_mask.size - blue_white_pixels
	blue_per = round(blue_white_pixels / (blue_white_pixels + blue_black_pixels) * 100, 2)

	cv2.imshow("camera_blue", cv2.resize(blue_mask, dsize=(480, 360)))
	return True if blue_per >= blue_per_max else False


alive = True
def keep_alive(d, iw):
  while alive:
    d.send_command('command')
    iw[0] = True
    time.sleep(5)

aliver = threading.Thread(target=keep_alive, args=(tello, is_wait))
aliver.start()

cap = cv2.VideoCapture(addr)
ok_red = True
ok_blue = True
up_flag = True

try:
	while(cap.isOpened()):

		ret, frame = cap.read()
		print("is_wait: ", is_wait[0])
		if ret == True:
			is_red_ditect = camera_red(frame)
			is_blue_ditect = camera_blue(frame)

			if is_red_ditect:
				if is_blue_ditect:
					print("Color: All")
					if is_wait[0]:
						is_wait[0] = False
						tello.forward(30)
				else:
					print("Color: Red")
					if is_wait[0]:
						is_wait[0] = False
						tello.cw(90)
			else:
				if is_blue_ditect:
					print("Color: Blue")
					if is_wait[0]:
						is_wait[0] = False
						if up_flag:
							tello.up(30)
						else:
							tello.down(30)
						up_flag ^= 1
				else:
					print("Color: None")
					if is_wait[0]:
						is_wait[0] = False
						tello.forward(30)

			cv2.imshow("camera", cv2.resize(frame, dsize=(480, 360)))
			cv2.waitKey(1)

except KeyboardInterrupt:
	tello.land()
	tello.send_command('streamoff')

finally:
	alive = False
	aliver.join()
	cap.release()
	cv2.destroyAllWindows()