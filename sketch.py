from mako.template import Template
from sostav import *
import yaml
import subprocess as sp
import os
import re
import matplotlib.pyplot as plt
os.chdir(r'C:\Python\.idea\kp ')
tpl="""
!------------------------------------------------------------------------------!
!    VVER-1000 2 Group Model for Unit 3 of  Kalinin NPP                        !
!      (c) Slava 12 May 2005    MEPhI    Fresh Core                            !
!------------------------------------------------------------------------------!
CNT_RCT_POWR ## REACTOR POWER (MWt)

 ${Q}

CNT_RCT_TYPE ## REACTOR TYPE

 "PWR"

XS_DIFF_FLAG

  1 ## Parameter 1 - Diffusion Coefficient, 0 - 3*Transport XS

XS_NEUT_SPEC

 1.0 0.0 ## xp(NG)

XS_POWR_CONV

 3.204E-11 3.204E-11 ## pow_conv

GMT_CRD_TYPE # Coordinate System ("XYZ" or "HEX-Z")

 "HEXZ"

GMT_NUM_BNDL ## Numbering of the reactor assdemblies (bundles)

 1 9     #1
 1 10    #2
 1 11    #3
 1 12    #4
 1 13    #5
 1 14    #6
 1 15    #7
 1 16    #8
 1 17    #9
 2 17    #10
 3 17    #11
 4 17    #12
 5 17    #13
 6 17    #14
 7 17    #15
 8 17    #16
 9 17    #17


GMT_MSH_RDIR ## Spatial Mesh for HEX Geometry

 9.6  # размер под ключ ТВС в см

GMT_MSH_ZDIR # Spatial Mesh in Z direction

  1 ${Heff}
  1 13. 1 13. 1 13. 1 13. 1 13.
  1 13. 1 13. 1 13.
  1 13. 1 13.
  1 ${Heff1} # npz(NZR),hz(NZR)

GMT_COR_LOAD ## Core Loading with Bundle Types


            5 5 5 5 5 5 5 5 5
           5 5 5 5 5 5 5 5 5 5
          5 5 2 2 2 2 2 2 2 5 5
         5 5 2 2 2 2 2 2 2 4 5 5
        5 5 2 2 2 2 3 2 2 2 2 5 5
       5 5 2 2 2 2 1 1 2 2 2 2 5 5
      5 5 2 2 3 1 1 1 1 1 3 2 2 5 5
     5 5 2 2 2 1 1 1 1 1 1 2 2 2 5 5
    5 5 2 2 2 1 1 1 1 1 1 1 2 2 2 5 5
     5 5 2 2 2 1 1 1 1 1 1 2 2 2 5 5
      5 5 4 2 3 1 1 1 1 1 3 2 4 5 5
       5 5 2 2 2 2 1 1 2 2 2 2 5 5
        5 5 2 2 2 2 3 2 2 2 2 5 5
         5 5 4 2 2 2 2 2 2 2 5 5
          5 5 2 2 2 2 2 2 2 5 5
           5 5 5 5 5 5 5 5 5 5      
            5 5 5 5 5 5 5 5 5        

 5  10*6 5   ## nb = 1  1-ТВС центральной зоны      
 5 8*2 2*7 5   ## nb = 2  2-ТВС переферийной зоны     
 5 10*3 5   ## nb = 3  3-ТВС со стержнем АЗ       
 5 10*4 5   ## nb = 4  4-ТВС с пустым каналом      
 5 10*5 5   ## nb = 5  5-отражатель                
                    
                
GMT_BND_COND ## Boundary Conditions

 1 1  1 1  1 1 ## type of boubdary condition (radial Ext. Dist. - 0, Log. Der. - 1)
 1 1  1 1  1 1  1 1  1 1  1 1  
 1 1 ## type of the axial boundary conditions                                       
 1 1  1 1  ## bound. condit. (axial Ext.Dist.-0, Log.Der.-1)


XS_NEUT_VELC

1.e7 1.e5 ## prompt newtron velocity, cm/s          

XS_BASE_DATA ## Basic set of the Macro Cross Section Data

%for i in range(7):
%if i!=4:
${'%-13s'%D[i].split()[0]}      ${'%-13s'%sabs[i].split()[0]}               ${'%-13s'%nusfis[i].split()[0]}                 ${'%13s'%sfis[i].split()[0]}
${'%-13s'%D[i].split()[1]}      ${'%-13s'%sabs[i].split()[1]}               ${'%-13s'%nusfis[i].split()[1]}                 ${'%13s'%sfis[i].split()[1]}

${'%-13s'%matr[i][0]}    ${'%-13s'%matr[i][1]}  
${'%-13s'%matr[i][2]}    ${'%-13s'%matr[i][3]}                ${i+1}               ${keff[i]}           0.0
%endif
%if i==4:
${'%-13s'%D[i].split()[0]}      ${'%-13s'%sabs[i].split()[0]}               0.00000000000                 0.00000000000
${'%-13s'%D[i].split()[1]}      ${'%-13s'%sabs[i].split()[1]}               0.00000000000                 0.00000000000

${'%-13s'%matr[i][0]}    ${'%-13s'%matr[i][1]}  
${'%-13s'%matr[i][2]}    ${'%-13s'%matr[i][3]}                ${i+1}               ${keff[i]}           0.0
%endif
%endfor

1.202855                 0.1427303E-01             0.00000000000              0.00000000000
0.3138439               0.1904504                    0.00000000000                      0.00000000000

0.5570224                          0.1260717E-03
0.1821472E-01                    1.195485                    8                     1.12153           0.0



1.227625             0.2697776E-01        0.1006361E-01        0.00000000000  0.00000000000
0.3042039          0.2349750                0.2629775                0.00000000000

0.5326820               0.1458579E-03
0.1025493E-01      1.159145                     9                        0.578448



1.195313        0.1460185E-01      0.00000000000      0.00000000000
0.3179431      0.1908335               0.00000000000             0.00000000000 

0.5566648                0.1280322E-03
0.1807053E-01       1.175959                  10               1.09930

"""
def transport(matrix,i):
    L_0 = matrix[i].split()[0]
    L_1 = matrix[i].split()[1]
    L_2 = matrix[i].split()[2]
    L_3 = matrix[i].split()[3]
    matrix.pop()
    matrix.append([L_0,L_2,L_1,L_3])
    return matrix
