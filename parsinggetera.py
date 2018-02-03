import yaml
import re
import os
os.chdir(r'C:\Python\.idea\kp ')
data=open('forSKETCH.yaml','w')
data.close()
def sketch(nameout,type):
    data=open('forSKETCH.yaml').read()
    file=open('forSKETCH.yaml','w')
    file.write(data+'\n')
    data=open(nameout).read()
    p=re.findall('flux 1/cm2c+.+\n+(.+)+\n+(.+)+',data)
    matr=re.findall('i / j -->            1           2+\n+\s+\w+\s+\w+\s+(.+)+\n+\s+\w+\s+\w+\s+(.+)+',data)
    sabs=[]
    sfis=[]
    nusfis=[]
    D=[]
    for i in range(len(p[0])):
        sabs.append(p[0][i].split()[3])
        sfis.append(p[0][i].split()[4])
        nusfis.append(p[0][i].split()[5])
        D.append(p[0][i].split()[6])
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

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_Centrwithoutpel.out ',type='1')

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_Perefwithoutpel.out  ',type='2')

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_PerefwithAZ.out ',type='3')

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_PerefwithoutAZ.out ',type='4')

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_Reflect.out ',type='5')

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_Centrwithpel.out ',type='6')

sketch(nameout = r'C:\GETERA-93\bin\my\KLT_Perefwithpel.out ',type='7')


data=open(r'C:\GETERA-93\bin\my\KLT_Centrwithoutpel.out').read()
