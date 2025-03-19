#include <cmath>
#include <iostream>
#include <random>
#include <ctime>
#include "molDyn.hpp"

particle::particle()
{
    //Default start at 0,0 in x,y
    mass = 1; //CHANGE THIS
}

particle::~particle()
{
    //Delete our arrays
    delete[] currentPos;
    delete[] oldPos;
    delete[] vel;
}

void particle::initialize(int Ndim)
{
    //Create our dynamic arrays based on number of dimensions
    currentPos = new double[Ndim];
    oldPos = new double[Ndim];
    vel = new double[Ndim];
}

//Getters and setters for our position (IDX referers to x, y, z, etc)
double particle::getCurrentPos(int IDX) {return currentPos[IDX];}
double particle::getOldPos(int IDX) {return oldPos[IDX];}
double particle::getVelocity(int IDX) {return vel[IDX];}
void particle::setCurrentPos(int IDX, double val) {currentPos[IDX] = val;}
void particle::setOldPos(int IDX, double val) {oldPos[IDX] = val;}
void particle::setVelocity(int IDX, double val) {vel[IDX] = val;}

//MolDyn constructor
molDyn::molDyn(int Nmol, int Ndim, double * dims, double rCutFact): Nmol(Nmol), Ndim(Ndim), dims(dims), rCutFact(rCutFact)
{
    //Seed our random number generator
    srand (static_cast <unsigned> (time(0)));  

    //Create our particle list
    particles = new particle[Nmol];

    //Set req to be 1 (for now)
    req = 1;
}

//Initialize our simulation
void molDyn::initializeSim(double dr, double dt, double v0, std::string filename)
{
    //Initialize row and column index
    int col_IDX = 0;
    int row_IDX = 0;

    //Rounds our number of molecules to nearest int
    int NmolRounded = std::round(std::sqrt(Nmol));

    //Initialize our particles
    //particles->initialize(Ndim);

    //Clear our file
    clearFile(filename);

    //Open our file
    file.open(filename);   //maybe add protection to this

    //Initialize our positions at equilib in a square
    for (int i = 0; i < Nmol; i++)
    {
        particles[i].initialize(Ndim);
        if (col_IDX >= NmolRounded)
        {
            col_IDX = 0;
            row_IDX++;
        }
        particles[i].setCurrentPos(0,req*col_IDX);
        particles[i].setCurrentPos(1,req*row_IDX);
        col_IDX++;
    }

    //DEBUG write initial to file
    writePos();

    //Displace each particle position and calc randomized velocity
    for (int i = 0; i < Nmol; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            //Calc our displacement and add to current position
            double displacement = particles[i].getCurrentPos(j) + 2*(randDouble(0,1)-0.5);
            particles[i].setCurrentPos(j,displacement);

            //Calc a randomized velocity
            double dv = 2*(randDouble(0,1)-0.5)*particles[i].getVelocity(j);
            particles[i].setVelocity(j,dv);

            //Define fictitious previous position
            double displacement2 = particles[i].getCurrentPos(j) - particles[i].getVelocity(j)*dt;
            particles[i].setOldPos(j,displacement2);
        }
    }
}

//Write our particle positions to the file
void molDyn::writePos()
{
    std::cout << "Writing to file" << std::endl;
    //Only works for 2dim for now
    for (int i = 0; i < Nmol; i++)
    {
        file << particles[i].getCurrentPos(0) << "," << particles[i].getCurrentPos(1) << std::endl;
    }
}

//Random number generator that creates a double between beginning and end
double molDyn::randDouble(double start, double end)
{
    double burn = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(1)));  //need this to make the random work
    return static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(end))); //Make random number between 0 and 1
}

//Clears the file
void molDyn::clearFile(std::string filename)
{
    std::ofstream file(filename, std::ofstream::out | std::ofstream::trunc);
        if (file.is_open()) {
            file.close(); // Close the file after clearing
            std::cout << "File " << filename << " cleared successfully." << std::endl;
        } else {
            std::cerr << "Error opening file." << std::endl;
        }
        file.close();
}