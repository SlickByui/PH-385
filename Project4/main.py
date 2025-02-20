###################################################################################
# Main Class Python 
#   - Main method responsible for initializing our grid, setting its
#     boundaries, point charges, and then using the over relaxation method
#     to simulate the electric potential of our given arrangement.
#
# Author: Nick Ball               Contact: bal16004@byui.edu
# Date: 2/18/25                   Git: @SlickByui
###################################################################################

#Import Libraries
from cubic_grid import cubic_grid
from over_relaxation_method import over_relaxation_method
import numpy as np

#Define the size of our grid and the spacing between the points
xlim=0.5
ylim=0.5
zlim=0.5
delta=0.025

#Calculate the number of points per axis of the grid
nx=int(2.0*float(xlim)/float(delta))+1
ny=int(2.0*float(ylim)/float(delta))+1
nz=int(2.0*float(zlim)/float(delta))+1

#Create our grid object
grid=cubic_grid(-xlim,xlim,-ylim,ylim,-zlim,zlim,delta)


# Enforcing Boundary Conditions

# 1. BC of zero at edges of the grid
for x in [x*delta-xlim for x in range (0,nx)]:
    for y in [y*delta-ylim for y in range (0,ny)]:
        grid.modify(x,y,-zlim,0.0,True,0.0)
        grid.modify(x,y,zlim,0.0,True,0.0)

for x in [x*delta-xlim for x in range (0,nx)]:
    for z in [z*delta-zlim for z in range (0,nz)]:
        grid.modify(x,-ylim,z,0.0,True,0.0)
        grid.modify(x,ylim,z,0.0,True,0.0)

for y in [y*delta-ylim for y in range (0,ny)]:
    for z in [z*delta-zlim for z in range (0,nz)]:
        grid.modify(-xlim,y,z,0.0,True,0.0)
        grid.modify(xlim,y,z,0.0,True,0.0)

# 2. Add grounded plate
for x in [x*delta-xlim for x in range (0,nx)]:
    for y in [y*delta-ylim for y in range (0,ny)]:
        if np.sqrt(x*x+y*y) <= 0.10:
            grid.modify(x,y,0.0,0.0,True,0.25)

# 3. Add the point charges
grid.modify( 0.25, 0.00,0., 1.0e-6,False,0.0)
grid.modify(-0.25, 0.00,0.,-1.0e-6,False,0.0)
grid.modify( 0.00, 0.25,0., 1.0e-6,False,0.0)
grid.modify( 0.00,-0.25,0.,-1.0e-6,False,0.0)

#Run grid through our over_relaxation_method
over_rerlax = over_relaxation_method(grid,1.8)
over_rerlax.solve(1e-4)

#Plot the potential on the x-y plane using our initial guess
grid.plot_slice("xy",0)

