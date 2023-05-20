import serial
import time
#using hapkit template #1 
# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('/dev/cu.usbserial-AB0LB3DQ', 9800, timeout=1)
time.sleep(2)

b = True

def num_to_range(num, inMin, inMax, outMin, outMax):
  return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                  - outMin))

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

for i in range(1000):
    line = ser.readline()   # read a byte
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        num = -float(string) # convert the unicode string to an int
        output = num_to_range(num, -0.06, 0.06, 0, 180)
        output = clamp(output, 0, 180)
        print(output)

ser.close()

