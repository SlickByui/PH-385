#########################################################################
#  Main Class
#    - Main function that initializes and runs the solar system
#      simulation 
#
# Author: Nick Ball       Contact: bal16004@byui.edu
# Date: 2/10/2025
#########################################################################

#Import Libraries
from celestial_object import celestial_object
from solar_system import solar_system
from numpy import pi

def main():
    """ Creates Sun, Earth, and Jupiter celestial_object objects and adds them
            to a solar system object. Function then simulates solar system 
            interaction and shows an animation of it.
        Input: None

        Return:None
    """
    #Create "planets" with input parameters
    sun = celestial_object("Sun",1.0,[0.0,0.0,0.0],[0.0,0.0,0.0],color = "yellow")
    earth = celestial_object("Earth", 3.00274e-6,[1.0,0.0,0.0],[0.0,2.0*pi,0.0])
    jupiter = celestial_object("Jupiter", 9.54588e-4*1000,[-5.2,0.0,0.0], [0.0,-2.0*pi*5.2/11.86,0.0],color = "orange")

    #Create our solar system object
    ss = solar_system([earth,sun,jupiter])

    #Evolve our solar system
    ss.evolve(11.2,0.01)

    #Show the plot of our trajectory
    ss.plot_data("output.png")

    return

main()