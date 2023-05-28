import numpy as np 
import matplotlib.pyplot as plt

# x = np.arange(5)
# y = np.arange(6)

# np.savez("example", x=x, y=y)

npzfile = np.load('example.npz')

x = npzfile['x']

y = npzfile['y']

plt.plot(x)
plt.show()

# print(npzfile['x'])
# print(npzfile['y'])
