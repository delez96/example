from mako.template import Template
from sostav import *
import yaml
import subprocess as sp
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
def mako(choice,material,place):
    tpl=""":poly                                                                                 
 &vvod                                                                                
 @ 1 tvel  cell@   rcel(1,1)=0.290,0.340,0.504,                                          
                   ncelsos(1,1)=1,3,4                                                 
 @ 2 tvel  cell@   rcel(1,2)=0.290,0.340,0.504,                                          
                   ncelsos(1,2)=2,3,4                                                 
 @ 3 svp-1 cell@   rcel(1,3)=0.290,0.340,0.504,                                          
                   ncelsos(1,3)=5,3,4,                                                
 @ 4 svp-2 cell@   rcel(1,4)=0.180,0.225,0.504,                                        
                   ncelsos(1,4)=5,3,4,                                                
                   %if material=='AZ': 
 @ 5 ${material}        @   rcel(1,5)=1.05,1.3,1.400,
                   ncelsos(1,5)=${variant}8,7, 
                   %endif
                   %if material=='pel': 
 @ 5 ${material}       @   rcel(1,5)=0.42,0.48,0.504 @0.290,0.340,0.504
                   ncelsos(1,5)=${variant}4,
                   %endif                                                
 @ 6 KM        @   rcel(1,6)=0.39,0.504,                                               
                   ncelsos(1,6)=3,4,                      
   %if material=='AZ':                                                                                                                               
   t=${t1}, ${t1}, ${t4}, ${t3}, ${t2}, ${t3}, ${t3}, ${t3},
   %endif
   %if material!='AZ':                                                                                                                               
   t=${t1}, ${t1}, ${t4}, ${t3}, ${t2}, ${t3}, ${t3}, 
   %endif          
@-----------------------------------------------------------------------              
 troiz=           
 %if material=='AZ':                                                   
   @        1 tv_1     2 tv_2     3 zr_ob_tv 4 h2o      5 svp_      6 ${material}       7 ob_${material}   8 vozduh
 @ *h*  @ 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%h2o['H']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 ,
 @ *o*  @ 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%h2o['O']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 ,
 @ zr   @ 0.000000 , ${'%0.6f'%tv2['ZR']} , ${'%0.6f'%ob['ZR']} , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['ZR']} , 0.000000 ,
 @ u233 @ ${'%0.6f'%tv1['U233']} , ${'%0.6f'%tv2['U233']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 ,
 @ th32 @ ${'%0.6f'%tv1['TH32']} , ${'%0.6f'%tv2['TH32']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 ,
 @ o    @ ${'%0.6f'%tv1['O']} , ${'%0.6f'%tv2['O']} , 0.000000 , 0.000000 , ${'%0.6f'%svp['O']} , 0.000000 , 0.000000 , ${'%0.6f'%vozd['O']} ,
 @ al   @ ${'%0.6f'%tv1['AL']} , ${'%0.6f'%tv2['AL']} , 0.000000 , 0.000000 , ${'%0.6f'%svp['AL']} , 0.000000 , 0.000000 , 0.000000 ,
 @ b-10 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['B-10']} , 0.000000 , 0.000000 ,
 @ b-11 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['B-11']} , 0.000000 , 0.000000 ,
 @ c    @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['C']} , 0.000000 , 0.000000 ,
 @ gd57 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%svp['GD57']} , 0.000000 , 0.000000 , 0.000000 ,
 @ gd55 @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%svp['GD55']} , 0.000000 , 0.000000 , 0.000000 ,
 @ ni   @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['NI']} , 0.000000 ,
 @ cr   @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%poglot['CR']} , 0.000000 ,
 @ n    @ 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , ${'%0.6f'%vozd['N']} ,
 @ si   @ ${'%0.6f'%tv1['SI']} , ${'%0.6f'%tv1['SI']} , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 , 0.000000 ,
 %endif
 %if material=='pel':                                                   
   @        1 tv_1     2 tv_2     3 zr_ob_tv 4 h2o      5 svp_      6 ${material}       7 ob_${material}   
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
 %endif
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
 &vvod qv=${qv},dtim=5.0,           
 &end                             
:corr                             
 &vvod &end                       
:fier                             
 &vvod &end 

%for i in range(1,num):
@ ${i} step - 50. days!----------     
:burn                             
 &vvod qv=${qv},dtim=50.0,           
 &end                             
:corr                             
 &vvod &end                       
:fier                             
 &vvod &end 
%endfor                      
                     
:stop                               
"""
    os.chdir(r'C:\Python\.idea\kp')
    if material=='AZ':
	    krat='51,18,9,6,1,36,'
    else:
	    krat='51,18,9,6,7,36,'
    if material=='AZ' and choice=='in':
        variant='6,'
    elif material=='AZ' and choice=='out':
        variant='8,'
    elif material=='pel' and choice=='in':
        variant='6,7,'
    elif material=='pel' and choice=='out':
        variant='4,4,'
    num=1
    #Расчет воды#################################################################
    x=(2*H+O).ro(0.72)
    x=x.todict()
    h2o=x
    #zr on obol##################################################################
    x=(ZR*0.99+NB*0.01).ro(6.5)
    x=x.todict()
    ob=x

    #tvl2########################################################################
    x=(TH32*0.92+U233*0.08+2*O).ro(10.1*((5.8**2-2.52**2)/5.8**2))
    y=(AL*0.25+SI*0.75).ro(2.6)
    z=(ZR*0.99+NB*0.01).ro(6.5*(((2.52**2-2.22**2)/5.8**2)))
    x+=y+z
    x=x.todict()
    # y=y.todict()
    # z=z.todict()
    # x.update(y)
    # x.update(z)
    tv2=x
    #tvl1########################################################################
    x=(TH32*0.90+U233*0.10+2*O).ro(10.1*((5.8**2-2.52**2)/5.8**2))
    y=(AL*0.25+SI*0.75).ro(2.6)
    z=(ZR*0.99+NB*0.01).ro(6.5*(((2.52**2-2.22**2)/5.8**2)))
    x=x.todict()
    y=y.todict()
    z=z.todict()
    x.update(y)
    x.update(z)
    tv1=x
    if place=='centr':
        tv2=x
    #svp
    x = (2 * GD55 * 0.078 + 2 * GD57 * 0.091 + GD56 * 2 * 0.685 + O * 3).ro(4)  # ro(4) 0.148 0.157 0.695
    y=(AL).ro(2.6)
    x=x.todict()
    y=y.todict()
    x.update(y)
    svp=x
    #vozduh######################################################################
    x=(2*N*0.75+2*O*0.25).ro(1.2)
    x=x.todict()
    vozd=x
    if material=='AZ':
        x=((B_10 * 0.9 + B_11 * 0.1) * 4 + C).ro(2.5 * (20 / 21) ** 2)
        y=(NI * 0.78 + CR * 0.22).ro(8.3 * (((20 + 1) ** 2 - 20 ** 2) / 21 ** 2))
        z=(ZR * 0.975 + NB * 0.025).ro(6.5)
        x=x.todict()
        y=y.todict()
        z=z.todict()
        x.update(y)
        x.update(z)
        poglot=x
    else:
        if place=='centr':
            x=((B_10 * 0.90*4 + B_11 * 0.10*4) + C).ro(2.5)#2.5
            z=(AL*2+O*3).ro(3.99)
            y=(CR * 0.44 + NI * 0.56).ro(8)#0.44 0.56
            x = x.todict()
            y = y.todict()
            z=z.todict()
            x.update(y)
            x.update(z)
            poglot = x
        else:
            x = ((B_10 * 0.9 * 4 + B_11 * 0.10 * 4) + C).ro(2.5)  # 2.5
            z = (AL * 2 + O * 3).ro(3.99)
            y = (CR * 0.44 + NI * 0.56).ro(8)  # 0.44 0.56
            x = x.todict()
            y = y.todict()
            z = z.todict()
            x.update(y)
            x.update(z)
            poglot = x
    file=yaml.load(open('datakp.yaml',encoding='utf-8'))
    if place=='centr':
        t1=file['средняя температура твэла(Ц)']
        t2=file['средняя температура свп(Ц)']
        t3=file['средняя температура других материалов(Ц)']
        t4 = file['средняя температура оболочки твэла(Ц)']
    else:
        t1 = file['средняя температура твэла(П)']
        t2 = file['средняя температура свп(П)']
        t3 = file['средняя температура других материалов(П)']
        t4 = file['средняя температура оболочки твэла(П)']
    qv=file['qv']
    file=yaml.load(open('getera(П).yaml'))
    matrix=file['for getera'].split('\n')
    shab = Template(tpl)
    pechat=shab.render(material=material,h2o=h2o,ob=ob,variant=variant,tv1=tv1,
                      tv2=tv2,vozd=vozd,svp=svp,poglot=poglot,matrix=matrix,
                       t1=t1,t2=t2,t3=t3,t4=t4,qv=qv,num=num,krat=krat)
    print(pechat)
    os.chdir(r'C:\GETERA-93\bin\my')
    if material=='AZ' and choice=='in'and place=='peref':
        file=open('KLT_PerefwithAZ.txt','w')
    elif material=='AZ' and choice=='out'and place=='peref':
        file=open('KLT_PerefwithoutAZ.txt','w')
    elif material=='pel' and choice=='in'and place=='centr':
        file=open('KLT_Centrwithpel.txt','w')
    elif material=='pel' and choice=='out'and place=='centr':
        file=open('KLT_Centrwithoutpel.txt','w')
    elif material=='pel' and choice=='in'and place=='peref':
        file=open('KLT_Perefwithpel.txt','w')
    elif material=='pel' and choice=='out'and place=='peref':
        file=open('KLT_Perefwithoutpel.txt','w')
    file.write(pechat)
    file.close()

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
# for dl in range(1,11):
mako('in','AZ','peref')
name='PerefwithAZ'
config(name)


