#define _USE_MATH_DEFINES
#include <random>
#include <vector>
#include <math.h>
#include <cstdlib>
#include <ctime>
#include <iostream>
using namespace std;

void testThing()
{

}

int main()
{
    srand (static_cast <unsigned> (time(0)));  //only call this once to seed the random generator
    //float theta = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/M_PI));

    float phi;
    float theta;
    float sumit = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/M_PI));  //if runs, following work
    phi = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/M_PI));
    theta = static_cast <float> (rand()) / (static_cast <float> (RAND_MAX/(2*M_PI)));

    cout << "Phi = " << phi << '\n';
    cout << "Theta = " << theta << '\n';
}