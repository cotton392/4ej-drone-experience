import cv2
import time
from easytello import tello

my_drone = tello.Tello()
my_drone.streamon()

my_drone.takeoff()
time.sleep(5)
my_drone.land()
