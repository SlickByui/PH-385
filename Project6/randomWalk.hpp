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
        double getPos(int IDX);
        void setPos(int IDX, double val);
};

class RandomWalk
{
    private:
        double xMax;
        double yMax;
        double zMax;
        double dr;
        int numWalks;
        int numParticles;
        int R_IDX;
        std::ofstream file1;
        std::ofstream file2;
        string fileName;
        double * rSqrdVals;
        Particle * particles;

    public:
        RandomWalk(double xMax, double yMax, double zMax, string fileName, int numParticles, int numWalks);
        void walk();
        void run();
        void writeData();
        void clearFile(string filename);
        void calcRSqrd();
        void writeRData();
        ~RandomWalk();
};