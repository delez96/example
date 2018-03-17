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
istream& operator>>(istream& s, Tpoint& p)
{
	s >> p.t >> p.y >> p.musor;
	return s;
}
ostream& operator<<(ostream& s, Tpoint& p)
{
	s << setprecision(18) << p.t << '\t' << p.y << endl;
	return s;
}

class Tbase_filter
{
public:
	Tbase_filter() :done(0) {}
	Tpoint p;//!< точка на выходе фильтра
	bool done;//!< признак что точка на выходе есть.
	virtual void push(const Tpoint& ) = 0;// запихивание входной точки
};

class Tfilter:public Tbase_filter
{
	Tpoint p0, p1;               //p0-точка начала отрезка, p1-последняя точка этого отрезка
public:
//	ofstream output{ "new.dat" };
	bool beg_line;
	double delta, k[2];
	Tfilter(Tpoint p_, double delta_ = 10)
	{
		beg_line = false;
		delta = delta_;
		p0 = p_;
		k[0] = -1e308;
		k[1] = 1e308;
	// первую точку выдаем на выход
		p = p0;
		done = 1;

		//output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	~Tfilter()
	{
//		output << setprecision(18) << p1.t << '\t' << p1.y << endl;
	}
	void push(const Tpoint& p)   //p- послежняя считанная точка
	{
		double k_new[2];
		double edt = 1. / (p.t - p0.t);
		k_new[0] = ((p.y - p0.y) - delta)*edt;
		k_new[1] = ((p.y - p0.y) + delta)*edt;
		if (beg_line || k_new[0]>k[1] || k_new[1]<k[0])
		{
			double k_best = (k[1] + k[0]) / 2;
			p0.y = p0.y + k_best * (p1.t - p0.t);
			p0.t = p1.t;
			p1 = p;
			Tbase_filter :: p = p0;
			done = 1;
			//			output << setprecision(18) << p0.t << '\t' << p0.y << endl;
			k[0] = -1e308;
			k[1] = 1e308;

		}
		else
		{
			p1 = p;
			if (k_new[0]<k[0] && k_new[1]<k[1]) k[1] = k_new[1];
			else if (k_new[0]>k[0] && k_new[1]<k[1])
			{
				k[0] = k_new[0];
				k[1] = k_new[1];
			}
			else if (k_new[0]<k[0] && k_new[1]>k[1]) {}
			else k[0] = k_new[0];
		}
	}
};

class Tfilter_constant :public Tbase_filter
{
	Tpoint p0, p1;              // p0-начальная точка, p1- предпоследняя(подается на вход), p -последняя
public:
//	ofstream output{ "constant.dat" };

	double delta;
	Tfilter_constant(Tpoint p_, double delta_ = 10)  
	{
		delta = delta_;
		p1 = p0 = p_;   
		p = p0;
		done = 1;
		//	output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	~Tfilter_constant()
	{
//		output << setprecision(18) << p1.t << '\t' << p1.y << endl;
	}
	void push(const Tpoint& p)  
	{
		if (fabs(p0.y - p.y)>delta)
		{
			Tbase_filter ::p = p0;
			done = 1;
//			output << setprecision(18) << p.t << '\t' << p.y << endl;
			p1 = p0; 
			p0 = p;
		}
		else p1 = p;
	}
};

class Tbifilter :public Tbase_filter
{
public:
	int last;
	Tfilter li_filt;
	Tfilter_constant co_filt;
	Tbifilter(Tpoint p_, double delta_ = 10):li_filt(p,delta_), co_filt(p, delta_)
	{

	}
	void push(const Tpoint& p_in)  
	{
		if (!li_filt.done) { li_filt.push(p_in);  last = 0; }
		if (!co_filt.done) { co_filt.push(p_in);  last = 1; }
		
		if (li_filt.done && co_filt.done)
		{
			done = 1;
			if (last==0)
			{
				p = co_filt.p;
				li_filt.push(p);
			}
			else 
			{
				p = li_filt.p;
				co_filt.push(p);
			}
			co_filt.done = 0;
			li_filt.done = 0;
		}
		
	}

};


int main()
{
	ifstream s("..\\data\\N_N.TXT ");//ifsteram- входной файловый поток, открытый файл
	ofstream out("bifilt.txt");
	Tpoint point;
	s >> point;
	double del = 5;
	
	Tbifilter flt(point, del);
	while (s)
	{
		s >> point;
		flt.push(point);
		if (flt.done)
		{
			out << flt.p;
			flt.done = 0;
		}
	}
	return 0;
}
