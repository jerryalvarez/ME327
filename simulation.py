import numpy as np
from worlds import *
import time

human_controller = True


def main():
    w = BaseCarlo()
    w.render()

    input() 
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
        for k in range(400):
            w.car.set_control(controller.steering, controller.throttle)
            w.tick() 
            w.render()
            time.sleep(DT/1) 
            if w.end_sim():
                w.world.close()
                import sys
                sys.exit(0)

if __name__ == "__main__":
    main()