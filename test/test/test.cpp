// test.cpp: определяет точку входа для консольного приложения.
//
#include <functional>
#include <iostream>

using namespace std;

class flt
{
public:
	flt * next;
	function<void(double)> next_filter;
	virtual void push(double x) =0;
};

class flt0:public flt
{
public:
	void push(double x) 
	{
		//if(next)next->push(x);
		cout << "flt0" << x << endl;
		next_filter(x);
	}
};

class flt1 :public flt
{
public:
	void push(double x) 
	{
		cout << "flt1" << x << endl;
	}
	void pushtest(double x)
	{
		cout << "flt1 __test" << x << endl;
	}
};

class flt2 :public flt
{
public:
	void push(double x)
	{
		cout << "flt2" << x << endl;
	}
	void pushtest(double x)
	{
		cout << "flt2 __test" << x << endl;
	}
};

int main()
{
		
	flt0 f;
	static flt1 f1;
	static flt2 f2;
	f.next_filter = [](double x) {f1.push(x); f2.push(x); };
	for (int i = 0; i < 500; ++i)
	{
		f.push(i);
	}
    return 0;
}

