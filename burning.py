from mako.template import Template
from sostav import *
import yaml
import subprocess as sp
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline



tpl = """:poly                                                                                 
 &vvod                                                                                
 @ 1 tvel  cell@   rcel(1,1)=0.290,0.340,0.504,                                          
                   ncelsos(1,1)=1,3,4                                                 
 @ 2 tvel  cell@   rcel(1,2)=0.290,0.340,0.504,                                          
                   ncelsos(1,2)=2,3,4                                                 
 @ 3 svp-1 cell@   rcel(1,3)=0.290,0.340,0.504,                                          
                   ncelsos(1,3)=5,3,4,                                                
 @ 4 svp-2 cell@   rcel(1,4)=0.180,0.225,0.504,                                        
                   ncelsos(1,4)=5,3,4,                                                 
 @ 5 pel       @   rcel(1,5)=0.42,0.48,0.504 @0.290,0.340,0.504
                   ncelsos(1,5)=4,4,4,
                                                
 @ 6 KM        @   rcel(1,6)=0.39,0.504,                                               
                   ncelsos(1,6)=3,4,                                                                                                                                                     
   t=${t1}, ${t1}, ${t4}, ${t3}, ${t2}, ${t3}, ${t3}, 
@-----------------------------------------------------------------------              
 troiz=                                                              
   @        1 tv_1     2 tv_2     3 zr_ob_tv 4 h2o      5 svp_      6 pel       7 ob_pel   
 @ *h*  @ 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%h2o['H']} , 0.000000 , 0.000000 , 0.000000 , 
 @ *o*  @ 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%h2o['O']} , 0.000000 , 0.000000 , 0.000000 , 
 @ zr   @ 0.000000 , 0.000000 , ${'%0.6f'%ob['ZR']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ u233 @ ${'%0.6f'%tv1['U233']} , ${'%0.6f'%tv2['U233']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ th32 @ ${'%0.6f'%tv1['TH32']} , ${'%0.6f'%tv2['TH32']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ o    @ ${'%0.6f'%tv1['O']} , ${'%0.6f'%tv2['O']} , 0.000000 , 0.000000 , ${'%0.6f'%svp['O']} , 0.000000 , 0.000000 , 
 @ al   @ ${'%0.6f'%tv1['AL']} , ${'%0.6f'%tv2['AL']} , 0.000000 , 0.000000 , ${'%0.6f'%svp['AL']} , 0.000000 , 0.000000 , 
 @ b-10 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['B-10']} , 0.000000 , 
 @ b-11 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['B-11']} , 0.000000 ,
 @ c    @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['C']} , 0.000000 , 
 @ gd57 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%svp['GD57']} , 0.000000 , 0.000000 , 
 @ gd55 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%svp['GD55']} , 0.000000 , 0.000000 , 
 @ ni   @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['NI']} , 
 @ cr   @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['CR']} , 
 @ n    @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ si   @ ${'%0.6f'%tv1['SI']} , ${'%0.6f'%tv1['SI']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @-----------------------------------------------------------------------              
 ntcell=1,2,3,4,5,6,                                                                  
 krat= ${krat}                                                                
 alout=                    
 %for i in matrix:
       ${i} 
 %endfor                                                                                                                                                 
 material(1)='chmc',                                                                  
 &end                                                                                 
*h*    
*o* 
zr  
u233                                                                                 
th32                                                                                                                                                                    
o                                                                                    
al                                                                                   
b-10
b-11                                                                                 
c                                                                                                                                                                        
gd57                                                                                 
gd55                                                                                 
ni                                                                                   
cr                                                                                   
n                                                                                 
si  
****                                                                                  
:corr                                                                                 
 &vvod &end                                                                           
:fier                                                                                 
 &vvod &end                                                                           
:macro                                                                                
 &vvod                                                                                
  ET=10.5E+6,2.15,2.15,0.,                                                            
 NBV=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,                                                    
 &end                                                                                 
@:stop@                                                                               
:dina                                                                                 
 &vvod                                                                                
 &end                                                                                 

:fier                                                                                 
 &vvod &end                                                                           

@:stop                                                                                 

@ 0 step - 5. days!----------     
:burn                             
 &vvod qv=${qv},dtim=3.0,           
 &end                             
:corr                             
 &vvod &end                       
:fier                             
 &vvod &end 
:macro
 &vvod &end 
 
%for i in range(1,num):
@ ${i} step - 50. days!----------     
:burn                             
 &vvod qv=${qv},dtim=3.0,           
 &end                             
:corr                             
 &vvod &end                                                                                      
:fier                             
 &vvod &end 
:macro
 &vvod &end 

%endfor                      

:stop                               
"""
os.chdir(r'C:\Python\.idea\kp')
krat = '129,21,18,12,19,61,'
num = 35*10
# Расчет воды#################################################################
x = (2 * H + O).ro(0.72)
x = x.todict()
h2o = x
# zr on obol##################################################################
x = (ZR * 0.99 + NB * 0.01).ro(6.5)
x = x.todict()
ob = x

