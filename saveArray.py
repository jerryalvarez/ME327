import numpy as np 
import matplotlib.pyplot as plt
from worlds import *

npzfile = np.load('Oscarc.npz')

x = npzfile['x']
y1 = np.arange(x.size)
center = GRASS_WIDTH + (NUM_LANES // 2 ) * ROAD_WIDTH + 0.5 * ROAD_WIDTH
disFromCenter = abs(x - center)
average = np.average(disFromCenter)

y2 = npzfile['y']
avg_orientation = np.rad2deg(np.average(abs(y2)))

print("Average Distance from Center:", round(average,3))
print("Average Orientation:", round(avg_orientation,3), "Degrees")
plt.axvline(x = center, color = 'b', label = 'axvline - full height')
plt.plot(x,y1)
plt.show()


