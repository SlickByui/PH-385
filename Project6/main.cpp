#include "randomWalk.hpp"
using namespace std;

int main()
{
    string fileName = "data.csv";
    RandomWalk randomWalk = RandomWalk(0.5,0.5,0.5,fileName,100);
    randomWalk.run(30);
}