from easytello import tello
import cv2

LOCAL_IP = '192.168.10.1'
LOCAL_PORT_VIDEO = '11111'
addr = 'udp://' + LOCAL_IP + ':' + str(LOCAL_PORT_VIDEO)
tello = tello.Tello()
tello.streamon()

alive = True
def keep_alive(d: tello.Tello):
  while True and alive:
    d.takeoff()
    time.sleep(5)

aliver = threading.Thread(target=keep_alive, args=(d, ))
aliver.start()


cap = cv2.VideoCapture(addr)
try:
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow("ohara-130", frame)
			cv2.waitKey(1)
except KeyboardInterrupt:
	tello.streamoff()
finally:
	alive = False
	aliver.join()
	cap.release()
	cv2.destroyAllWindows()