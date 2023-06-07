import numpy as np
from world import *
import time
from helper import *
import serial 

human_controller = True

def main():
    w = BaseCarlo()
    w.render()

    if not human_controller:
        for k in range(400):
            w.tick() 
            w.render()
            time.sleep(DT/1) # Let's watch it 1x
            if w.end_sim():
                w.world.close()
                import sys
                sys.exit(0)

    else: # Let's use the steering wheel (Logitech G29) for the human control of car c1
        from carlo.interactive_controllers import KeyboardController
        controller = KeyboardController(w.world)
        ser = serial.Serial('/dev/cu.usbserial-AB0LB3DQ', 250000, timeout=1)
        for k in range(400):
            w.car.set_control(controller.steering, controller.throttle)
            if w.lane_departure:
                if rightcollision(w):
                    ser.write(b"left\n")
                elif leftcollision(w):
                    ser.write(b"right\n") 
                else: 
                    ser.write(b"other\n") 

            w.tick() 
            w.render()
            time.sleep(DT/1) 
            if w.end_sim():
                w.world.close()
                import sys
                sys.exit(0)

if __name__ == "__main__":
    main()