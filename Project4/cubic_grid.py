################################################################################
# Cubic Grid Class
#  - Given a grid construction, runs through the relaxation method
#    and normalises it (to a given threshold)
#
# Author: Nick Ball 
# Date: 2/18/25
################################################################################

#Import Libraries
import numpy as np
from matplotlib import pyplot as plt

class cubic_grid:
    def __init__(self,xmin,xmax,ymin,ymax,zmin,zmax,delta):
        #Initialize our array
        self.x = np.arange(xmin,xmax+delta,delta)
        self.y = np.arange(ymin,ymax+delta,delta)
        self.z = np.arange(zmin,zmax+delta,delta)
        self.rho = np.zeros((self.x.size, self.y.size, self.z.size))
        self.fixed = np.full((self.x.size, self.y.size, self.z.size),False)
        self.V = np.zeros((self.x.size, self.y.size, self.z.size))
        self.delta = delta
        return
    

    def modify(self,x,y,z,rho,fixed:bool,V:float):
        #find closest points
        i = np.argmin(np.abs(self.x-x))
        j = np.argmin(np.abs(self.y-y))
        k = np.argmin(np.abs(self.z-z))

        #Set the values for the charge density, fixed flag, and voltage
        self.rho[i][j][k] = rho
        self.fixed[i][j][k] = fixed
        self.V[i][j][k] = V
        return
    
    def slice(self,plane = "xy", guess = 0):
        # for xy plane
        if plane == "xy":
            x1 = self.x
            x2 = self.y 
            i = np.argmin(np.abs(self.z-guess))
            x3 = self.V[:,:,i]
        # for xz plane
        elif plane == "xz":
            x1 = self.x
            x2 = self.z 
            i = np.argmin(np.abs(self.y-guess))
            x3 = self.V[:,i,:]
        # for yz plane
        elif plane == "yz":
            x1 = self.y
            x2 = self.z 
            i = np.argmin(np.abs(self.x-guess))
            x3 = self.V[i,:,:]
        # if not xy, xz, or yz plane then not known
        else:
            print("UNKNOWN SLICE PLANE", plane)
            return
        x1g,x2g = np.meshgrid(x1,x2)
        return x1g,x2g,x3
    
    def plot_slice(self,plane = "xy", guess = 0):
        
        # set the slice plane
        x,y,z = self.slice(plane,guess)
        # Display plot
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        # if in xy plane, label x axis "x" and y axis "y"
        if plane == "xy":
            ax.set_xlabel("x")
            ax.set_ylabel("y")

        # if in xz plane, label x axis "x" and y axis "z"
        elif plane == "xz":
            ax.set_xlabel("x")
            ax.set_ylabel("z")

        # if in yz plane, label x axis "y" and y axis "z"
        elif plane == "yz":
            ax.set_xlabel("y")
            ax.set_ylabel("z")

        # labels the z axis as "V" for potential
        ax.set_zlabel("V")

        # plots a surface plot, rstride defines the step sizes of the 
        # rows, cstride is the stepsizes for the columns, plasma is the coloring 
        ax.plot_surface(x,y,z, rstride = 1, cstride=1, cmap = 'plasma',edgecolor = None)
        plt.show()
    

    