# tvl2########################################################################
x = (TH32 * 0.92 + U233 * 0.08 + 2 * O).ro(10.1 * ((5.8 ** 2 - 2.52 ** 2) / 5.8 ** 2))
y = (AL * 0.25 + SI * 0.75).ro(2.6)
z = (ZR * 0.99 + NB * 0.01).ro(6.5 * (((2.52 ** 2 - 2.22 ** 2) / 5.8 ** 2)))
x += y + z
x = x.todict()
# y=y.todict()
# z=z.todict()
# x.update(y)
# x.update(z)
tv2 = x
# tvl1########################################################################
x = (TH32 * 0.90 + U233 * 0.10 + 2 * O).ro(10.1 * ((5.8 ** 2 - 2.52 ** 2) / 5.8 ** 2))
y = (AL * 0.25 + SI * 0.75).ro(2.6)
z = (ZR * 0.99 + NB * 0.01).ro(6.5 * (((2.52 ** 2 - 2.22 ** 2) / 5.8 ** 2)))
x = x.todict()
y = y.todict()
z = z.todict()
x.update(y)
x.update(z)
tv1 = x
# svp
x = (2 * GD55 * 0.078 + 2 * GD57 * 0.091 + GD56 * 2 * 0.685 + O * 3).ro(4)  # ro(4) 0.148 0.157 0.695
y = (AL).ro(2.6)
x=x+y
x=x.todict()
svp = x
# vozduh######################################################################
x = (2 * N * 0.75 + 2 * O * 0.25).ro(1.2)
x = x.todict()
vozd = x
x = ((B_10 * 0.802 * 4 + B_11 * 0.198 * 4) + C).ro(2.5)  # 2.5
z = (AL * 2 + O * 3).ro(3.99)
y = (CR * 0.44 + NI * 0.56).ro(8)  # 0.44 0.56
x = x.todict()
y = y.todict()
z = z.todict()
x.update(y)
x.update(z)
poglot = x
file = yaml.load(open('datakp.yaml', encoding='utf-8'))

t1_1 = float(file['средняя температура твэла(Ц)'])
t2_1 = float(file['средняя температура свп(Ц)'])
t3_1 = float(file['средняя температура других материалов(Ц)'])
t4_1 = float(file['средняя температура оболочки твэла(Ц)'])

t1_2 = float(file['средняя температура твэла(П)'])
t2_2 = float(file['средняя температура свп(П)'])
t3_2 = float(file['средняя температура других материалов(П)'])
t4_2 = float(file['средняя температура оболочки твэла(П)'])
t1=(t1_1+t1_2)/2
t2=(t2_1+t2_2)/2
t3=(t3_1+t3_2)/2
t4=(t4_1+t4_2)/2
qv = file['qv']
file = yaml.load(open('proba.yaml'))
matrix = file['for getera'].split('\n')
shab = Template(tpl)
pechat = shab.render( h2o=h2o, ob=ob,  tv1=tv1,
                     tv2=tv2, vozd=vozd, svp=svp, poglot=poglot, matrix=matrix,
                     t1=t1, t2=t2, t3=t3, t4=t4, qv=qv, num=num, krat=krat)
print(pechat)
os.chdir(r'C:\GETERA-93\bin\my')
file = open('KLT_burning.txt', 'w')
file.write(pechat)
file.close()


