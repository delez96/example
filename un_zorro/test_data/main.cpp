#include <fstream>
#include <iostream>
#include <math.h>
#include <stdlib.h>

using namespace std;
int main()
{
        ofstream s("test.dat");
        double noise;
	for (double i=0; i<1e2; i+=1e-2)
		{   
			      noise=double(rand())/(RAND_MAX);
			      s<<i<<'\t'<< (sin(i)+noise) <<endl; //диапазон rand() от 0 до RAND_MAX
		}
	return 0;
}