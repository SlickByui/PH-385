###################################################################################
# Main Routine
# - For now, basic wave equation
#
#
#
#
###################################################################################

#Import Libs
import numpy as np
from matplotlib import pyplot as plt
from _debug import debug

DEBUG = debug(True)

class basic_wave:
    def __init__(self, length, dx, wave_speed, t_max):
        
        #Initialize our values
        self.L = length
        self.dx = dx
        self.c = wave_speed
        self.dt = dx/self.c
        
        self.r = 1.0    #make dependent values for this?
        self.t_max = t_max

        #Create our x_array for plotting
        self.x_array = np.arange(0,self.L + self.dx,self.dx)
        DEBUG.print(len(self.x_array),"Len of x_array: ")

        #Create our time array
        self.time = np.arange(0,t_max + self.dt, self.dt)
        DEBUG.print(len(self.time),"Len of time: ")

        #Make our y_array from 0 to M
        self.y_array = np.zeros((len(self.x_array),len(self.time)),float)      #End points should be fixed
        DEBUG.print(np.shape(self.y_array),"Shape of y_array: ")

        return

    #Displaceme a random point as defined by the user
    def displace(self,x0:float):
        #For now, k will be fixed here
        k = 1000   #m^-2

        #Loop through x array and apply 
        for i,x in enumerate(self.x_array):
            self.y_array[i,0] = np.exp(-k*(x-x0)**2)

        #Reset end points
        self.y_array[0,0] = 0
        self.y_array[-1,0] = 0

        DEBUG.print(self.y_array[0,0],"self.y_array[0,0] = ")
        DEBUG.print(self.y_array[-1,0], "self.y_array[-1,0] = ")

    #Propogate our function through time
    def propogate(self):
        #Loop through our first time value
        for x in range(1,len(self.x_array)-1):
                self.y_array[x,1] = 2.0*(1.0-self.r**2)* self.y_array[x,0] - self.y_array[x,0] + (self.r**2)*(self.y_array[x+1,0] + self.y_array[x-1,0])

        #Loop through our time values
        for t in range(1,len(self.time)-1):   #Make sure this starts at Next time step (not t=0)
            #Loop through our discretized string
            for x in range(1,len(self.x_array)-1):     #might be better to fix this
                self.y_array[x,t+1] = 2.0*(1.0-self.r**2)* self.y_array[x,t] - self.y_array[x,t-1] + (self.r**2)*(self.y_array[x+1,t] + self.y_array[x-1,t])
        return
    

    #Plot our function
    def plot_wave(self):

        #Loop through our time function to graph each segment of dt
        DEBUG.print(np.shape(self.y_array[:,0]),"Shape of y_array[:,t]")
        DEBUG.print(np.shape(self.y_array[:][0]),"Shape of y_array[:][t]")
        DEBUG.print(len(self.y_array[:,0]),"Len of y_array[:,t]")
        DEBUG.print(self.y_array[:,0])
        DEBUG.print(self.y_array[:][0])

        DEBUG.print(self.y_array[1,1],"self.y_array[1,0] = ")
        DEBUG.print(self.y_array[1][1],"self.y_array[1][0] = ")

        for t in range(0,len(self.time)):
            #Set our plot features
            plt.title("Basic Wave Eq.")
            plt.ylim([-3.5,3.5])
            plt.plot(self.x_array,self.y_array[:,t])
            plt.draw()
            plt.pause(0.01)
            plt.clf()

        plt.close()

        return
