#include <iostream>
#include <fstream>
#include <math.h>
#include <iomanip>

using namespace std;
double delta_ = 10;
class Tpoint
{
public:
	double t;
	double y;
	double musor;
};
istream& operator>>(istream& s, Tpoint& p)
{
	s >> p.t >> p.y >> p.musor;
	return s;
}

class Tfilter
{
	Tpoint p0, p1;               //p0-точка начала отрезка, p1-последняя точка этого отрезка
public:
	ofstream output{ "new.dat" };

	double delta, k[2];
	Tfilter(Tpoint p_)
	{
		delta = delta_;
		p0 = p_;
		k[0] = -1e308;
		k[1] = 1e308;
		output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	~Tfilter()
	{
		double k_best = (k[1] + k[0]) / 2;
		p0.y = p0.y + k_best * (p1.t - p0.t);
		p0.t = p1.t;
		output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	void push(const Tpoint& p)   //p- последняя считанная точка
		{
		double k_new[2];
		double edt = 1. / (p.t - p0.t);
		k_new[0] = ((p.y - p0.y) - delta)*edt;
		k_new[1] = ((p.y - p0.y) + delta)*edt;
		if (k_new[0]>k[1] || k_new[1]<k[0])
		{
			double k_best = (k[1] + k[0]) / 2;
			p0.y = p0.y + k_best * (p1.t - p0.t);
			p0.t = p1.t;
			p1 = p;
			output << setprecision(18) << p0.t << '\t' << p0.y << endl;
			output << setprecision(18) << p1.t << '\t' << p1.y << endl;
			p0 = p1;
			//edt = 1. / (p1.t - p0.t);
			//k[0] = ((p1.y - p0.y) - delta)*edt;
			//k[1] = ((p1.y - p0.y) + delta)*edt;
			k[0] = -1e308;
			k[1] = 1e308;
		}
		else
		{
			p1 = p;
			if ( (k_new[0]>=k[0] && k_new[1]<=k[1])  )
			{
				k[0] = k_new[0];
				k[1] = k_new[1];
			}
			else if (k_new[0] <= k[0] && k_new[1] <= k[1]) 
			{
				k[1] = k_new[1];
			}
			else if (k_new[0]<=k[0] && k_new[1]>=k[1]){}
			else if (k_new[0] >= k[0] && k_new[1] >= k[1]) 
			{
				k[0] = k_new[0];
			}
		}
	}
};

class Tfilter_old
{
	Tpoint p0, p1;               //p0-точка начала отрезка, p1-последняя точка этого отрезка
public:
	ofstream output{ "old.dat" };
	double razn, razn_max_plus, razn_max_minus;
	double delta;
	Tfilter_old(Tpoint p_)
	{
		razn = 0;
		razn_max_plus = razn_max_minus = 0;
		delta = delta_;
		p1 = p0 = p_;
		output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	~Tfilter_old()
	{
		output << setprecision(18) << p1.t << '\t' << p1.y << endl;
	}
	void push(const Tpoint& p)   //p- послежняя считанная точка
	{
		if (fabs(p0.y - p.y) > delta)
		{
			output << setprecision(18) << p1.t << '\t' << p1.y << endl;
			p0 = p1;
			p1 = p;
			razn = p0.y - p.y;
			if (razn > 0)
			{
				razn_max_plus = razn;
				razn_max_minus = 0;
			}
			else 
			{
				razn_max_minus = razn;
				razn_max_plus = 0;
			}
			if (fabs(p0.y - p.y) > delta)
			{
				output << setprecision(18) << p1.t << '\t' << p1.y << endl;
				p0 = p1;
				p1 = p;
				razn = 0;
				razn_max_plus = razn_max_minus = razn;
			}
		}
		else if ((((fabs(razn_max_plus) + fabs(p0.y - p.y)) > delta) || ((fabs(razn_max_minus)+fabs(p0.y - p.y)) >delta)))
		{
			output << setprecision(18) << p1.t << '\t' << p1.y << endl;
			p0 = p1;
			p1 = p;
			razn = p0.y - p.y;
			if (razn > 0)
			{
				razn_max_plus = razn;
				razn_max_minus = 0;
			}
			else
			{
				razn_max_minus = razn;
				razn_max_plus = 0;
			}
		
		}
			
		else p1 = p;
		razn = p0.y - p.y;
		if (razn > razn_max_plus) {razn_max_plus = razn;}
		else if (razn < razn_max_minus) { razn_max_minus = razn;}
		
		
	}
};


int main()
{
	ifstream s("C:\\Users\\User\\Desktop\\cplusplus\\data\\N_N.txt");//ifsteram- входной файловый поток, открытый файл
	Tpoint point;
	s >> point;

	Tfilter flt(point);
	Tfilter_old flt_old(point);
	while (s)
	{
		s >> point;
		flt.push(point);
		flt_old.push(point);
	}
	return 0;
}
