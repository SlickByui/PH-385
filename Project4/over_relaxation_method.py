###################################################################################
# Over Relaxation Method Class
#  - Given a grid construction, runs through the relaxation method and 
#    normalises it (to a given threshold)
#
# Author: Nick Ball               Contact: bal16004@byui.edu
# Date: 2/18/25                   
###################################################################################

#Import Libraries
import numpy as np
from cubic_grid import cubic_grid

class over_relaxation_method:

    def __init__(self,grid:cubic_grid, alpha:float):
        self.grid = grid        #set our grid point
        self.alpha = alpha      #set our alpha point
        self.e0 = 8.85e-12      #Farads/meter
        return

    #Run our over_relaxation method
    def run(self,max_tolerance):
        #Set our initial iteration and tolerance values
        n = 0
        tol = 0
        while (tol > max_tolerance or n < 5): 
            #Reset our tolerance
            tol = 0                        #tolerance value that we compare our value to

            #Make a copy of our old array values for comparison
            V_old = np.copy(self.grid.V)   

            #Parse through each point (excluding the bounds) to see calculate the average voltage
            for i in range(1, self.grid.x.size - 1):
                for j in range(1, self.grid.y.size - 1):
                    for k in range(1, self.grid.z.size - 1):

                        #Check to see if the selected point is fixed
                        if not self.grid.fixed[i,j,k]:
                            dV = self.Gauss_Seidel(i,j,k) - self.grid.V[i,j,k]
                            self.grid.V[i,j,k] += self.alpha * dV

            #Check to find our maximum difference and save it to our tolerance
            tol = np.max(np.abs(self.grid.V - V_old))

            n += 1  #update the iterator

    #Gauss_Seidel method of averaging our points (used to run the over_relaxation method)
    def Gauss_Seidel(self,i,j,k):
        return (1.0/6.0)*(self.grid.V[i-1,j,k] + self.grid.V[i+1,j,k] + self.grid.V[i,j-1,k] + 
                self.grid.V[i,j+1,k] + self.grid.V[i,j,k-1] + self.grid.V[i,j,k+1] + 
                self.grid.rho[i,j,k] * (self.grid.delta**3)/self.e0)


