import yaml
from math import ceil
import os
#имя файла
name='a.yaml'
nameout='stog.yaml'
numberkart='2'
p={}
os.chdir('C:\Python\.idea\kp')
for i in range(-100,100):
    for j in range(-100,100):
        p[(i,j)]=None
aq=yaml.load(open(name,'r'))
x=aq['kart'+numberkart].split('\n')
for i in range(len(x)):
    for j in range(len(x[i].split())):
        p[(i,j)] =int(x[i].split()[j])
count=[]
matr={}
index=0

for k in aq['symbol'].split(','):
    count.append(int(aq['kart'+numberkart].count(k)*6))
    integ=int(k)
    for  i in range(len(x)-1):
        for j in range(len(x[i].split())):
            if p[(i,j)] == integ:
                if i < ceil((len(x) - 2) / 2):
                     if p[(i - 1, j - 1)] == None:
                         count[index]-=1

                     if p[(i - 1, j)] == None:
                         count[index] -= 1

                     if p[(i, j - 1)] == None:
                         count[index] -= 1

                     if p[(i, j + 1)] == None:
                         count[index] -= 1

                     if p[(i + 1, j + 1)] == None:
                         count[index] -= 1

                     if p[(i + 1, j)] == None:
                         count[index] -= 1

                elif i > ceil((len(x) - 2) / 2):
                    if p[(i - 1, j + 1)] == None:
                         count[index] -= 1
                    if p[(i - 1, j)] == None:
                        count[index] -= 1
                    if p[(i, j - 1)] == None:
                         count[index] -= 1
                    if p[(i, j + 1)] == None:
                         count[index] -= 1
                    if p[(i + 1, j - 1)] == None:
                         count[index] -= 1
                    if p[(i + 1, j)] == None:
                         count[index] -= 1
                else:
                     if p[(i - 1, j - 1)] == None:
                         count[index] -= 1
                     if p[(i - 1, j)] == None:
                         count[index] -= 1
                     if p[(i, j - 1)] == None:
                         count[index] -= 1
                     if p[(i, j + 1)] == None:
                         count[index] -= 1
                     if p[(i + 1, j - 1)] == None:
                         count[index] -= 1
                     if p[(i + 1, j)] == None:
                         count[index] -= 1


    #         if p[(i,j + 1)] == None:
    #             count[index]-=1
    #         if p[(i, j - 1)] == None:
    #             count[index] -= 1
    #         if p[(i + 1, j )] == None:
    #             count[index] -= 1
    #         if p[(i - 1, j )] == None:
    #             count[index] -= 1
    # for corner in [(0,0),(0,len(x[0].split())-1),(len(x)-2, 0),(len(x)-2, len(x[len(x)-2].split())-1)]:
    #      if p[corner] == integ:
    #           count[index] -= 3
    # i=0
    # for j in range(1, len(x[i].split()) - 1):
    #     if p[(i, j)] == integ:
    #         count[index] -= 2
    # i = len(x) - 2
    # for j in range(1, len(x[i].split()) - 1):
    #     if p[(i, j)] == integ:
    #         count[index] -= 2
    # j = 0
    # for i in range(1, len(x) - 2):
    #     if p[(i, j)] == integ:
    #         count[index] -= 2
    # for i in range(1, len(x) - 2):
    #     j = len(x[i].split()) - 1
    #     if p[(i, j)] == integ:
    #         count[index] -= 2
    # for i,j in zip(2*[ceil((len(x)-2)/2)],[0,len(x[ceil((len(x)-2)/2)].split())-1]):
    #     if p[(i, j)] == integ:
    #         count[index] -= 1
    for z in aq['symbol'].split(','):
        integ1 = int(z)
        cur=0
        for i in range(0,len(x)-1):
            for j in range(0,len(x[i].split())):
                if i<ceil((len(x)-2)/2):
                    if p[i,j]== integ:
                         if p[(i-1,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i-1,j)]==integ1:
                             cur += 1 / count[index]
                         if p[(i,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i,j+1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i+1,j+1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i+1,j)]==integ1:
                             cur += 1 / count[index]
                elif i>ceil((len(x)-2)/2):
                    if p[i,j]== integ:
                         if p[(i-1,j+1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i-1,j)]==integ1:
                             cur += 1 / count[index]
                         if p[(i,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i,j+1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i+1,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i+1,j)]==integ1:
                             cur += 1 / count[index]
                else:
                    if p[i,j]== integ:
                         if p[(i-1,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i-1,j)]==integ1:
                             cur += 1 / count[index]
                         if p[(i,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i,j+1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i+1,j-1)]==integ1:
                             cur += 1 / count[index]
                         if p[(i+1,j)]==integ1:
                             cur += 1 / count[index]
        matr[(integ,integ1)]='%0.4f' % cur
    index+=1
k=len(aq['symbol'].split(','))+1

def summ(i,ll,k):
    pruf=0
    for j in range(1,k):
         pruf +=float(ll[(i,j)])
    print('сумма по ',i,'-ой строчке =','%0.2f' % pruf)

for  i in range(1,k):
    summ(i,matr,k)

file=open(nameout,'w')
file.write('for getera : |1'+'\n'+' ')
for i in range (1,k):
    for j in range(1,k):
        file.write(str(matr[(i,j)])+' , ')
    file.write('\n'+' ')
file.close()