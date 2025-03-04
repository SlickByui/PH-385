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
    //Set our vector size to match the number of particles we have
    dr = 0.025;     //static step size for now
    particles.resize(numParticles);  //see if better way
    srand (static_cast <unsigned> (time(0)));  //only call this once to seed the random generator
    clearFile(fileName);  //clear our file upon class init
    clearFile("rqrdvals.csv");
}

void RandomWalk::walk()
{
    //Run through each element of our array and choose a random direction
    // to walk it through
    for (Particle & particle : particles)
    {
        //Choose random angle
        double burn = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(2.0*M_PI)));  //need this to make the random work
        double theta = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/(2.0*M_PI)));
        double phi = static_cast <double> (rand()) / (static_cast <double> (RAND_MAX/M_PI));

        //Step the particle forward for x, y, and z
        //For x dir
        double xNew = particle.getXpos() + dr * cos(theta);
        if (xNew >= xMax)
        {
            xNew = particle.getXpos() -2*dr * cos(theta);
        }
        else if (xNew <= -xMax)
        {
            xNew = particle.getXpos() -2*dr * cos(theta);
        }
        
        particle.setXpos(xNew);   //need to implement check for boundary cond

        //For y dir
        double yNew = particle.getYpos() + dr * sin(theta);
        if (yNew >= yMax)
        {
            yNew = particle.getYpos() -2 * dr * sin(theta);
        }
        else if (yNew <= -yMax)
        {
            yNew = particle.getYpos() +2 * dr * sin(theta);
        }
        particle.setYpos(yNew);

        //For z dir
        double zNew = particle.getZpos() + dr * cos(phi);
        if (zNew >= zMax)
        {
            zNew = particle.getZpos() -2 * dr * cos(phi);
        }
        else if (zNew <= -zMax)
        {
            zNew = particle.getZpos() +2 * dr * cos(phi);
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
    std::ofstream outputFile(fileName, std::ios::app);  //Should append to end of file

    if (outputFile.is_open()) {  //Checks to see if the file actually opens
        for (Particle & particle: particles) //does this pull from existing list or make new one
        {
            outputFile << particle.getXpos() << "," << particle.getYpos() << "," << particle.getZpos() << endl;
        }

        //Add two extra endlines to the file
        outputFile << endl << endl;

        outputFile.close();
    } else {
        std::cerr << "Error opening file " << fileName << std::endl;
    }
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
}

void RandomWalk::calcRSqrd()  //Run every instance or run at end of cycle?
{
    //Initialize our rSqrd value
    double rSqrd = 0;
    int N = particles.size();   //num particles

    //Loop through and calc r squared
    for (int i = 0; i < N; i++)
    {
        for (int j = i; j < N; j++)
        {
            //Maybe find way to simplify math?
            double ri = sqrt(particles[i].getXpos()*particles[i].getXpos() + particles[i].getYpos()*particles[i].getYpos() 
                        + particles[i].getZpos()*particles[i].getZpos());
            double rj = sqrt(particles[j].getXpos()*particles[j].getXpos() + particles[j].getYpos()*particles[j].getYpos() 
                        + particles[j].getZpos()*particles[j].getZpos());
            rSqrd += pow(ri-rj,2);  //square our r vals
        }
    }
    rSqrdVals.push_back(rSqrd/N);  //add element to end of array

}

void RandomWalk::writeRData()
{
    std::ofstream outputFile("rqrdvals.csv", std::ios::app);  //Should append to end of file

    if (outputFile.is_open()) {  //Checks to see if the file actually opens
        for (double & rSqrd: rSqrdVals) //does this pull from existing list or make new one
        {
            outputFile << rSqrd << endl;
        }

        outputFile.close();
    } else {
        std::cerr << "Error opening file " << fileName << std::endl;
    }
    return;
}