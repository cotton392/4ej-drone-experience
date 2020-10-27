from easytello import tello
import time
import threading
import cv2

# see: https://stackoveflow.com/questions/50916903

d = tello.Tello()
d.takeoff()

d.streamon()

# for i in range(4):
# 	d.forward(100)
# 	d.cw(90)
	
# time.sleep(10)

# d.land()
# Turning on stream
# Turning off stream
# d.streamoff()
alive = True
def keep_alive(d: tello.Tello):
  while True and alive:
    d.takeoff()
    time.sleep(5)

cap = cv2.VideoCapture('udp://0.0.0.0:11111')
if not cap.isOpened():
  print("Failed to open VideoCapture, stopping.")
  exit(-1)

aliver = threading.Thread(target=keep_alive, args=(d, ))
aliver.start()

while True:
  ret, frame = cap.read()

  if not ret:
    print('empty frame')
    break 

  mask = cv2.inRange(frame, (0, 0, 0), (100, 100, 100))
  not_mask = cv2.bitwise_not(mask)
  cv2.imshow('ohara-mask', not_mask)
  cv2.imshow('ohara-130', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

d.land()
alive = False
d.streamoff()
cap.release()
aliver.join()
cv2.destroyAllWindows()