#include "molDyn.hpp"

int main()
{
    int nmol=16;                  // Number of molecules in simulation
    double dims[2]={20.,20.};     // Box limits (distance)
    double rcutfactor=5.00;       // Ignore interactions > 5 eq. lengths
    double dt=0.005;              // Time step (time)
    double dr=0.001;              // Position variation (distance)
    double v0=0.1;                // Max. initial speed (speed)

    molDyn * mol = new molDyn(nmol,2,dims,rcutfactor);
    mol->initializeSim(dr,dt,v0,"data.csv");
}