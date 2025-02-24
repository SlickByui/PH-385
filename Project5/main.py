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
from basic_wave import basic_wave
from wave import wave
from _debug import debug
from _test import test

Test = test()

def main():
    #Define our init values
    length = 1    #m
    dx = 0.01     #m
    wave_speed = 200
    t_max = 0.1

    new_wave = wave(length,dx)

    #Initialize our basic wave
    b_wave = basic_wave(length,dx,wave_speed,t_max)

    #Displace a random point
    b_wave.displace(0.3)

    b_wave.propogate()

    #Propogate our wave to populate array data
    #b_wave.propogate()

    #Plot it
    b_wave.plot_wave()

    return

#Test.run()
main()