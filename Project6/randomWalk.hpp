#define _USE_MATH_DEFINES
#include <random>
#include <vector>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <fstream>
#include <iostream>
using namespace std;

class Particle
{
    private:
        double position[3];
    
    public:
        Particle();
        void initialize();
        double getXpos();
        double getYpos();
        double getZpos();  //consider making these const
        void setXpos(double x);
        void setYpos(double y);
        void setZpos(double z);
};

class RandomWalk
{
    private:
        double xMax;
        double yMax;
        double zMax;
        double dr;
        string fileName;
        double LO = 0.0;  //not sure if needed
        double HI = 2*M_PI;
        default_random_engine generator;
        uniform_real_distribution<double> dist(double,double);
        vector<double> rSqrdVals;

    public:
        vector<Particle> particles; //does this generate anything or do we need initialize
        RandomWalk(double xMax, double yMax, double zMax, string fileName, int numParticles);
        void walk();
        void run(int numWalks);
        void writeData();
        void clearFile(string filename);
        void calcRSqrd();
        void writeRData();
};