#include <iostream>
#include <fstream>
#include <math.h>
#include <iomanip>

using namespace std;

class Tpoint
{
public:
    double t;
    double y;
    int musor;
};
istream& operator>>(istream& s,Tpoint& p)
{
    s>>p.t>>p.y>>p.musor;
    return s;
}

class Tfilter
{
    Tpoint p0,p1;               //p0-точка начала отрезка, p1-последн€€ точка этого отрезка
public:
    ofstream output{"new.dat"};

    double delta,k[2];
    Tfilter(Tpoint p_,double delta_=10)
    {
        delta=delta_;
        p0=p_;
        k[0]=-1e308;
        k[1]=1e308;
        output<<setprecision(18)<<p0.t<<'\t'<<p0.y<<endl;
    }
    ~Tfilter()
    {
      output<<setprecision(18)<<p1.t<<'\t'<<p1.y<<endl;
    }
    void push(const Tpoint& p)   //p- послежн€€ считанна€ точка
    {
        double k_new[2];
        double edt=1./(p.t-p0.t);
        k_new[0]=((p.y-p0.y)-delta)*edt;
        k_new[1]=((p.y-p0.y)+delta)*edt;
        if(k_new[0]>k[1] || k_new[1]<k[0])
        {
            double k_best = (k[1]+k[0])/2;
            p0.y=p0.y+k_best*(p1.t-p0.t);
            p0.t=p1.t;
            p1=p;
            output<<setprecision(18)<<p0.t<<'\t'<<p0.y<<endl;
            k[0]=-1e308;
            k[1]=1e308;

        }
        else
        {
            p1=p;
            if (k_new[0]<k[0] && k_new[1]<k[1]) k[1]=k_new[1];
            else if (k_new[0]>k[0] && k_new[1]<k[1])
            {
                    k[0]=k_new[0];
                    k[1]=k_new[1];
            }
            else if (k_new[0]<k[0] && k_new[1]>k[1]) {}
            else k[0]=k_new[0];
        }
    }
};

class Tfilter_old
{
    Tpoint p0,p1;               //p0-точка начала отрезка, p1-последн€€ точка этого отрезка
public:
    ofstream output{"old.dat"};

    double delta;
    Tfilter_old(Tpoint p_,double delta_=0.1)
    {
        delta=delta_;
        p1=p0=p_;
        output<<setprecision(18)<<p0.t<<'\t'<<p0.y<<endl;
    }
    ~Tfilter_old()
    {
      output<<setprecision(18)<<p1.t<<'\t'<<p1.y<<endl;
    }
    void push(const Tpoint& p)   //p- послежн€€ считанна€ точка
    {
        if (fabs(p0.y-p.y)>delta)
        {
            output<<setprecision(18)<<p.t<<'\t'<<p.y<<endl;
            p1=p0;
            p0=p;
        }
        else p1=p;
    }
};


int main()
{
    ifstream s("C:\\Python\\.idea\\Jpath\\N.TXT ");//ifsteram- входной файловый поток, открытый файл
    Tpoint point;
    s>>point;

    Tfilter flt(point);
    Tfilter_old flt_old(point);
    while(s)
    {
        s>>point;
        flt.push(point);
        flt_old.push(point);
    }
    return 0;
}