mako('out','AZ','peref')
name='PerefwithoutAZ'
config(name)


mako('in','pel','peref')
name='Perefwithpel'
config(name)


mako('out','pel','peref')
name='Perefwithoutpel'
config(name)

mako('in','pel','centr')
name='Centrwithpel'
config(name)


mako('out','pel','centr')
name='Centrwithoutpel'
config(name)

    # sp.run('graph.bat',cwd=r'C:\Python\.idea\bat',shell=1)
    # data = open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Output\SKETCH.lst ').read()
    # cur = ((re.findall('k_ef +\s+\:+(.+)', data)[1].split()))
    # valid.append(cur)

# data=yaml.load(open(r'C:\Python\.idea\kp\datakp.yaml'))['Reff']*100
# L=[]
# for i in range(1,11):
#     L.append(i*data)
#
# intr=UnivariateSpline(L,valid,s=0,k=5)
# x_interpol=np.linspace(L[0],L[len(L)-1],100)
# plt.plot(x_interpol,intr(x_interpol))
# plt.grid(1)
# plt.xlabel('$Reff$, $см$')
# plt.ylabel('$k_e$$_f$')
file=open('KLT_'+name+'.out','r').read()
p=re.findall('keff         nu           mu           fi           teta+\n+\s+([\d\.]+)+',file)
print(p)