D=[]
sabs=[]
nusfis=[]
sfis=[]
matr=[]
keff=[]
file=yaml.load(open('forSKETCH.yaml'))
for i in range(1,8):
    D.append(file[str(i)+'_D'])
    sabs.append(file[str(i) + '_sabs'])
    nusfis.append(file[str(i) + '_nusfis'])
    sfis.append(file[str(i) + '_sfis'])
    matr.append(file[str(i)+'_matr'])
    matr=transport(matr,i-1)
    keff.append(file[str(i)+'_keff'])
file=yaml.load(open('datakp.yaml',encoding='utf-8'))
Q=file['Qр']
#Heff=file['Heff']/2*100
Heff=12
Heff1=45
shab = Template(tpl)
pechat=shab.render(Q=Q,Heff=Heff,D=D,sabs=sabs,nusfis=nusfis,sfis=sfis,matr=matr,keff=keff,Heff1=Heff1)
print(pechat)
data=open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Input\my.dat','w')
data.write(pechat)
data.close()
sp.run('SKETCH.exe',cwd=r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor',shell=1)

data=open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Output\SKETCH.lst ').read()
cur=((re.findall('k_ef +\s+\:+(.+)',data)[1].split()))
print(cur)
keff_graph=[]
x=[0]
for i in range(1):

    shab = Template(tpl)
    pechat=shab.render(Q=Q,Heff=Heff,Heff1=Heff1,D=D,sabs=sabs,nusfis=nusfis,sfis=sfis,matr=matr,keff=keff)
    print(pechat)
    data=open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Input\my.dat','w')
    data.write(pechat)
    data.close()


    sp.run('SKETCH.exe',cwd=r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor',shell=1)
    Heff+=2
    data=open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Output\SKETCH.lst ').read()
    cur=((re.findall('k_ef +\s+\:+(.+)',data)[1].split()))
    keff_graph.append(cur)
    x.append(Heff)
x.pop()
# plt.plot(x,keff_graph)
# plt.grid(1)
# plt.xlabel('$Heff$, $см$')
# plt.ylabel('$k_e$$_f$')
print(cur)