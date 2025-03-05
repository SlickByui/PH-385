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
        std::ofstream file1;
        std::ofstream file2;
        string fileName;
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
        ~RandomWalk();
};