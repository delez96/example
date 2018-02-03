from mako.template import Template
from sostav import *
from TS import *
import re
tpl="""
    V-1002, ТВСА, 4.95% (d=0.12), 6 tveg(e=5%,x=3.6%), Zr,                 
  &IZOT
   %for nm,conc in nuclides:
    ${nm}=  ${conc},                                                             
   %endfor                                                                      
  &GEOM                                                                      
    HK=23.6,  HKEY=23.452,  DET_WA=0.026,  HT=1.275,  ISIM=6,  NRYAD=12, 
     %for nm,conc in nuclides:
    ${nm}=    ${conc},                                                            
   %endfor               
    MAP=           26,                                                       
                  25,-50,                                                    
                 25,-50,-50,                                                 
                25,-50,-50,-50,                                             
               25,-50,-50,-50,${'%0.2f'%nuc['O']},35,                               
###              25,-50,-50,-50,-50,-50,                                        
###             25,-50,-50,-50,-50,-50, 29,                                     
###            25,-50,-50,-50,-50,-50,-50,-50,                                  
###           25,-50,-50,-50,-50, 29,-50,-50,-50,                               
###          25,-50,-50,-50,-50,-50,-50,-50,-50,-50,                            
###         25,-50,-50,-50,-50,-50,-50,-50, 29,-50,-50,                         
###        26,-50,-50,-50,-50,-50, 29,-50,-50,-50,-50,27,                                                                                                    
###    DP_FU=3*0.78,                                                            
###    DC_FU=3*0.793,                                                           
"""

data=[["U35",25],["H",15.55]]
nuc={'O':0.5555525}
p='%1.2f' % 1.56787545
ss=p
shab = Template(tpl)
print(shab.render(nuclides=data,nuc=nuc))


from sostav import *
#Расчет воды
x=(2*H+O).ro(0.72)

a()