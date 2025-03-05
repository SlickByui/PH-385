#include "randomWalk.hpp"

Particle::Particle() {
    //Set the inital position of our particles when first init
    position[0] = 0;
    position[1] = 0;   
    position[2] = 0;
}

double Particle::getXpos() {
    return position[0];
}

double Particle::getYpos() {
    return position[1];
}

double Particle::getZpos() {
    return position[2];
}

void Particle::setXpos(double x) {
    position[0] = x;
}

void Particle::setYpos(double y) {
    position[1] = y;
}

void Particle::setZpos(double z) {
    position[2] = z;
}


//RandomWalk class
RandomWalk::RandomWalk(double xMax, double yMax, double zMax, string fileName, int numParticles)
                :xMax(xMax), yMax(yMax), zMax(zMax), fileName(fileName) 
{
    //Initialize static 
    dr = 0.025;

    //Set our vector size to match the number of particles we have
    particles.resize(numParticles);  //see if better way (there is)

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
    for (Particle & particle : particles)
    {
        //Choose random angle and save it
        double burn = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(2.0*M_PI)));  //need this to make the random work
        double theta = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(2.0*M_PI)));
        double phi = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/M_PI));

        //Step the particle forward for x, y, and z
        //For x dir
        double dx = dr * cos(theta)*sin(phi);
        double xNew = particle.getXpos() + dx;
        if (xNew > xMax)
        {
            xNew = xNew  -2*(xNew - xMax);  //calc these separately then apply?
        }
        else if (xNew <= -xMax)
        {
            xNew = xNew -2*(xMax-xNew);  //double check this logic
        }
        particle.setXpos(xNew);

        //For y dir
        double dy = dr * sin(theta)*sin(phi);
        double yNew = particle.getYpos() + dy;
        if (yNew > yMax)
        {
            yNew = yNew -2*(yNew-yMax);
        }
        else if (yNew < -yMax)
        {
            yNew = yNew + 2*(yMax - yNew);
        }
        particle.setYpos(yNew);

        //For z dir
        double dz = dr * cos(phi);
        double zNew = particle.getZpos() + dz;
        if (zNew > zMax)
        {
            zNew = zNew - 2*(zNew - zMax);
        }
        else if (zNew < -zMax)
        {
            zNew = particle.getZpos() +2*(zMax - zNew);
        }
        particle.setZpos(zNew);
    }
}

//Function runs through a specified number of walks 
void RandomWalk::run(int numWalks) 
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
    for (Particle & particle: particles) //does this pull from existing list or make new one
    {
        file1 << particle.getXpos() << "    " << particle.getYpos() << "    " << particle.getZpos() << endl;
    }
    //Add two extra endlines to the file
    file1 << endl << endl;
    return;
}

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

void RandomWalk::calcRSqrd()  //Run every instance or run at end of cycle?
{
    //Initialize our rSqrd value
    double rSqrd = 0;
    int N = particles.size();   //num particles
    double ri = 0;
    double rj = 0;

    //Loop through and calc r squared
    for (int i = 0; i < N; i++)
    {
        for (int j = i; j < N; j++)
        {
            //Maybe find way to simplify math?
            ri = sqrt(particles[i].getXpos()*particles[i].getXpos() + particles[i].getYpos()*particles[i].getYpos() 
                        + particles[i].getZpos()*particles[i].getZpos());
            rj = sqrt(particles[j].getXpos()*particles[j].getXpos() + particles[j].getYpos()*particles[j].getYpos() 
                        + particles[j].getZpos()*particles[j].getZpos());
            rSqrd += pow(ri-rj,2);  //square our r vals
        }
    }
    rSqrdVals.push_back(rSqrd/N);  //FIX ME
}

void RandomWalk::writeRData()
{
    int iter = 1;
    for (double & rSqrd: rSqrdVals) //does this pull from existing list or make new one
    {
        file2 << iter << " " << rSqrd << endl;
        iter++;
    }
    return;
}

//Deconstructor
RandomWalk::~RandomWalk()
{
    file1.close();
    file2.close();
}