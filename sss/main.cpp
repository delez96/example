#include <iostream>

using namespace std;
void f1(int i)
{
    cout<<i<<endl;

}
using fp =void (int);
using fpp =void(fp);

void f2(fp f)
{
    f(3);
//    cout<<"asdasd"<<i<<endl;
}

void f3(fpp f )
{
    f(f1);
}
void Demonstrarion()
{
    cout << "BRILK";
}

void d(int i)
{


}

extern "C"
{
void d(double i)
{


}

}
int main()
{
    f3(f2);
    return 0;
}

