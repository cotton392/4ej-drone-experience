import cv2
from easytello import tello

my_drone = tello.Tello()
my_drone.streamon()

my_drone.takeoff()

my_drone.land()
