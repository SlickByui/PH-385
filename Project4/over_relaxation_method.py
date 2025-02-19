#############################################################################################
# Over Relaxation Method Class
#  - Given a grid construction, runs through the relaxation 
#    method and normalises it (to a given threshold)
#
#############################################################################################

#Import Libraries
import numpy as np
from cubic_grid import cubic_grid

class over_relaxation_method:

    def __init__(self,grid:cubic_grid, alpha:float):
        self.grid = grid
        self.alpha = alpha
        self.e0 = 8.85e-12
        return

    def solve(self,max_tolerance):
        #Set our initial iteration and tolerance values
        n = 0
        tol = 0
        while (tol > max_tolerance or n < 5): 
            #Reset our tolerance
            tol = 0
            V_old = np.copy(self.grid.V)   #Make a copy of our old array values for comparison
            for i in range(1, self.grid.x.size - 1):
                for j in range(1, self.grid.y.size - 1):
                    for k in range(1, self.grid.z.size - 1):
                        if not self.grid.fixed[i,j,k]:
                            dV = self.Gauss_Seidel(i,j,k) - self.grid.V[i,j,k]
                            self.grid.V[i,j,k] += self.alpha * dV

            #Check to find our maximum difference and save it to our tolerance
            tol = np.max(np.abs(self.grid.V - V_old))

            n += 1  #update the runtime

    def Gauss_Seidel(self,i,j,k):
        return (1.0/6.0)*(self.grid.V[i-1,j,k] + self.grid.V[i+1,j,k] + self.grid.V[i,j-1,k] + 
                self.grid.V[i,j+1,k] + self.grid.V[i,j,k-1] + self.grid.V[i,j,k+1] + 
                self.grid.rho[i,j,k] * (self.grid.delta**3)/self.e0)


