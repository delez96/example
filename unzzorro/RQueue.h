#ifndef RQueue_h
#define RQueue_h
#include <iostream>

//! очередь из чисел типа T размером N
template <class T,int N>
class RQueue
{
protected:
 T data[N];
 T* p;
 int n;
public:
 RQueue():p(data+N-1),n(0){}
 int full(){return N==n;}
 T& operator[](int i){if(p>=data+N-i){return *(p+i-N);}else{return *(p+i);}}
 T  operator[](int i) const {if(p>=data+N-i){return *(p+i-N);}else{return *(p+i);}}
 T& dropelement(){return (p==data)? *(p+N-1):*(p-1);}
 void push(T el){n++;if(n>N){n=N;}p--;if(p<data){p=data+N-1;}*p=el;}
 void push(){n++;if(n>N){n=N;}if(p<=data){p=data+N-1;}else p--;}
 void flush(){p=data+N-1;n=0;}
 int Count() const {return n;}
 int Size() const {return N;}
 void SetCount(int nn){nn=n;}
};

//! очередь из чисел типа T размер определяется конструктором
template <class T>
class RQueue_n
{
protected:
 int n,N;
 T* data;
 T* p;
public:
 RQueue_n(int N_):
   N(N_),
   data(new T[N]),
   p(data+N-1),
   n(0)
   {}
 ~RQueue_n(){delete [] data;}
 int full() const {return N==n;}
 T& operator[](int i){if(p>=data+N-i){return *(p+i-N);}else{return *(p+i);}}
 T  operator[](int i) const {if(p>=data+N-i){return *(p+i-N);}else{return *(p+i);}}
 T& dropelement(){return (p==data)? *(p+N-1):*(p-1);}
 virtual void push(T el){n++;if(n>N){n=N;}p--;if(p<data){p=data+N-1;}*p=el;}
 virtual void push(){n++;if(n>N){n=N;}if(p<=data){p=data+N-1;}else p--;}
 virtual void flush(){p=data+N-1;n=0;}
 int Count() const {return n;}
 int Size() const {return N;}
};

//! очередь из векторо чисел типа T размер определяется конструктором
template <class T>
class RQueue_n_arr:public RQueue_n<T*>
{
protected:
 void push(T el){}
 T* mydata;
 int Dim;
public:
// virtual void push(){n++;if(n>N){n=N;}p--;if(p<data){p=data+N-1;}}
//Dim - size of vector N - amount of vectors
 RQueue_n_arr(int N_,int Dim_):RQueue_n<T*>(N_),mydata(new T[Size()*Dim_]),Dim(Dim_)
 {
  int i;
  for(i=0;i<N_;i++)
  {
   data[i]=mydata+Dim*i;
  }
 }
 void ptp(std::ostream &s)
 {
  int i;
  for(i=0;i<N;i++)
  {
   s<<data[i]<<std::endl;
  }
 }
 void push()
 {
  RQueue_n<T*>::push();
 }
 void push(const T* val)
 {
  RQueue_n<T*>::push();
  int i;
  T* pp=(*this)[0];
  for(i=0;i<Dim;i++)
  {
    pp[i]=val[i];
  }
 }
 ~RQueue_n_arr(){delete [] mydata;}
 int dimo() const {return n;}
 int dim() const {return Dim;}
};

#include "../matrix/matrix/matrix.h"

template <class T>
class RQueue_as_op:public RQueue_n_arr<T>,public operat<T>
{
public:
  RQueue_as_op(int _dimo, int _dim):RQueue_n_arr<T>(_dimo,_dim){}
  int dim()const{return Dim;}
  int dimo()const{return N;}
};

#endif