#include "randomWalk.hpp"

Particle::Particle() {
    //Set the inital position of our particles when first init
    position[0] = 0;
    position[1] = 0;   
    position[2] = 0;
}

//Getters and setters for our 
double Particle::getPos(int IDX) {return position[IDX];}
void Particle::setPos(int IDX, double val) {position[IDX] = val;}

//RandomWalk class
RandomWalk::RandomWalk(double xMax, double yMax, double zMax, string fileName, int numParticles, int numWalks)
                :xMax(xMax), yMax(yMax), zMax(zMax), fileName(fileName), numParticles(numParticles),numWalks(numWalks) 
{
    //Initialize static step size
    dr = 0.025;

    //Set our vector size to match the number of particles we have
    rSqrdVals = new double[numWalks];
    particles = new Particle[numParticles];

    //Initialize random functionality
    srand (static_cast <unsigned> (time(0)));  //only call this once to seed the random generator

    //Clear our files before using them
    clearFile(fileName);  //clear our file upon class init
    clearFile("rsqrdvals.csv");

    //Open our files
    file1.open(fileName);
    file2.open("rsqrdvals.csv");
}

void RandomWalk::walk()
{
    //Run through each element of our array and choose a random direction
    // to walk it through
    for (int i = 0; i < numParticles; i++)
    {
        //Choose random angle and save it
        double burn = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(2.0*M_PI)));  //need this to make the random work
        double theta = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(2.0*M_PI)));
        double phi = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/M_PI));
        dr = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/0.025));   //sloppy, but should work

        //Step the particle forward for x, y, and z
        //For x dir
        double dx = dr * cos(theta)*sin(phi);
        double xNew = particles[i].getPos(0) + dx;
        if (xNew > xMax)
        {
            xNew += (xMax - xNew);  //calc these separately then apply?
        }
        else if (xNew <= -xMax)
        {
            xNew += (-xMax-xNew);  //double check this logic
        }
        particles[i].setPos(0,xNew);

        //For y dir
        double dy = dr*sin(theta)*sin(phi);
        double yNew = particles[i].getPos(1) + dy;
        if (yNew > yMax)
        {
            yNew += (yMax - yNew);
        }
        else if (yNew < -yMax)
        {
            yNew += (-yMax - yNew);
        }
        particles[i].setPos(1,yNew);

        //For z dir
        double dz = dr * cos(phi);
        double zNew = particles[i].getPos(2) + dz;
        if (zNew > zMax)
        {
            zNew += (zMax - zNew);
        }
        else if (zNew < -zMax)
        {
            zNew += (-zMax - zNew);
        }
        particles[i].setPos(2,zNew);
    }
}

//Function runs through a specified number of walks 
void RandomWalk::run() 
{
    //Write initial cond to file
    writeData();

    //run through our walk function for number of walks
    for (int i = 0; i < numWalks; i++)
    {
        walk();
        writeData();  //Write our current data to our file
        calcRSqrd();
    }

    //Write our RSqrd value
    writeRData();
}

//Writes our data to a file
void RandomWalk::writeData()
{
    for (int i = 0; i < numParticles; i++)
    {
        file1 << particles[i].getPos(0) << "    " << particles[i].getPos(1) << "    " << particles[i].getPos(2) << endl;
    }
    //Add two extra endlines to the file
    file1 << endl << endl;
    return;
}

//Clears the file
void RandomWalk::clearFile(string filename)
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

//Calculates our rSqrd value at the specific step
void RandomWalk::calcRSqrd()
{
    //Initialize our rSqrd value
    double rSqrd = 0;

    //Loop through and calc r squared
    for (int i = 0; i < numParticles; i++)
    {
        for (int j = i+1; j < numParticles; j++)
        {
            for (int k = 0; k < 3; k++)   //need to fix this to work with N dim
            {
                rSqrd += (particles[i].getPos(k) - particles[j].getPos(k))*(particles[i].getPos(k) - particles[j].getPos(k));
            }
        }
    }
    rSqrdVals[R_IDX] = rSqrd/numParticles;
    R_IDX++;
}

//Writes RSqrd data to a file
void RandomWalk::writeRData()
{
    int iter = 1;
    for (int i = 0; i < numWalks; i++)
    {
        file2 << iter << " " << rSqrdVals[i] << endl;
        iter++;
    }
    return;
}

//Deconstructor
RandomWalk::~RandomWalk()
{
    //Close our files
    file1.close();
    file2.close();

    //Delete our arrays
    delete[] rSqrdVals;
    delete[] particles;
}