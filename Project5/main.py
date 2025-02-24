###################################################################################
# Main Routine
# - For now, basic wave equation
#
#
#
#
###################################################################################

#Import Libs
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

    #Create new wave
    new_wave = wave(length,dx,wave_speed,t_max)

    #Set the endpoints to be fixed
    new_wave.set_fixed_points(0)
    new_wave.set_fixed_points(1)

    #Initialize our basic wave
    b_wave = basic_wave(new_wave)

    #Displace a random point
    b_wave.displace(0.3)

    #Propogate our wave to populate array data
    b_wave.propogate()

    #Plot it
    b_wave.wave_animation()

    return

#Test.run()
main()