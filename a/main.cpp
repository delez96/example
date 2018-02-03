#include <iostream>
//#define a 5

using namespace std;

namespace x
{
    int bb=3;
}

int f()
{
    return 1;
}
class complex
{
public:
    float re,im;
};

int main()
{
    complex d,c;
    d.re=5;
    d.im=0;
    int b=x::bb;
    int bb=55;

    for(int i=0;i<5;++i)
    {
        int g=4;
     cout << "Hello world!" << endl;
    }
    return 0;
}
