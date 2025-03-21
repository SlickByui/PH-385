#ifndef _MOLDYN_HPP_
#define _MOLDYN_HPP_

#include <fstream>

//Particle class
class particle
{
    //Attributes
    private:
        double * currentPos;
        double * oldPos;
        double * vel;
        double mass;

    //Methods
    public:
        particle();
        ~particle();
        void initialize(int Ndim);
        double getCurrentPos(int IDX);
        void setCurrentPos(int IDX, double value);
        double getOldPos(int IDX);
        void setOldPos(int IDX,double val);
        double getVelocity(int IDX);
        void setVelocity(int IDX, double val);
        double getMass(void);
};

class molDyn
{
    //Attributes
    private:
        double eps;
        double sig;
        int Nmol;
        int Ndim;
        double *dims;
        double rCutFact;
        double req;
        double dr;
        double dt;
        double v0;
        particle * particles;   //list of particles
        double *** F;           // Force list w/ [i][j][comp] corresponding to particles i and j
        std::fstream file;

    //Methods
    private:
        void initForceArray(void);
        void resetForceArray(void);
        void writePos(void);
        double randDouble(double, double);
        void clearFile(std::string filename);
        void updateForce(void);
        //void updatePos();

    public:
        molDyn(int Nmol, int Ndim, double * dims, double rCutFact);
        ~molDyn(void);
        void initializeSim(double dr, double dt, double v0, std::string filename);
        double currentTemp(void);
        //void addEnergy(double E, int numSteps);
        //double measureTemp(int numSteps);
        //void evolve(int numSteps);
};

#endif