file = open(r'C:\GETERA-93\bin\CONFIG.DRV').read()
data = open(r'C:\GETERA-93\bin\CONFIG.DRV', 'w')
data.write(file[:file.find('INGET')])
data.write(r'INGET:C:\GETERA-93\bin\my\KLT_')
data.write('burning.txt' + '\n')
data.write(r'OUTGET:C:\GETERA-93\bin\my\KLT_')
data.write('burning.out')
data.close()
sp.run("getera.exe", cwd=r"C:\GETERA-93\bin", shell=1)


file = open('KLT_burning.out', 'r').read()
p = re.findall('keff         nu           mu           fi           teta+\n+\s+([\d\.]+)+', file)
u=re.findall('u233     ([\d\.\-\+\w]+)',file)
gd=re.findall('gd57     ([\d\.\-\+\w]+)',file)
burn=re.findall('burn up = \s+([\d\.\-\+\w]+)',file)
u233=[]
for i in range(len(u)):
    if i%2==0:
        u233.append(u[i])
# plt.plot(B,u233[2:])
# plt.grid(1)
# plt.xlabel('$Сутки$')
# plt.ylabel('$концентрация$ $U_2$$_3$$_3$')

gd57=[]
# for i in range(2,len(gd)):
#     if i%4==2:
#         gd57.append(gd[i])
# plt.plot(B,gd57[:-1])
# plt.grid(1)
# plt.xlabel('$Сутки$')
# plt.ylabel('$концентрация$ $Gd_5$$_7$')

print(p)
B=[3]

for i in range(len(p[3:])):
    B.append(3*(i+1))

plt.plot(B,p[2:])
plt.plot(burn,p[2:len(p)])
plt.grid(1)
plt.xlabel(r'$Выгорание,$ ${}\frac {{МВт сут}}{{кг U}}$')
plt.ylabel('$K_\infty $')

plt.grid(1)
plt.xlabel('$Сутки$')
plt.ylabel('$K_\infty $')
#
# spl=UnivariateSpline(B,p[2:],s=0,k=3)
# plt.plot(np.linspace(B[0],B[len(B)-1],1000),spl(np.linspace(B[0],B[len(B)-1],1000)))
# interpol=spl(np.linspace(B[0],B[len(B)-1],1000))
for i in range(len(interpol)):
    if (interpol[i]-1.002) <1e-6:
        print(np.linspace(B[0],B[len(B)-1],1000)[i])
        break
x=[]
for i in range(len(p)):
    x.append(abs(float(p[i])-1))
for i in range(100):
    if x[i]==np.partition(x, 0)[0]:
        k=i-6
        print(k)
        break

os.chdir(r'C:\Python\.idea\kp ')

def sketch(k,nameout,type):
    file=open('burn_sketch.yaml','w')
    data=open(nameout).read()
    p=re.findall('flux 1/cm2c+.+\n+(.+)+\n+(.+)+',data)
    matr=re.findall('i / j -->            1           2+\n+\s+\w+\s+\w+\s+(.+)+\n+\s+\w+\s+\w+\s+(.+)+',data)
    sabs=[]
    sfis=[]
    nusfis=[]
    D=[]
    for i in range(len(p[k])):
        sabs.append(p[k][i].split()[3])
        sfis.append(p[k][i].split()[4])
        nusfis.append(p[k][i].split()[5])
        D.append(p[k][i].split()[6])
    file.write('\n'+type+'_'+'sabs'+' : |'+'\n')
    [file.write(' '+i+'\n') for i in sabs]
    file.write('\n'+type + '_' + 'sfis' + ' : |' + '\n')
    [file.write(' '+i + '\n') for i in sfis]
    file.write('\n'+type + '_' + 'nusfis' + ' : |' + '\n')
    [file.write(' '+i + '\n') for i in nusfis]
    file.write('\n'+type + '_' + 'D' + ' : |' + '\n')
    [file.write(' '+i + '\n') for i in D]
    file.write('\n'+type+'_matr'+' : |'+'\n')
    [file.write(' '+i+'\n')for i  in matr[0]]
    x = re.findall('keff+.+\n+\s+([\.\d\+\-\w]+)+', data)
    file.write('\n'+type+'_keff'+' : '+str(x[0]))
    file.close()
sketch(k,nameout = r'C:\GETERA-93\bin\my\KLT_burning.out ',type='8')
