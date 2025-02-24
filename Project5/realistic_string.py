###################################################################################
# Realistic String Class
# - Runs a simulation of a more realistic string w/ parameters of stiffness
#   implementing Eq.(6.11).
#
###################################################################################

#Import Libraries
from wave import wave
import numpy as np

class realistic_string:
    def __init__(self,wave,e0):
        self.wave = wave
        self.e0 = e0       #stiffness parameter (unitless)
        return
    
    def displace(self):
        pass

    def propogate(self):
        #Defining coefficient values here to simplify the loop math
        c1 = (2 - 2.0*(self.wave.r**2) - 6 * self.e0 * (self.wave.r**2) * len(self.wave.x_array)**2)
        c2 = (2.0*self.wave.r**2)*(1 + 4 * self.e0 * len(self.wave.x_array)**2)
        c3 = self.e0 * (self.wave.r**2) * len(self.wave.x_array)**2

        #Loop through our first time value
        t = 0
        for x in range(0,len(self.wave.x_array)-1):
                if (self.wave.fixed_point[x] != True):
                    self.wave.y_array[x,t+1] = c1 * self.wave.y_array[x,t] - self.wave.y_array[x,t] + \
                        c2*(self.wave.y_array[x+1,t] + self.wave.y_array[x-1,0])
                    
                    #Check for hinge points (ie i = 0,1 or i = max-1,max)
                    if (x <= 1): #i = 0,1
                        self.wave.y_array[x,t+1] = self.wave.y_array[x,t+1] - c3*(self.wave.y_array[x + 2,t] + self.wave.y_array[2-x,t])

                    elif (x >= len(self.wave.x_array)-2): #i = max-1,max
                        self.wave.y_array[x,t+1] = self.wave.y_array[x,t+1] - c3*(-self.wave.y_array[x - 2,t] - self.wave.y_array[x-2,t])

                    else:
                        self.wave.y_array[x,t+1] = self.wave.y_array[x,t+1] - c3*(self.wave.y_array[x + 2,t] + self.wave.y_array[x-2,t])

        #Loop through the rest of our time (possibly make the above code a function)
        
        pass

    def spectral_analysis(self):
        pass