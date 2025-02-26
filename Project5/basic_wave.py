###################################################################################
# Basic Wave Class
# - Just the basic wave propogation function outlined in Eq.(6.6) using the 
#   string object passed from main. Technically not needed for the project
#   but helpful for testing out basic wave functionality
###################################################################################

#Import Libs
from base_string import string
import numpy as np

class basic_wave:
    def __init__(self, wave):
        #Init the wave function
        self.string = wave
        return

    #Displaceme a random point as defined by the user
    def displace(self,x0:float):
        #For now, k will be fixed here
        k = 1000   #m^-2

        #Loop through x array and apply 
        for i,x in enumerate(self.string.x_array):
            if (self.string.fixed_point[i] != True):
                self.string.y_array[i,0] = np.exp(-k*(x-x0)**2)

    #Propogate our function through time
    def propogate(self):
        #Loop through our first time value
        for x in range(1,len(self.string.x_array)-1):
                self.string.y_array[x,1] = 2.0*(1.0-self.string.r**2)* self.string.y_array[x,0] - self.string.y_array[x,0] + \
                    (self.string.r**2)*(self.string.y_array[x+1,0] + self.string.y_array[x-1,0])

        #Loop through our time values
        for t in range(1,len(self.string.time)-1):   #Make sure this starts at Next time step (not t=0)
            #Loop through our discretized string
            for x in range(1,len(self.string.x_array)-1):     #might be better to fix this
                if (self.string.fixed_point[x] != True):
                    self.string.y_array[x,t+1] = 2.0*(1.0-self.string.r**2)* self.string.y_array[x,t] - self.string.y_array[x,t-1] + \
                        (self.string.r**2)*(self.string.y_array[x+1,t] + self.string.y_array[x-1,t])
        return