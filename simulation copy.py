import numpy as np
from worlds import *
import time
import serial

human_controller = True

def num_to_range(num, inMin, inMax, outMin, outMax):
  return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                  - outMin))

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def main():
    w = BaseCarlo()
    w.render()

    input() 
    if not human_controller:
        for k in range(400):
            w.tick() 
            w.render()
            time.sleep(DT) # Let's watch it 1x
            if w.end_sim():
                w.world.close()
                import sys
                sys.exit(0)

    else: # Let's use the steering wheel (Logitech G29) for the human control of car c1
        ser = serial.Serial('/dev/cu.usbserial-AB0LB3DQ', 9800, timeout=1)
        time.sleep(2)

    for k in range(400):
        line = ser.readline()   # read a byte
        if line:
            string = line.decode()  # convert the byte string to a unicode string
            num = -float(string) # convert the unicode string to an int
            output = num_to_range(num, -0.06, 0.06, 0, 180)
            output = clamp(output, 0, 180)
            w.car.set_control(output, 0)
            print(output)
        w.tick() 
        w.render()
        time.sleep(DT) 
        if w.end_sim():
            ser.close()
            w.world.close()
            import sys
            sys.exit(0)

if __name__ == "__main__":
    main()