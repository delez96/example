from mako.template import Template
from sostav import *
import yaml
import subprocess as sp
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
tpl=""":poly                                                                                 
 &vvod                                                                                
 @ 1 tvel  cell@   rcel(1,1)=0.290,0.340,0.504,                                          
                   ncelsos(1,1)=1,4,4                                                 
 @ 2 tvel  cell@   rcel(1,2)=0.290,0.340,0.504,                                          
                   ncelsos(1,2)=1,4,4                                                 
 @ 3 svp-1 cell@   rcel(1,3)=0.290,0.340,0.504,                                          
                   ncelsos(1,3)=4,4,4,                                                
 @ 4 svp-2 cell@   rcel(1,4)=0.180,0.225,0.504,                                        
                   ncelsos(1,4)=4,4,4,                                                
 @ 5 pel       @   rcel(1,5)=0.42,0.48,0.504 @0.290,0.340,0.504
                   ncelsos(1,5)=4,4,4,
 @ 6 KM        @   rcel(1,6)=0.39,0.504,                                               
                   ncelsos(1,6)=4,4,                      
   t=${t}, ${t}, ${t}, ${t}, ${t}, ${t}, ${t}, 
@-----------------------------------------------------------------------              
 troiz=           
   @        1 tv_1     2 tv_2     3 zr_ob_tv 4 h2o      5 svp_      6 pel       7 ob_pel   
 @ *h*  @ 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%h2o['H']} , 0.000000 , 0.000000 , 0.000000 , 
 @ *o*  @ 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%h2o['O']} , 0.000000 , 0.000000 , 0.000000 , 
 @ zr   @ 0.000001 , 0.000001 , 0.000001 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ u233 @ 0.000001 , 0.000001 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ th32 @ 0.000001 , 0.000001 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ o    @ 0.000001 , 0.000001 , 0.000000 , 0.000000 , 0.000001 , 0.000000 , 0.000000 , 
 @ al   @ 0.000001 , 0.000001 , 0.000000 , 0.000000 , 0.000001 , 0.000000 , 0.000000 , 
 @ b-10 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 0.000000 , 
 @ b-11 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 0.000000 ,
 @ c    @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 0.000000 , 
 @ gd57 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 0.000000 , 0.000000 , 
 @ gd55 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 0.000000 , 0.000000 , 
 @ ni   @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 
 @ cr   @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000001 , 
 @ n    @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @ si   @ 0.000001 , 0.000001 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 
 @-----------------------------------------------------------------------              
 ntcell=1,2,3,4,5,6,                                                                  
 krat= 51,18,9,6,7,36,                                                                
 alout=                    
       0.5882 , 0.1373 , 0.1176 , 0.0000 , 0.0000 , 0.1569 ,  
       0.3889 , 0.3333 , 0.0000 , 0.2222 , 0.0556 , 0.0000 ,  
       0.6667 , 0.0000 , 0.0000 , 0.0000 , 0.0000 , 0.3333 ,  
       0.0000 , 0.6667 , 0.0000 , 0.0000 , 0.3333 , 0.0000 ,  
       0.0000 , 0.1429 , 0.0000 , 0.2857 , 0.5714 , 0.0000 ,  
       0.3478 , 0.0000 , 0.1304 , 0.0000 , 0.0000 , 0.5217 ,  
        
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
 &vvod qv=${qv},dtim=5.0,           
 &end                             
:corr                             
 &vvod &end                       
:fier                             
 &vvod &end 

                     
:stop                               
"""
def config(type):
	file = open(r'C:\GETERA-93\bin\CONFIG.DRV').read()
	data = open(r'C:\GETERA-93\bin\CONFIG.DRV', 'w')
	data.write(file[:file.find('INGET')])
	data.write(r'INGET:C:\GETERA-93\bin\my\KLT_')
	data.write(type+'.txt'+'\n')
	data.write(r'OUTGET:C:\GETERA-93\bin\my\KLT_')
	data.write(type+'.out')
	data.close()
	sp.run("getera.exe", cwd=r"C:\GETERA-93\bin", shell=1)
valid=[]
for dl in range(1,2):
    os.chdir(r'C:\Python\.idea\kp')
    x=(2*H+O).ro(0.72*1.52*dl)
    x=x.todict()
    h2o=x
    file=yaml.load(open('datakp.yaml'))
    t = file['средняя температура других материалов(Ц)']
    qv = file['qv']
    shab = Template(tpl)
    pechat=shab.render(qv=qv,t=t,h2o=h2o)

    file=open(r'C:\GETERA-93\bin\my\KLT_Reflect.txt','w')
    file.write(pechat)
    file.close()
    name='Reflect'
    config(name)
    # sp.run('graph.bat', cwd=r'C:\Python\.idea\bat', shell=1)
    # data = open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Output\SKETCH.lst ').read()
    # cur = ((re.findall('k_ef +\s+\:+(.+)', data)[1].split()))
    # valid.append(cur)
# data=yaml.load(open(r'C:\Python\.idea\kp\datakp.yaml'))['Reff']*100
# L=[]
# for i in range(1,2):
#     L.append(i*data)
#
# intr=UnivariateSpline(L,valid,s=0,k=5)
# x_interpol=np.linspace(L[0],L[len(L)-1],100)
# plt.plot(x_interpol,intr(x_interpol))
# plt.grid(1)
# plt.xlabel('$Reff$, $см$')
# plt.ylabel('$k_e$$_f$')
#
