import matplotlib.pyplot as plt
import numpy as np
import math
from sympy import*
from scipy.special import*
import  yaml
import os
from scipy.interpolate import UnivariateSpline
os.chdir(r'C:\Python\.idea\kp')

#НАЧАЛЬНЫЕ ДАННЫЕ
delh1=1439800-1311100   # разность энальпий 1-го контура
Tin=294.7 #температура воды на входе в реактор
delT1=317-294.7 #разность температур  1ого контура
delT2=241.4-170 #разность температур  2ого контура
N=35*10**6
delh2=1044200-720650# разность энтальпий участок a-b
delh3=2939900-2802900 # разность энтальпий участок с-d
r=2.8029e+006-1.0442e+006 #теплота парообразования при температуре 241.4 С разность двух  энтальпий
Sk= 96.0 #размер чехла кассеты под ключ, мм
Sm= 2.0 #межкассетные промежутки, мм
Ntvs = 121
Ntvl=69 #число твеэлов
Nsvp1=9 #число свп d1=6.8 мм
Nsvp2=6 #число свп d2=4.5 мм
Npl=7 #количество пэлов
delcheh=0.7 #толщина  чехла твс
dcentr=8.6 #диаметр центральной трубки
d1=6.8 #диаметр свп 1ого типа
d2=4.5  #диаметр свп 2ого типа
dtvl=6.8   #диаметр твэла
deltvl=0.5  #толщина оболочки твэла
dpl=6.8 #диаметр пэл
ro=1/1.4126e-003    #плотность воды при средней температуре в 1ом контуре
Sv=689 #площадь вытеснителя
kG=0.93
Raz=1219/2000 #Raz=609.5 радиус АЗ
Haz=1300/1000  #Высота АЗ
infile=yaml.load(open('input.yaml'))
kr=infile['kr']  #коэффициент равномерности по радиусу 1.42
if kr!=1.42:
    kz=infile['kz'].split()  #коэффициент равномерности по высоте  1.36
else:
    kz = infile['kz']
kQ=0.98
s=9.6   #шаг решетки
shag=1.41 #x=s/dtvl
nu=1.2025e-007 #кинематическая вязкость при температуре 305,85 С и давлении 12,7
lamd=0.54244 #теплопроводность   при температуре 305,85 С и давлении 12,7
Cp=5744.9 #при температуре 305,85 С и давлении 12,7
lamdob=18 #теплопроводность оболочки твэла
dcomp=2.52 #эквивалентный диаметр компенсатора в мм
lambdt=35 #теплопроводность сердечника
Tkip=329.04 #температура кипения в первом контуре
davl1=12.7 #давление в первом контуре в МПа
#############################################################
file=open('datakp.yaml','w',encoding="utf-8")
form = format('%.3f')
kpd=0.272304597
file.write('kpd : '+ str(form%kpd)+'\n')
Q=35/kpd
print('тепловая мощность реактора Qр=',form%Q, 'МВт')
file.write('Qр : '+ str(form%Q)+'\n')
G1=Q*10**6/(delh1)
g1=G1*3.6
print('расход тн 1-го контура',form% g1, 'т/ч')
G2=Q*10**6/(delh2+r+delh3)
g2=G2*3.6
print('расход тн 2-го контура',form% g2, 'т/ч')
#Расчет эквивалентного диаметра
Dequl=(math.sqrt(2*math.sqrt(3)/math.pi*Ntvs)*(Sk+Sm))
print('эквивалентный диаметр',form% Dequl, 'мм')

