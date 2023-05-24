import threading
import time
import serial
from worlds import *
from helper import *

# Global variable to store the latest value from the serial monitor
latest_value = None
sim_ended = False
rightLane = False 
leftLane = False
centered = True
ser = serial.Serial('/dev/cu.usbserial-AB0LB3DQ', 250000, timeout=1)

# Rendering function
def main():
    w = BaseCarlo()
    for k in range(400):

        if w.lane_departure:
            if rightcollision(w):
                ser.write(b"left\n")
            elif leftcollision(w):
                ser.write(b"right\n") 
            else: 
                ser.write(b"other\n") 

        if (k == 1):
            print("Please move handle to its limits slowly")
            input()

        if latest_value is not None:  
            #print(latest_value)
            w.car.set_control(steeringInput(latest_value),0)

        w.tick() 
        w.render()
        time.sleep(DT/1) 

        if w.end_sim():
            global sim_ended
            sim_ended = True
            w.world.close()
            import sys
            sys.exit(0)

# Serial reading function
def read_serial_values():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline()
            string = line.decode()  # convert the byte string to a unicode string
            num = float(string) # convert the unicode string to an int
            # Update the latest_value with the new value from the serial monitor
            global latest_value
            latest_value = num
        
        if sim_ended:
            ser.close()
            return

if __name__ == "__main__":
    serial_thread = threading.Thread(target=read_serial_values)
    serial_thread.start()
    main()


