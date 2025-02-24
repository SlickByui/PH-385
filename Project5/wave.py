###################################################################################
# Wave Class
# - Contains information for a 2D wave for use in other wave methods
#
###################################################################################

#Import Libs
import numpy as np
from _debug import debug

DEBUG = debug(True)

class wave:
    def __init__(self, length, dx, wave_speed, t_max):
        #Initialize our values
        self.L = length
        self.dx = dx
        self.c = wave_speed
        self.dt = dx/self.c
        self.r = 1.0    #make dependent values for this?
        self.t_max = t_max

        #Make i array from 0 to L given steps of dx
        self.i = np.arange(0,self.L + 1,1)
        DEBUG.print(len(self.i), "Len of i: ")

        #Create our x_array for plotting
        self.x_array = np.arange(0,self.L + self.dx,self.dx)
        DEBUG.print(len(self.x_array),"Len of x_array: ")

        self.time = np.arange(0,t_max + self.dt, self.dt)
        DEBUG.print(len(self.time),"Len of time: ")

        #Make our y_array
        self.y_array = np.zeros((len(self.x_array),len(self.time)),float)      #End points should be fixed
        DEBUG.print(np.shape(self.y_array),"Shape of y_array: ")

        #Create array of bool values about point fixedness
        self.fixed_point = np.full_like(self.x_array,False)

    #Function sets explicit points corresponding to y_array vals that are fixed
    def set_fixed_points(self,x_point:float):
        #Find closest point to input point
        i = np.argmin(np.abs(self.x_array-x_point))

        self.fixed_point[i] = True #Set fixed point to true
        return

    
