###################################################################################
# Main Routine
# - Rewrite of basic_wave. Not sure if this is good or not.
#
#
#
#
###################################################################################

#Import libs
import numpy as np
from matplotlib import pyplot as plt

class basic_wave2:  #would we want to make this into only the wave_data? (like x, y, clamped points, etc?)
    def __init__(self, length, dx, wave_speed, t_max):
        self.L = int(length/dx)
        self.dx = dx
        self.c = wave_speed
        self.t_max = t_max

        #Use defined values to calculate dt
        self.dt = dx/self.c
        self.r = 1    #this value is 'Idealy' 1, for now

        #Make i array from 0 to L given steps of dx
        self.i = np.arange(0,self.L + 1,1)

        #Make n array from t = 0 to t=t_max with steps of dt
        # Note: so long as t_max > dt, we are fine
        self.t_max = int(self.t_max/self.dt)  #converts this into int value (or should)
        self.n = np.arange(0,t_max + 1,1)  

        #Make x array from 0 to L
        self.x_array = np.arange(0,length + dx, dx)

        #Make y array match our x_array
        self.y_array = np.zeros_like(self.x_array)    

        #Make list of ypoints
        self.y_points = []  

    def displace(self,x0:float):
        #For now, k will be fixed here
        k = 1000   #m^-2

        #Loop through x array and apply 
        for i,x in enumerate(self.x_array):
            self.y_array[i,0] = np.exp(-k*(x-x0)**2)

        #Make sure the displaced values are first on the list
        self.y_points = [self.y_array]
        return



    def propogate(self):
        for n in self.n:
            for i in range(1,len(self.x_array)-1):
                self.y_points.append()


    def calc_next_y(self,i,n):
        return 2*(1-self.r**2)*self.y_array[]

            

