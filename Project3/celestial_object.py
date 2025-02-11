###################################################################################
# Celestial Object Class
#  - Keeps track of and returns properties of a celestial object
#
# Author: Nick Ball       Contact: bal16004@byui.edu
# Date: 2/10/2025
###################################################################################

#Import Libraries
from numpy import array

class celestial_object:
    def __init__(self,name: str, mass:float ,x_initial: list ,v_initial: list, color:str = "blue"):
        #Get our initial mass, position, and velocity and store them
        self.name = name
        self.mass = mass
        self.r = array(x_initial)
        self.v = array(v_initial)
        self.color = color

        #Create a list that tracks our positions
        self.pos = [self.r]

    def get_mass(self):
        #Returns objects mass
        return self.mass

    def get_position(self):
        #Return most recent version of r
        return self.r
    
    def set_position(self, position:list):
        self.r = array(position)
        return
    
    def get_velocity(self):
        #Return most recent version of v
        return self.v