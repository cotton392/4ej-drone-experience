import time
import cv2
from easytello import tello


def main():
    my_drone = tello.Tello()
    my_drone.takeoff()
    time.sleep(1)
    my_drone.land()


if __name__ == '__main__':
    main()
