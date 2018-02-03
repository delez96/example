import yaml
file=open(r'C:\Users\delez\Desktop\DIPLOM\kp\sketch_fast_reactor\Output\SKETCH.lst').read()
index1=file.rfind('2D RADIAL ASSEMBLY-AVERAGED POWER DENSITY')
index2=file.rfind('1D AXIAL AVERAGE POWER DENSITY')
radial=file[index1:index2].split('\n')
matrrad=[]
cur=[]
for i in range(4,17):
    cur.append(radial[i].split(':')[1].split())
for i  in  range(len(cur)):
    for  j in range(len(cur[i])):
        matrrad.append(cur[i][j])
kr=max(matrrad)

axial=file[index2:index2+200]
matrax=[]
cur=[]
axial=axial.split('\n')
for i in range(1,len(axial)):
    cur.append(axial[i])
for i in range(1,len(cur)-1):
    matrax.append(cur[i].split()[1])
kz=max(matrax)
kv=float(kr)*float(kz)

file=open(r'C:\Python\.idea\kp\input.yaml ','w')
file.write('kr'+': '+str(kr)+'\n')
file.write('kz'+': '+'|'+'\n')
for i in range(len(matrax)):
    file.write(' '+matrax[i]+'\n')
file.close()