#Расчет средней скорости движения воды
Stvs=math.sqrt(3)/2*(Sk-2*delcheh)**2
Stn=Stvs-math.pi*(Ntvl*dtvl**2/4+Nsvp1*d1**2/4+Nsvp2*d2**2/4)-Sv #площадь проходного сечения в мм^2
print('площадь проходного сечения в 1-ой твс', form% Stn, 'мм^2')
Wsr=kG*G1/(ro*Stn*Ntvs/10**6)
Gtn=ro*Wsr*Stn/10**6
print('средняя скорость теплоносителя',form % Wsr, 'м/с')
print('средний расход теплоносителя на охлаждение твэлов и СВП', form%Gtn, 'кг/с')
Heff=1.
#Расчет толщин отражателя
#x=pi*Haz/(2*Heff)
if kr==1.42:
    a=0.1 #коэффициенты a и b выбираются для метода дихотомии
    b=4.
    p=5 #просто число первоначальное
    while abs(p)>0.0001:
        x = 0.5 * (b + a)
        p = x / sin(x) - float(kz)
        if p<0:
            a=x
        else:
            b=x

    Heff=math.pi*Haz/(2*x)
    print('высота активной зоны с учетом отражателя', form % Heff,'м')
    file.write('Heff : '+str(form%(Heff-Haz))+'\n')
    ksi=2.405
    j1(ksi)
    j1(1.316)    #x=ksi*R/Reff
    a=0.1
    b=5.
    p=5
    while abs(p)>0.0001:
        x = 0.5 * (b + a)
        p = x /(2*j1(x)) - kr
        if p<0:
            a=x
        else:
            b=x
    Reff=ksi*Raz/x
    print('радиус активной зоны с учетом отражателя',form % Reff,'м')
    file.write('Reff : '+str(form%(Reff-Raz))+'\n')

#Расчет средних тепловых характеристик АЗ
Vaz=Haz*math.pi*Dequl**2/4/10**6 #объем АЗ в м^3
qv=Q/Vaz  #удельная энергонапряженность АЗ
Qtvs=kQ*Q/Ntvs #средняя тепловая можность ТВС
qlsr=Qtvs/(Ntvl*Haz) #средний линейный тепловой поток от твелов,Мвт/м
qsr=qlsr/(math.pi*dtvl/1000) #средняя плотнссть теплового потока на пов-ти твелов
if kr==1.42:
    qmax=qsr*kr*float(kz) #max плотнссть теплового потока на пов-ти твелов
print('удельная энергонапряженность АЗ', form % qv,'МВт/м^3')
file.write('qv : '+(str(form%qv))+'\n')
print('средняя тепловая мощность ТВС',form % Qtvs,'МВт')
qlsrviv=qlsr*10**6/10**2
print('средний линейный тепловой поток от твэлов', form % qlsrviv,'Вт/см')
print('средняя плотность теплового потока на пов-ти твэлов',form % qsr,'МВт/м^2')

#Расчет распределения температур
Wsrtvsm=Wsr*kr
deql=dtvl*(2*math.sqrt(3)/math.pi*(s/dtvl)**2-1)/1000 #Экваивалентный диаметр для треугольной решетки в м^2
a=lamd/(ro*Cp) #при температуре 305,85 С и давлении 12,7
Pr=nu/a
Re=Wsrtvsm*deql/nu
x=shag
Nu=(0.0165+0.02*(1-0.91/x**2)*x**0.15)*Re**0.8*Pr**0.4
alf=Nu/deql*lamd
print('Коэффициент теплоотдачи', '%1.2f' % alf,'Вт/(м^2*К)')

#График распределения плотности теплового потока на поверхности твэлов по высоте

if kr==1.42:
    def q(z,qmax,Heff):
        return qmax*cos(math.pi*z/Heff)/kr #для температур
    xlist=plt.mlab.frange(-Haz/2,Haz/2,Haz/10)
    ylist=[q(z,qmax,Heff) for z in xlist]
    spl=UnivariateSpline(xlist,ylist)
    plt.plot(np.linspace(xlist[0],xlist[len(xlist)-1],100),spl(np.linspace(xlist[0],xlist[len(xlist)-1],100)),'red')
    plt.ylabel(r'$q(z),$ ${}\frac {{МВт}}{{м^2}}$')
    plt.xlabel('$z,$ $м$')
    plt.title('Плотность теплового потока')
    plt.grid(True)

