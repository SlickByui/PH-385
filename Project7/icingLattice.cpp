#include "icingLattice.hpp"

////////////////////////////////////////////////////////////////////////////
// Icing Lattice Object and Methods
//  - Object and methods for our Icing lattice, defining its boundaries
//    and simulating random flipping, total energy, and total magnetization
//    of our particle lattice.
// 
// Author: Nick Ball              Contact: nbal16004@byui.edu
// Date: 03/10/25                 Git: https://github.com/SlickByui/PH-385
////////////////////////////////////////////////////////////////////////////

//Initializer
icingLattice::icingLattice(int Nx, int Ny, int Nz): Nx(Nx), Ny(Ny), Nz(Nz) 
{
    //Create new array for our spins
    s = new int**[Nx];  //Double check that this works
    for (int i = 0; i < Nx; i++)
    {
        s[i] = new int*[Ny];
        for (int j = 0; j < Ny; j++)
        {
            s[i][j] = new int[Nz];
        }
    }

    //Init our random function
    srand (static_cast <unsigned> (time(0)));  //only call this once to seed the random generator
}

//Initialize our Spin array to all spin up (1)
void icingLattice::initSpinArray()
{
    for (int i = 0; i < Nx; i++)
    {
        for (int j = 0; j < Ny; j++)
        {
            for (int k = 0; k < Nz; k++)
            {
                s[i][j][k] = 1;
            }
        }
    }
}

//Make sure this works (it doesnt, need to sum)
int icingLattice::calcE(int i, int j, int k) 
{
    int Esum = 0;

    //Applying periodic boundary conditions (if needed)
    //For x
    int im = i - 1;
    int ip = i + 1;
    if (i == 0) {im = Nx-1;}
    else if (i == Nx-1) {ip = 0;}
    Esum -= s[i][j][k] * (s[im][j][k] + s[ip][j][k]);

    //For y
    int jm = j - 1;
    int jp = j + 1;
    if (j == 0) {jm = Ny - 1;}
    else if (j == Ny - 1) {jp = 0;}
    Esum -= s[i][j][k] * (s[i][jm][k] + s[i][jp][k]);

    //For z
    int km = k - 1;
    int kp = k + 1;
    if (k == 0) {km = Nz - 1;}
    else if (k == Nz - 1) {kp = 0;}
    Esum -= s[i][j][k] * (s[i][j][km] + s[i][j][kp]);

    return Esum;
}

//Calculates total energy of our lattice
double icingLattice:: calcEtotal()
{
    double Esum;

    //Run through all points and sum energy
    for (int i = 0; i < Nx; i++) {
        for (int j = 0; j < Ny; j++) {
            for (int k = 0; k < Nz; k++) {
                Esum += calcE(i,j,k);
            }
        }
    }

    return (Esum/(6.0*Nx*Ny*Nz));
}

//Calculates total magnetization of our lattice
double icingLattice::calcMagTotal()
{
    double Msum;
    for (int i = 0; i < Nx; i++) {
        for (int j = 0; j < Ny; j++) {
            for (int k = 0; k < Nz; k++) {
                Msum += s[i][j][k];
            }
        }
    }
    return Msum/(static_cast<double>(Nx*Ny*Nz));
}

//Runs through our icing method for our lattice
void icingLattice::run(double temp, int Nsweeps)
{
    for (int N = 0; N < Nsweeps; N++)  //Run through all our sweeps
    {
    for (int i = 0; i < Nx; i++)
    {
        for (int j = 0; j < Ny; j++)
        {
            for (int k = 0; k < Nz; k++)
            {
                int E = -1*calcE(i,j,k);  //Calc our E value
                if (E < 0) {   //Check for first flip condition
                    s[i][j][k] = s[i][j][k] * -1;
                }
                else {
                    //Random number generator
                    double burn = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(1)));  //need this to make the random work
                    double r = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(1)));  //Make random number between 0 and 1

                    double bFact = exp(-E/temp);
                    if (r <= bFact) { //Check for second flip condition
                        s[i][j][k] = s[i][j][k] * -1;
                    }
                }
            }
        }
    }
    }
}

//Deconstructor
icingLattice::~icingLattice()
{
    //Deconstruct our spin array
    for (int i = 0; i < Nx; i++) {
        for (int j = 0; j < Ny; j++) {
            delete[] s[i][j];
        }
        delete[] s[i];
    }
    delete[] s;
}