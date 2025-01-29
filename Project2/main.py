#Import libs
from numpy import pi
from driven_damped_oscillator import driven_damped_oscillator

def main():
    osci = driven_damped_oscillator(0.2,0,1.2,pi/2,run_poincare=True)
    osci.run()
    osci.plot_data()
    return

main()