else:
    def q(kz,qsr,qkr):
        potok=[]
        for i in range(len(kz)):
            potok.append(qsr*float(kz[i])*kr/kr)
        return potok
    xlist=np.linspace(-Haz/2,Haz/2,10)
    ylist=q(kz,qsr,kr)
    spl=UnivariateSpline(xlist,ylist,s=0,k=2)
    plt.plot(np.linspace(xlist[0],xlist[len(xlist)-1],100),spl(np.linspace(xlist[0],xlist[len(xlist)-1],100)),'red')
    plt.ylabel(r'$q(z),$ ${}\frac {{МВт}}{{м^2}}$')
    plt.title('Плотность теплового потока')
    plt.xlabel('$z,$ $м$')
    plt.grid(True)


###################################кипение####################################
def kipenie(xlist,Tobolout,Tkip,davl1,Heff,alf):
    x=[]
    x2=0
    if kr==1.42:
        for i in range(len(xlist)):
            x.append(abs(Tobolout[i]-Tkip))
        for i in range(len(xlist)):
            if abs(Tobolout[i]-Tkip) == np.partition(x,0)[0] or abs(Tobolout[i]-Tkip) ==np.partition(x,1)[1]:
                x1=x2 #индекс массива в начале кипения
                x2=i  #индекс массива в конце кипения
        if Tobolout[len(xlist)-1]>Tkip:
            x2=len(xlist)-1
        alfkip=[]
        k=0
        for i in range(x1,x2+1):
            alfkip.append(4.32*(davl1**0.14+1.28*10**(-2)*davl1**2)*(q(xlist[i],qmax*10**6,Heff))**0.7)
        ll=[]
        for z, i in zip(xlist, range(len(xlist))):
            if i in range(x1,x2+1):
                 ll.append( Tkip + q(z, qmax * 10 ** 6, Heff) / (alfkip[k]))
                 k+=1
            else:
                ll.append( Tteplonos[i] + q(z, qmax * 10 ** 6, Heff) / (alf))
    else:
        x=[]
        for i in range(len(xlist)):
            x.append(abs(Tobolout[i] - Tkip))
        for i in range(len(xlist)):
            if abs(Tobolout[i] - Tkip) == np.partition(x, 0)[0] or abs(Tobolout[i] - Tkip) == np.partition(x, 1)[1]:
                x1 = x2  # индекс массива в начале кипения
                x2 = i  # индекс массива в конце кипения
        if Tobolout[len(xlist)-1]>Tkip:
            x2=len(xlist)-1

        alfkip = []
        k = 0
        for i in range(x1, x2 + 1):
            alfkip.append(4.32 * (davl1 ** 0.14 + 1.28 * 10 ** (-2) * davl1 ** 2) * (q(kz,qsr*10**6,kr)[i]) ** 0.7)
        ll = []
        for z, i in zip(xlist, range(len(xlist))):
            if i in range(x1, x2 + 1):
                ll.append(Tkip + q(kz,qsr*10**6,kr)[i] / (alfkip[k]))
                k += 1
            else:
                ll.append(Tteplonos[i] + q(kz,qsr*10**6,kr)[i] / (alf))
    return ll
##График распределения температуры теплоносителя по высоте
#в- центре
Per=Ntvl*math.pi*dtvl/1000

