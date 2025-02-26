###################################################################################
# Realistic String Class
# - Runs a simulation of a more realistic string w/ parameters of stiffness
#   implementing Eq.(6.11).
#
###################################################################################

#Import Libraries
from base_string import string
import numpy as np

class realistic_wave:
    def __init__(self,wave,e0):
        self.string = wave
        self.e0 = e0       #stiffness parameter (unitless)
        return
    
    def displace(self, x_mid, width):
        """ Performs gaussian pluck on a given mid point of specified width
        over the whole of the y_array.
        """
        #For now, k will be fixed here
        k = 2/(width**2)   #m^-2

        #Loop through y_array from start to end point to apply Gauss Pluck
        for i,x in enumerate(self.string.x_array):
            if (self.string.fixed_point[i] != True):
                self.string.y_array[i,0] = np.exp(-k*(x-x_mid)**2)

        pass

    def propogate(self):
        """ Propogates our relaxation-like method of the wave over time
        using Eq. 6.11.
        """
        #Defining coefficient values here to simplify the loop math
        c1 = (2.0 - 2.0*(self.string.r**2) - 6 * self.e0 * (self.string.r**2) * self.string.M**2)
        c2 = (self.string.r**2)*(1 + 4 * self.e0 * self.string.M**2)
        c3 = self.e0 * (self.string.r**2) * self.string.M**2

        #Loop through our first time value
        t = 0
        for x in range(2,len(self.string.x_array)-2):
            if (self.string.fixed_point[x] != True):  #Check to see if its a fixed point
                self.string.y_array[x,t+1] = c1 * self.string.y_array[x,t] - self.string.y_array[x,t] + \
                    c2*(self.string.y_array[x+1,t] + self.string.y_array[x-1,t]) - c3*(self.string.y_array[x + 2,t] + self.string.y_array[x-2,t])

        #Loop through the rest of our time
        for t in range(1,len(self.string.time)-1):
            for x in range(2,len(self.string.x_array)-2):
                if (self.string.fixed_point[x] != True):  #Check to see if its a fixed point
                    self.string.y_array[x,t+1] = c1 * self.string.y_array[x,t] - self.string.y_array[x,t-1] + \
                        c2*(self.string.y_array[x+1,t] + self.string.y_array[x-1,t]) - c3*(self.string.y_array[x + 2,t] + self.string.y_array[x-2,t])

        return