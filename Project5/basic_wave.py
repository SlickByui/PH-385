###################################################################################
# Basic Wave Class
# - Just the basic wave propogation function outlined in Eq.(6.6) using the 
#   wave class.
#
#
#
###################################################################################

#Import Libs
import numpy as np
from matplotlib import pyplot as plt
from _debug import debug
from wave import wave

DEBUG = debug(False)

class basic_wave:
    def __init__(self, wave):
        #Init the wave function
        self.wave = wave
        return

    #Displaceme a random point as defined by the user
    def displace(self,x0:float):
        #For now, k will be fixed here
        k = 1000   #m^-2

        #Loop through x array and apply 
        for i,x in enumerate(self.wave.x_array):
            if (self.wave.fixed_point[i] != True):
                self.wave.y_array[i,0] = np.exp(-k*(x-x0)**2)

        DEBUG.print(self.wave.y_array[0,0],"wave.y_array[0,0] = ")
        DEBUG.print(self.wave.y_array[-1,0], "self.y_array[-1,0] = ")

    #Propogate our function through time
    def propogate(self):
        #Loop through our first time value
        for x in range(1,len(self.wave.x_array)-1):
                self.wave.y_array[x,1] = 2.0*(1.0-self.wave.r**2)* self.wave.y_array[x,0] - self.wave.y_array[x,0] + \
                    (self.wave.r**2)*(self.wave.y_array[x+1,0] + self.wave.y_array[x-1,0])

        #Loop through our time values
        for t in range(1,len(self.wave.time)-1):   #Make sure this starts at Next time step (not t=0)
            #Loop through our discretized string
            for x in range(1,len(self.wave.x_array)-1):     #might be better to fix this
                self.wave.y_array[x,t+1] = 2.0*(1.0-self.wave.r**2)* self.wave.y_array[x,t] - self.wave.y_array[x,t-1] + \
                    (self.wave.r**2)*(self.wave.y_array[x+1,t] + self.wave.y_array[x-1,t])
        return
    

    #Plot our function
    def wave_animation(self):

        #Loop through our time function to graph each segment of dt
        DEBUG.print(np.shape(self.wave.y_array[:,0]),"Shape of y_array[:,t]")
        DEBUG.print(np.shape(self.wave.y_array[:][0]),"Shape of y_array[:][t]")
        DEBUG.print(len(self.wave.y_array[:,0]),"Len of y_array[:,t]")
        DEBUG.print(self.wave.y_array[:,0])
        DEBUG.print(self.wave.y_array[:][0])
        DEBUG.print(self.wave.y_array[1,1],"self.y_array[1,0] = ")
        DEBUG.print(self.wave.y_array[1][1],"self.y_array[1][0] = ")

        for t in range(0,len(self.wave.time)):
            #Set our plot features
            plt.title("Basic Wave Eq.")
            plt.ylim([-3.5,3.5])
            plt.plot(self.wave.x_array,self.wave.y_array[:,t])
            plt.draw()
            plt.pause(0.01)
            plt.clf()

        plt.close()

        return
