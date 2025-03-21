#include <cmath>
#include <iostream>
#include <random>
#include <ctime>
#include "molDyn.hpp"

//Constructor for particle class
particle::particle()
{
    //Default start at 0,0 in x,y
    mass = 1; //CHANGE THIS
}

//Deconstructor for particle class
particle::~particle()
{
    //Delete our arrays
    delete[] currentPos;
    delete[] oldPos;
    delete[] vel;
}

//Particle initializer method
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
double particle::getMass() {return mass;}
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
    req = 1;    //equilibrium spacing

    //Initialize our force array
    initForceArray();
    resetForceArray();  //set all force values to zero (might be useless tbh)
}

//Initialize force array
void molDyn::initForceArray()
{
    F = new double**[Nmol];  //Double check that this works
    for (int i = 0; i < Nmol; i++)
    {
        F[i] = new double*[Nmol];
        for (int j = 0; j < Nmol; j++)
        {
            F[i][j] = new double[Ndim];
        }
    }
}

//Reset our force array to zero at all points
void molDyn::resetForceArray()
{
    for (int i = 0; i < Nmol; i++) {
        for (int j = 0; j < Nmol; j++) {
            for (int k = 0; k < Ndim; k++) {
                F[i][j][k] = 0;
            }
        }
    }
}

//Initialize our simulation
void molDyn::initializeSim(double dr, double dt, double v0, std::string filename)
{
    //Initialize row and column index
    int col_IDX = 0;
    int row_IDX = 0;

    //Rounds our number of molecules to nearest int
    int NmolRounded = std::round(std::sqrt(Nmol));

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

    //Displace each particle position and calc randomized velocity
    for (int i = 0; i < Nmol; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            //Calc our displacement and add to current position
            double displacement = particles[i].getCurrentPos(j) + 2*(randDouble(0,1)-0.5)*dr;
            particles[i].setCurrentPos(j,displacement);

            //Calc a randomized velocity
            double dv = 2*(randDouble(0,1)-0.5)*v0;
            particles[i].setVelocity(j,dv);

            //Define fictitious previous position
            double displacement2 = particles[i].getCurrentPos(j) - particles[i].getVelocity(j)*dt;
            particles[i].setOldPos(j,displacement2);
        }
    }

    //DEBUG write initial to file
    writePos();
}

//Write our particle positions to the file
void molDyn::writePos()
{
    //Only works for 2dim for now
    for (int i = 0; i < Nmol; i++)
    {
        file << particles[i].getCurrentPos(0) << "," << particles[i].getCurrentPos(1) << std::endl;
    }
}

//Measure our current temp in e/kB for the current step
double molDyn::currentTemp()
{
    double tempSum = 0;  //Set temp sum init to 0
    
    for (int i = 0; i < Nmol; i++)
    {
        for (int j = 0; j < Ndim; j++)  //Loop over the dimensions we have
        {
            tempSum += particles[i].getVelocity(j)*particles[i].getVelocity(j);
        }
    }
    return (particles[0].getMass() * tempSum/2.0/Nmol);
}

//Update the force matrix 
void molDyn::updateForce()
{
    //Reset our force array to zero (potentially could just do diagonals)
    resetForceArray();  //Diags may not even change, so we might not even need this after first run

    //Loop through our molecules and calculate force pairs between them 
    for (int i = 0; i < Nmol; i++) {
        for (int j = i + 1; j < Nmol; j++) {
            //Find x and y position
            double x = particles[i].getCurrentPos(0) - particles[j].getCurrentPos(0);
            double y = particles[i].getCurrentPos(1) - particles[j].getCurrentPos(1); 

            //Calculate our distance between the two particles
            double r_ij = std::sqrt(x*x + y*y);

            //Check to see if our radius is greater than the cutoff
            if (r_ij < rCutFact*req)
            {
                //Calculate the angle from the x plane of our force
                double theta = std::atan2(y,x);

                //Calculate the force between our two particles (temporary)
                double Ftemp = 24*(2/(pow(r_ij,13)) - 1/(pow(r_ij,7)));

                //Calculate the force components corresponding to the x and y values
                F[i][j][0] = Ftemp * cos(theta);
                F[i][j][1] = Ftemp * sin(theta);

                //Set their "mirror" counterparts equal to one another
                F[j][i][0] = - F[i][j][0];   //note here, the forces between i,j and j,i should be equal and opposite
                F[j][i][1] = - F[i][j][1];
            }
            else {  //Otherwise force is approx 0
                F[j][i][0] = 0;
                F[j][i][1] = 0;
            }
        }
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