import threading
import time
import serial
from worlds import *
from helper import *

# Global variables
latest_value = None
sim_ended = False
ser = serial.Serial('/dev/cu.usbserial-AB0LB3DQ', 250000, timeout=1)
#er = serial.Serial('/dev/cu.usbserial-AL03G1OK', 250000, timeout=1) #Johnny's Hapkit 

# Rendering function
def main():
    w = BaseCarlo()
    depth = 0
    MAX_DEPTH = abs((GRASS_WIDTH + ROAD_WIDTH * (1 + 1)) - w.rightlane.center.x)
    x = np.array(0)
    y = np.array(0)
    export = True
    filename = "jerry_bad"

    for k in range(400):
        if export: 
            x = np.append(x, w.car.center.x)

        if (k == 1):
            print("Please wait for Serial Montior to begin")
            input()

        if w.car.center.x < w.leftlane.center.x: #left crash, depth is negative value 
            depth = max(w.car.center.x - w.leftlane.center.x, -MAX_DEPTH)
        elif w.car.center.x > w.rightlane.center.x:  #right crash, depth is positive value 
            depth = min(w.car.center.x - w.rightlane.center.x, MAX_DEPTH)
        else: 
            depth = 0
        
        if w.car.center.x < GRASS_WIDTH + ROAD_WIDTH * (1):
            y = np.append(y, 1)
        elif w.car.center.x > GRASS_WIDTH + ROAD_WIDTH * (2):
            y = np.append(y, 1)
        else: 
            y = np.append(y, 0)

        data = str(depth) + ',' + str(MAX_DEPTH) + '\n'
        ser.write(data.encode()) 

        if latest_value is not None:  
            w.car.set_control(steeringInput(latest_value),0)

        w.tick() 
        w.render()
        time.sleep(DT/1) 

        if w.end_sim():
            if export:
                x = np.delete(x, 0)
                y = np.delete(y, 0)
                exportPos(x, y, filename)
            depth = 0
            data = str(depth) + ',' + str(MAX_DEPTH) + '\n'
            ser.write(data.encode()) 
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


