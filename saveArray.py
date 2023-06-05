import numpy as np 
import matplotlib.pyplot as plt

npzfile = np.load('jerry_bad.npz')

x = npzfile['x']
y1 = np.arange(x.size)
center = x[0]
disFromCenter = abs(x - center)
average = np.average(disFromCenter)

y2 = npzfile['y']
percentOutsideLane = (np.sum(y2)/np.size(y2)) * 100


print("Average Distance from Center:", round(average,3))
print("Percent Outside Lane:", round(percentOutsideLane,3) ,"%")
plt.plot(x,y1)
plt.show()