if kr==1.42:
    def Ttn(z, qmax, Heff, Haz):
        y = symbols('y')
        return integrate(qmax * cos(math.pi * y / Heff), (y, -Haz / 2, z))


    Tteplonos = [Tin + kG * Per / (Gtn * kQ*kr * Cp) * Ttn(z, qmax * 10 ** 6, Heff, Haz) for z in xlist]
    Tobolout = [Tteplonos[i] + q(z, qmax * 10 ** 6, Heff) / (alf) for z, i in zip(xlist, range(len(xlist)))]
    if max(Tobolout) > Tkip:
        Tobolout = kipenie(xlist, Tobolout, Tkip, davl1, Heff, alf)
    spl_Tobolout=UnivariateSpline(xlist,Tobolout,k=2)
    print('максимальная температура внешней оболчки твэла =',form%max(Tobolout),'C')
    Tobolin=[Tobolout[i]+q(z,kr*kz*qlsr*10**6,Heff)*ln(dtvl/(dtvl-2*deltvl))/(2*math.pi*lamdob) for z,i in zip(xlist,range(len(xlist)))]
    spl_Tobolin=UnivariateSpline(xlist,Tobolin)
    print('максимальная температура внутренней оболчки твэла =',form % max(Tobolin),'C' )
    Rts=dtvl/1000/((4*lambdt)*(1-(dcomp/(dtvl-2*deltvl))**2))*(1-(dcomp/(dtvl-2*deltvl))**2*(1-2*ln((dtvl-2*deltvl)/dcomp)))
    Tts=[Tobolin[i]+q(z,qmax*10**6,Heff)*Rts for z,i in zip(xlist,range(len(xlist)))] #температура топливного сердечника
    spl_Tts=UnivariateSpline(xlist,Tts)
    print('максимальная температура топливного сердечника =',form % max(Tts),'C' )
    spl_Tobolout.set_smoothing_factor(20)
    spl_Tobolin.set_smoothing_factor(20)
    spl_Tts.set_smoothing_factor(20)

    plt.plot(xlist,Tteplonos,'red')
    plt.ylabel('$T,$ $^oC$')
    plt.xlabel('$z,$ $м$')
    plt.plot([-0.65,0.65],[329.04,329.04],'--',)
    plt.plot(np.linspace(xlist[0],xlist[len(xlist)-1],100),spl_Tobolout(np.linspace(xlist[0],xlist[len(xlist)-1],100)),'blue')
    plt.plot(np.linspace(xlist[0],xlist[len(xlist)-1],100),spl_Tobolin(np.linspace(xlist[0],xlist[len(xlist)-1],100)),'green')
    plt.xlabel('$z,$ $м$')
    plt.plot(np.linspace(xlist[0],xlist[len(xlist)-1],100),spl_Tts(np.linspace(xlist[0],xlist[len(xlist)-1],100)),'orange')
    plt.grid(True)


    Tsvp=[Tobolin[i]+0.02*q(z,qmax*10**6,Heff)*Rts for z,i in zip(xlist,range(len(xlist)))] #температура сердечников остальных элементов
    file.write('средняя температура твэла(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tts)/len(Tts)+273)/1e3))+'"'+'\n')
    file.write('средняя температура оболочки твэла(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tobolin)/len(Tobolin)+273)/1e3))+'"'+'\n')
    file.write('средняя температура свп(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tsvp)/len(Tsvp)+273)/1e3))+'"'+'\n')
    file.write('средняя температура других материалов(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tteplonos)/len(Tteplonos)+273)/1e3))+'"'+'\n')

        #на переферии
    def q(z,qmax,Heff):
        return qmax/kr*cos(math.pi*z/Heff)

    def Ttn(z,qmax,Heff,Haz):
        y=symbols('y')
        return  integrate(qmax/kr*0.7*cos(math.pi*y/Heff),(y,-Haz/2,z))
    Tteplonos=[Tin+kG*Per/(Gtn*kQ*0.7*Cp)*Ttn(z,qmax*10**6,Heff,Haz) for z in xlist]
    Tobolout=[Tteplonos[i]+q(z,qmax*10**6,Heff)/(alf) for z,i in zip(xlist,range(len(xlist)))]
    if max(Tobolout)>Tkip:
        Tobolout=kipenie(xlist,Tobolout,Tkip,davl1,Heff,alf)
    print('максимальная температура внешней оболчки твэла(П) =',form%max(Tobolout),'C')
    Tobolin=[Tobolout[i]+q(z,qmax*10**6,Heff)*deltvl/1000/lamdob for z,i in zip(xlist,range(len(xlist)))]
    print('максимальная температура внутренней оболчки твэла(П) =',form % max(Tobolin),'C' )
    Rts=dtvl/1000/((4*lambdt)*(1-(dcomp/(dtvl-2*deltvl))**2))*(1-(dcomp/(dtvl-2*deltvl))**2*(1-2*ln((dtvl-2*deltvl)/dcomp)))
    Tts=[Tobolin[i]+q(z,qmax*10**6,Heff)*Rts for z,i in zip(xlist,range(len(xlist)))] #температура топливного сердечника
    print('максимальная температура топливного сердечника(П) =',form % max(Tts),'C' )

    Tsvp=[Tobolin[i]+0.02*q(z,qmax*10**6,Heff)*Rts for z,i in zip(xlist,range(len(xlist)))] #температура сердечников остальных элементов
    file.write('средняя температура твэла(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tts)/len(Tts)+273)/1e3))+'"'+'\n')
    file.write('средняя температура оболочки твэла(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tobolin)/len(Tobolin)+273)/1e3))+'"'+'\n')
    file.write('средняя температура свп(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tsvp)/len(Tsvp)+273)/1e3))+'"'+'\n')
    file.write('средняя температура других материалов(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tteplonos)/len(Tteplonos)+273)/1e3))+'"'+'\n')
    
else:
    def Ttn(kz,qsr,kr):
        xlist=np.linspace(-Haz/2,Haz/2,10)
        integr=[0]
        for i in range(1,len(kz)):
            integr.append(integr[i-1]+(float(kz[i-1])+float(kz[i]))/2*(xlist[i]-xlist[i-1])*qsr*kr)
        return integr

    Tteplonos = [Tin + kG*Per/(Gtn*kQ*kr*Cp)*Ttn(kz,qsr*10**6,kr)[z] for z in range(len(xlist))]
    spl_teplonos=UnivariateSpline(xlist,Tteplonos,s=0,k=2)
    Tobolout = [Tteplonos[i] + q(kz,qsr*10**6,kr)[i] / (alf ) for  i in (range(len(xlist)))]
    # if max(Tobolout)>Tkip:
    #      Tobolout=kipenie(xlist,Tobolout,Tkip,davl1,Heff,alf)
    spl_Tobolout = UnivariateSpline(xlist, Tobolout,k=2)
    print('максимальная температура внешней оболчки твэла =', form % max(Tobolout), 'C')
    Tobolin = [Tobolout[i] + q(kz,qsr*10**6,kr)[i] * deltvl / 1000 / (lamdob ) for i in (range(len(xlist)))]
    spl_Tobolin = UnivariateSpline(xlist, Tobolin,s=0,k=2)
    print('максимальная температура внутренней оболчки твэла =', form % max(Tobolin), 'C')
    Rts = dtvl/1000/((4*lambdt)*(1-(dcomp/(dtvl-2*deltvl))**2))*(1-(dcomp/(dtvl-2*deltvl))**2*(1-2*ln((dtvl-2*deltvl)/dcomp)))
    Tts = [Tobolin[i] + q(kz,qsr*10**6,kr)[i]*Rts for i in (range(len(xlist)))]  # температура топливного сердечника
    spl_Tts = UnivariateSpline(xlist, Tts,s=0,k=2)
    print('максимальная температура топливного сердечника =', form % max(Tts), 'C')
    spl_Tobolout.set_smoothing_factor(30)
    spl_Tobolin.set_smoothing_factor(20)
    spl_Tts.set_smoothing_factor(20)
    plt.plot(np.linspace(-Haz/2,Haz/2,100),spl_teplonos(np.linspace(-Haz/2,Haz/2,100)),'red')
    plt.ylabel('$T,$ $^oC$')
    plt.xlabel('$z,$ $м$')
    plt.plot([-0.65,0.65],[329.04,329.04],'--',)
    plt.plot(np.linspace(-Haz/2,Haz/2,100),spl_Tobolout(np.linspace(-Haz/2,Haz/2,100)),'blue')
    plt.plot(np.linspace(-Haz/2,Haz/2,100),spl_Tobolin(np.linspace(-Haz/2,Haz/2,100)),'green')
    plt.plot(np.linspace(-Haz/2,Haz/2,100),spl_Tts(np.linspace(-Haz/2,Haz/2,100)),'orange')
    plt.grid(True)

    Tsvp=[Tobolin[i] + 0.02*q(kz,qsr*10**6,kr)[i]*Rts for i in (range(len(xlist)))] #температура сердечников остальных элементов
    file.write('средняя температура твэла(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tts)/len(Tts)+273)/1e3))+'"'+'\n')
    file.write('средняя температура оболочки твэла(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tobolin)/len(Tobolin)+273)/1e3))+'"'+'\n')
    file.write('средняя температура свп(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tsvp)/len(Tsvp)+273)/1e3))+'"'+'\n')
    file.write('средняя температура других материалов(Ц) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tteplonos)/len(Tteplonos)+273)/1e3))+'"'+'\n')
    
    
        #на переферии
    def q(kz,qsr,kr):
        potok=[]
        for i in range(len(kz)):
            potok.append(qsr*float(kz[i])*kr)
        return potok

    def Ttn(kz,qsr):
        xlist=np.linspace(-Haz/2,Haz/2,10)
        integr=[0]
        for i in range(1,len(kz)):
            integr.append(integr[i-1]+(float(kz[i-1])+float(kz[i]))/2*(xlist[i]-xlist[i-1])*qsr*kr)
        return integr

    Tteplonos=[Tin+kG*Per/(Gtn*kQ*kr*Cp)*Ttn(kz,qsr*10**6)[i] for i in range(len(xlist))]
    Tobolout=[Tteplonos[i]+q(kz,qsr*10**6,kr)[i]/(alf) for i in (range(len(xlist)))]
    if max(Tobolout)>Tkip:
        Tobolout=kipenie(xlist,Tobolout,Tkip,davl1,Heff,alf)
    print('максимальная температура внешней оболчки твэла(П) =',form%max(Tobolout),'C')
    Tobolin=[Tobolout[i]+q(kz,qsr*10**6,kr)[i]*deltvl/1000/lamdob for i in (range(len(xlist)))]
    print('максимальная температура внутренней оболчки твэла(П) =',form % max(Tobolin),'C' )
    Rts=dtvl/1000/((4*lambdt)*(1-(dcomp/(dtvl-2*deltvl))**2))*(1-(dcomp/(dtvl-2*deltvl))**2*(1-2*ln((dtvl-2*deltvl)/dcomp)))
    Tts=[Tobolin[i]+q(kz,qsr*10**6,kr)[i]*Rts for i in (range(len(xlist)))] #температура топливного сердечника
    print('максимальная температура топливного сердечника(П) =',form % max(Tts),'C' )

    Tsvp=[Tobolin[i]+0.02*q(kz,qsr*10**6,kr)[i]*Rts for i in (range(len(xlist)))] #температура сердечников остальных элементов
    file.write('средняя температура твэла(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tts)/len(Tts)+273)/1e3))+'"'+'\n')
    file.write('средняя температура оболочки твэла(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tobolin)/len(Tobolin)+273)/1e3))+'"'+'\n')
    file.write('средняя температура свп(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tsvp)/len(Tsvp)+273)/1e3))+'"'+'\n')
    file.write('средняя температура других материалов(П) : '+'"'+str('{:0=0.3f}e+3'.format(float(sum(Tteplonos)/len(Tteplonos)+273)/1e3))+'"'+'\n')

#
# matr=[]
# for i in range(len(xlist)):
#     matr.append(q(xlist[i],qmax*10**6,Heff))
# enthalpy=[]
# teta=[]
# for i in range(len(matr)):
#    # teta.append(matr[i]*(-1/alfkip[i]+1/alf))
#     enthalpy.append(Tteplonos[i]*Cp)
#
# Tteplonos=[kG*Per/(Gtn*kQ*kr)*Ttn(z,qmax*10**6,Heff,Haz) for z in xlist]
################################################################################
#Расчет гидравлических потерь
dzeSOPR=(1.10+0.18*(shag-1))*(1.82*math.log(Re/kr,10)-1.64)**(-2)
dzeIN=6
dzeOUT=4
dzeNR=2
dzeVR=3
dzedr=6*(Sv/Stn)**2
dzeDR=dzedr*5
print('коэффициент сопротивления трения=',form% dzeSOPR)
print('коэффициент сопротивления входных участков сборки=',dzeIN)
print('коэффициент сопротивления выходных участков сборки=',dzeOUT)
print('коэффициент сопротивления нижней опорной решетки  стержней=',dzeNR)
print('коэффициент сопротивления верхней опорной решетки  стержне=',dzeVR)
print('коэффициент сопротивления дистанционирующих решеток x5=',form % dzeDR )

delPtr=dzeSOPR*Haz/deql*ro*Wsr**2/2
delPm=(dzeIN+dzeDR+dzeOUT+dzeVR+dzeNR)*ro*Wsr**2/2

roN=1/1.3633e-003
roK=1/1.4704e-003
delPusk=(ro*Wsr)**2*(1/roK -1/roN)

ro1=1/1.3859e-003 #при температуре 294+(-294+(294+(317-294)/2))/2=299,75
ro2=1/1.4389e-003 #при температуре 311.25
delPniv=(ro1-ro2)*9.8*Haz
delP=delPtr+delPm+delPusk+delPniv
now=delP/1000
print('потеря давления на трение',form % now, 'KПа')
print('потеря давления на местные сопротивления',form %delPm, 'KПа')
print('потеря давления на ускорение',form %delPusk, 'KПа')
print('потеря давления на нивелирный напор',form %delPniv, 'KПа')
N1=delP*Wsr*G1*kG/(ro*0.55)
now=N1/10**6
print('потеря мощности на все виды споротивления', form % now,'МВт')
now=N1/N*100
print('доля потерянной мощности к электрической',form % now, '%')
kpdnet=(N-N1)/(Q*10**6)
now=kpdnet*100
#print('кпд нетто',form % now,'%')
################################################################################
##Проверка TQ
#print('#########################################################')
#q1=delh1*G1/10**6
#print('мощность, требуемая на  нагрев 1ого контура',form %q1,'МВт' )
#qek=G2*delh2/10**6
#print('мощность экономайзера',form %qek,'МВт' )
#qisp=G2*r/10**6
#print('мощность испарителя',form %qisp ,'МВт')
#qnagr=G2*delh3/10**6
#print('мощность пароперегревателя',form %qnagr,'МВт' )
#Tmax=294.1-170
#Tmin=317-295
#Tnap=(Tmax-Tmin)/ln(Tmax/Tmin)
#print('Температурный напор', form % Tnap)
##Построение T-Q диаграммы
#T=[]
#T.append(170)
#i=0
#while T[i]!=317:
#    i += 1
#    T.append(T[i-1]+1)
#ax=plt.gca()
#ax.set_xlim(0,180)
#ay=plt.gca()
#ay.set_ylim(160,330)
#plt.plot([0,Q],[294,317],'red',label = '$1^й$ $контур$')
#plt.plot([0,G2/10**6*delh2],[170,241.1],'blue',label = '$2^й$ $контур$')
#plt.legend(loc='upper right')
#plt.plot([G2/10**6*delh2,G2/10**6*(delh2+r)],[241.1]*2,'blue')
#plt.plot([G2/10**6*(delh2+r),G2/10**6*(delh2+r+delh3)],[241.1,285],'blue')
#plt.plot([G2/10**6*delh2,G2/10**6*delh2],[0,241.1],'-.',color='dodgerblue')
#plt.plot([G2/10**6*(delh2+r),G2/10**6*(delh2+r)],[0,241.1],'-.',color='dodgerblue')
#plt.plot([G2/10**6*(delh2+r+delh3),G2/10**6*(delh2+r+delh3)],[0,285],'-.',color='dodgerblue')
#plt.text(8,186,'Qэк')
#plt.text(65,186,'Qисп')
#plt.text(121,186,'<---')
#plt.text(132,186,'Qпп')
#plt.grid(True)
#plt.xlabel(r'$Q$, $МВт$')
#plt.ylabel('$T$, $^0C$')
#plt.title('$T-Q,$ $диаграмма$')
#plt.show()
#
#
#print('####################################################################')
#rtabl=5.8/2
#robol=6.8/2
#rH2O=(math.sqrt(1/math.pi*math.sqrt(3)/2))*Sk/100
file.close()