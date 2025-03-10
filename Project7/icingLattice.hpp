#ifndef ICINGLATTICE_HPP
#define ICINGLATTICE_HPP

#include <cmath>
#include <iostream>
#include <random>
#include <ctime>

class icingLattice
{
    private:
        int Nx;
        int Ny;
        int Nz;
        int *** s;

    public:
        icingLattice(int Nx, int Ny, int Nz);
        void initSpinArray();
        void testSpinArr();
        int calcE(int i, int j, int k);
        double calcEtotal();
        double calcMagTotal();
        void run(double temp, int Nsweeps);
        ~icingLattice();
};

#endif