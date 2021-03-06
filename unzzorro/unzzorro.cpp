#include <iostream>
#include <fstream>
#include <math.h>
#include <iomanip>

using namespace std;
ofstream out_proba, out;

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
	Tpoint P0,P1;//!< точка на выходе фильтра
	bool done;//!< признак что точка на выходе есть.
	virtual void push(const Tpoint& ) = 0;// запихивание входной точки
//	virtual void ini(Tpoint&, Tpoint&) = 0;
};


class Tfilter :public Tbase_filter
{
public:
	Tpoint p0, p1;               //p0-точка начала отрезка, p1-последняя точка этого отрезка
	//	ofstream output{ "new.dat" };
	double delta, k[2];
	Tfilter(Tpoint p_, double delta_ = 10)
	{
		delta = delta_;
		p0 = p_;
		k[0] = -1e308;
		k[1] = 1e308;
		// первую точку выдаем на выход
		done = 0;
		//output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	~Tfilter()
	{
		//		output << setprecision(18) << p1.t << '\t' << p1.y << endl;
	}
	void ini(Tpoint &p_first, Tpoint &p_last)
	{
		p0 = p_first;
		p1 = p_last;
		k[0] = -1e308;
		k[1] = 1e308;
		done = 0;
	}
	void push(const Tpoint& p)   //p- послежняя считанная точка
	{
		double k_new[2];
		double edt = 1. / (p.t - p0.t);
		k_new[0] = ((p.y - p0.y) - delta)*edt;
		k_new[1] = ((p.y - p0.y) + delta)*edt;
		if (k_new[0] > k[1] || k_new[1] < k[0])
		{
			double k_best = (k[1] + k[0]) / 2;
			p0.y = p0.y + k_best * (p1.t - p0.t);
			p0.t = p1.t;
			p1 = p;
			//			output << setprecision(18) << p0.t << '\t' << p0.y << endl;
			k[0] = -1e308;
			k[1] = 1e308;
			done = 1;
		}
		else
		{
			p1 = p;
			if ((k_new[0] >= k[0] && k_new[1] <= k[1]))
			{
				k[0] = k_new[0];
				k[1] = k_new[1];
			}
			else if (k_new[0] <= k[0] && k_new[1] <= k[1])
			{
				k[1] = k_new[1];
			}
			else if (k_new[0] <= k[0] && k_new[1] >= k[1]) {}
			else if (k_new[0] >= k[0] && k_new[1] >= k[1])
			{
				k[0] = k_new[0];
			}
		}
	}
};

class Tfilter_constant :public Tbase_filter
{
	
public:
//	ofstream output{ "constant.dat" };
	Tpoint p0, p1;              // p0-начальная точка, p1- предпоследняя(подается на вход), p -последняя
	Tpoint p_p1, p_p;
	bool flag=0;
	double delta;
	double razn, razn_max_plus, razn_max_minus;
	Tfilter_constant(Tpoint p_, double delta_ = 10)  
	{
		razn = 0;
		razn_max_plus = razn_max_minus = 0;
		delta = delta_;
		p1 = p0 = p_;   
		done =0;
		//	output << setprecision(18) << p0.t << '\t' << p0.y << endl;
	}
	~Tfilter_constant()
	{
//		output << setprecision(18) << p1.t << '\t' << p1.y << endl;
	}
	void ini(Tpoint &p_first, Tpoint &p_last)
	{
		p0 = p_first;
		p1 = p_last;
		razn = 0;
		razn_max_plus = razn_max_minus = 0;
		done = 0;
	}
	void push(const Tpoint& p)  
	{
		flag = 0;
		if (fabs(p0.y - p.y)>delta)
		{
	
//			output << setprecision(18) << p.t << '\t' << p.y << endl;
			p_p = p1; //печать на bifilter;
			p0 = p1;
			p1 = p;
			razn = p0.y - p.y;
			done = 1;
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
				p_p1 = p1; //печать на bifilter;
				flag = 1;
				p0 = p1;
				p1 = p;
				razn = 0;
				razn_max_plus = razn_max_minus = razn;
			}
		}
		else if ((((fabs(razn_max_plus) + fabs(p0.y - p.y)) > delta) || ((fabs(razn_max_minus) + fabs(p0.y - p.y)) >delta)))
		{
			p_p = p1; //печать на bifilter;
			p0 = p1;
			p1 = p;
			razn = p0.y - p.y;
			done = 1;
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
		if (razn > razn_max_plus) { razn_max_plus = razn; }
		else if (razn < razn_max_minus) { razn_max_minus = razn; }
	}
};


class Tbifilter :public Tbase_filter
{
public:
	double op = 0;

	int last;
	Tfilter li_filt;
	Tfilter_constant co_filt;
	Tbifilter(Tpoint p_, double delta_ = 10):li_filt(p_,delta_), co_filt(p_, delta_)
	{
		out << li_filt.p0;
		done = 0;

	}
	~Tbifilter()
	{
		
		double k_best = (li_filt.k[1] + li_filt.k[0]) / 2;
		li_filt.p0.y = li_filt.p0.y + k_best * (li_filt.p1.t - li_filt.p0.t);
		li_filt.p0.t = li_filt.p1.t;
		out << li_filt.p0;	
	}
	void push(const Tpoint& p_in)  
	{

		if (!li_filt.done) { li_filt.push(p_in);  last = 0; }
		if (!co_filt.done) { co_filt.push(p_in);  last = 1; }

		if (li_filt.done && co_filt.done) 
		{
			if (last == 0)
			{
				out << li_filt.p0;
				out << li_filt.p1;
				li_filt.p0 = li_filt.p1;
				done = 1;
				co_filt.ini(li_filt.p0, li_filt.p1);
				li_filt.push(p_in);
				co_filt.push(p_in);
			}
			else
			{
				out << co_filt.p_p;
				li_filt.ini(co_filt.p0, co_filt.p1);
				if (co_filt.flag)
				{
					out << co_filt.p_p1;
				}
				co_filt.push(p_in);
				li_filt.push(p_in);
				done = 1;
			}
			li_filt.done = 0;
			co_filt.done = 0;

		}
		
/*		if (li_filt.done && co_filt.done)
		{
			done = 1;
			if (last==0)
			{
				co_filt.ini(li_filt.p0, li_filt.p1);
				out << li_filt.p0;
				out << li_filt.p1;
				//if (op >= p.t) { p.t += 1e-5; op = p.t; }
				//else { op = p.t; }
				//out_proba << p;
			}
			else 
			{
				li_filt.ini(co_filt.p0, co_filt.p1);
				out << co_filt.p1;
				//Tpoint p_pechat;

				//p_pechat.t = co_filt.p1.t;
				//p_pechat.y = co_filt.p0.y;


				//if (op >=p_pechat.t) { p_pechat.t += 1e-5; op = p_pechat.t; }
				//else { op = p_pechat.t; }
				//out_proba << p_pechat;


				//if (op >=p.t) { p.t += 1e-5; op = p.t; }
				//else { op = p.t; }
				//out_proba << p;
			}
			co_filt.done = 0;
			li_filt.done = 0;
		}*/
		
	}

};


int main()
{
	ifstream s("..\\data\\N_N.TXT ");//ifsteram- входной файловый поток, открытый файл
	out.open("bifilt.txt");
	out_proba.open("proba.dat");
	Tpoint point;
	s >> point;
	double del = 5.0;
	
	Tbifilter flt(point, del);

	while (s)
	{
		s >> point;
		flt.push(point);
		if (flt.done)
		{
		//	out << flt.P0;
			flt.done = 0;
		}
	}
	return 0;
}
