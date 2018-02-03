import subprocess as sp
import yaml
import os
os.chdir(r'C:\Python\.idea\kp ')
p1=0
p2=0
p3=yaml.load(open('input.yaml'))['kz']
p4=yaml.load(open('input.yaml'))['kr']
cur1=abs(p3-p1)
cur2=abs(p4-p2)
i=0
while abs(cur1)>=0.0001 or abs(cur2)>=0.0001:
    sp.run(r'C:/Python/.idea/bat/iter.bat ',shell=True)
    i+=1
    p1=p3
    p3=float(yaml.load(open('input.yaml'))['kz'].split()[0])
    p2=p4
    p4=yaml.load(open('input.yaml'))['kr']
    cur1 = abs(p3 - p1)
    cur2 = abs(p4-p2)