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
    def __init__(self,length, dx):
        self.L = length/dx
        self.dx = dx

        #Make i array from 0 to L given steps of dx
        self.i = np.arange(0,self.L + 1,1)
        DEBUG.print(len(self.i), "Len of i: ")

        #Make x array from 0 to L
        self.x_array = np.arange(0,length + dx, dx)   #Do these need to be 100 or 101
        DEBUG.print(len(self.x_array), "Len of x_array: ") 

        #Make y array match our x_array
        self.y_array = np.zeros_like(self.x_array)
        DEBUG.print(len(self.y_array), "Len of y_array: ")

        #Create array of bool values about point fixedness
        self.fixed_point = np.full_like(self.x_array,False)

    #Function sets explicit points corresponding to y_array vals that are fixed
    def set_fixed_points(self,I:int):
        pass

    
