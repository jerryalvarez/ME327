from world import *
import numpy as np

def steeringInput(xh): 
    """ 
    Receives position of steeering wheel and determines 
    the appropriate steering that the object should receive
    """
    if(xh > 0.01):
       current_steering = -3.5
    elif (xh < -0.01):
       current_steering = 3.5
    else: 
       current_steering = 0

    return current_steering

def exportPos(x, y, filename):
   """ 
   Exports the x and y np arrays using np.savez
   """
   np.savez(str(filename), x=x, y=y)

def importPos(filename):
   """ 
   Imports the x and y np arrays using np.savez
   """
   npzfile = np.load(str(filename) + ".npz")
   x = npzfile['x']
   y = npzfile['y']