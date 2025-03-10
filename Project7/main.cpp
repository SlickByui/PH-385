#include "icingLattice.hpp"
#include <fstream>

void clearFile(std::string filename) {
    std::ofstream file(filename, std::ofstream::out | std::ofstream::trunc);
        if (file.is_open()) {
            file.close(); // Close the file after clearing
            std::cout << "File " << filename << " cleared successfully." << std::endl;
        } else {
            std::cerr << "Error opening file." << std::endl;
        }
        file.close();
}

int main()
{
    //Define our values
    int numSweeps = 100;
    int Ndim = 20;
    std::ofstream file;

    //Clear our file
    clearFile("data.csv");

    //Open our file
    file.open("data.csv");

    //Initialize lattice object
    icingLattice lattice = icingLattice(Ndim,Ndim,Ndim);

    //Loop through temperatures
    for (double temp = 0.01; temp < 4.00; temp += 0.01) {
        lattice.initSpinArray();
        lattice.run(temp,10);
        file << temp << "," << lattice.calcMagTotal() << std::endl;
    }

    file.close();
}