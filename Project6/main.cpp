#include "randomWalk.hpp"
using namespace std;

int main()
{
    //Define our intial conditions
    double xMax = 0.5;
    double yMax = 0.5;
    double zMax = 0.5;
    int numParticles = 2500;
    int numWalks = 1000;

    string fileName = "data.csv";  //fileName for our large data file

    //Initialize our random walk object
    RandomWalk randomWalk = RandomWalk(xMax,yMax,zMax,fileName,numParticles,numWalks);

    //Run our randomwalk
    randomWalk.run();
}