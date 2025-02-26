###################################################################################
# Main Routine
# - Runs the advanced_wave simulation then performs specral analysis of the
#   wave for different values of stiffness (e0). Also can run an animation of
#   the wave if so desired.
#
# Author: Nick Ball               Contact: bal16004@byui.edu
# Date: 2/26/25                   Git: @SlickByui 
###################################################################################

#Import Libs
from basic_wave import basic_wave
from realistic_wave import realistic_wave
from base_string import string

def basic_wave_demo():
    #Define our init values
    length = 1.4      #m
    dx = 0.01         #m
    wave_speed = 200
    t_max = 0.1

    #Create new wave
    new_wave = string(length,dx,wave_speed,t_max)

    #Set the endpoints to be fixed
    new_wave.set_fixed_points(0)
    new_wave.set_fixed_points(length)

    #Initialize our basic wave
    b_wave = basic_wave(new_wave)

    #Displace a random point
    b_wave.displace(0.3)

    #Propogate our wave to populate array data
    b_wave.propogate()

    #Plot wave animation
    new_wave.wave_animation()

def advanced_wave_demo():
    """Runs option 2 algorithm for a given e0 value defined by
    the user per run."""
    
    #Define our init values
    length = 1.90      #m
    dx = 0.01          #m
    wave_speed = 250.  #m/s
    t_max = 0.1        #max time length in secods
    e0 = 1e-6
    r = 1/4            #ratio value

    #Create new wave
    adv_string = string(length,dx,wave_speed,t_max,r)

    #Set the endpoints to be fixed
    adv_string.set_fixed_points(0)
    adv_string.set_fixed_points(length)

    #Initialize our advanced wave
    adv_wave = realistic_wave(adv_string,e0)

    #Perform our Gaussian Pluck
    adv_wave.displace(0.4,0.1)

    #Propogate our wave to populate array data
    adv_wave.propogate()

    #Plot the Fourier Transform
    adv_string.plot_fourier(1.0)

    #Plot Average fourier 
    adv_string.plot_average_fourier()

    #Plot wave animation
    #adv_wave.wave_animation()

    return


def main():
    advanced_wave_demo()
    return

main()