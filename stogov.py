import re
import matplotlib.pyplot as plt
file = open(r'C:\GETERA-93\bin\stogov\tolya\cell-stogov_vver-3.out ', 'r').read()
p = re.findall('keff         nu           mu           fi           teta+\n+\s+([\d\.]+)+', file)
u=re.findall('u235     ([\d\.\-\+\w]+)',file)
gd=re.findall('gd57     ([\d\.\-\+\w]+)',file)
burn=re.findall('burn up = \s+([\d\.\-\+\w]+)',file)
u233=[]
for i in range(len(u)):
    if i%4==1:
        u233.append(u[i])
B=0
burn=[]
for i in range(54):
    burn.append(B)
    B+=1
plt.plot(burn,u233)
plt.grid(1)
plt.xlabel('$Сутки$')
plt.ylabel('$концентрация$ $U_2$$_3$$_3$')
