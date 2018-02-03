#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""проеделяеем состав Tsostav  это элемент линейного пространства
доступно разбалвение и смешение в одном объеме
выдает все результаты в ядерной концентрации деленной на 10^24
плотности в граммах на см^3
"""

import numpy as np
import re

# имена нуклидов и их атомные массы
nucconc = {"VAC": 1,
           "*C*": 12,
           "*H*": 1.00782503207,
           "*O*": 15.99491461956,
           "AL": 26.981538627,
           "AG09": 107.905955556,
           "B-10": 10.012936992,
           "B-11": 11.009305406,
           "C": 12,
           "CR": 51.940507472,
           "D-SC": 2,
           "FE": 55.934937475,
           "FP33": 233,
           "FP35": 235,
           "FP39": 239,
           "GD55": 154.922622022,
           "GD56": 155.922122743,
           "GD57": 156.923960135,
           "H": 1.00782503207,
           "HE": 4.00260325415,
           "HF": 177.943698766,
           "I135": 134.910048121,
           "N": 14.00307400478,
           "NB": 92.906378058,
           "NI": 58.934346705,
           "O": 15.99491461956,
           "PU38": 238.049559894,
           "PU39": 239.052163381,
           "PU40": 240.053813545,
           "PU41": 241.056851456,
           "PU42": 242.058742611,
           "SCAT": 1,
           "XE35": 134.907227495,
           "SM49": 148.917184735,
           "TH32": 232.037156152,
           "U233": 233.039635207,
           "U235": 235.043929918,
           "U236": 236.045568006,
           "U238": 238.050788247,
           "ZR": 91.22,
           "TI": 47.88,
           "ER66": 166,
           "ER67": 167,
           "ER": 167.27,
           "CD": 112.41,
           "IN15": 114.82,
           "DY": 162.51,
           "MO": 95.95,
           "SI": 28.0855}

# список символьных имен нуклидов
izotlist = np.array(list(nucconc.keys()))
izotlist.sort()
# таблица соответсвия - символьное имя нуклида - его индекс
izot2index = {v:i for i, v in enumerate(izotlist)}
# список атомных масс нуклидов
n_Avagadr = 0.6022141793
nuclidmass = np.array([nucconc[nm] for nm in izotlist])/ n_Avagadr
nizot = len(izotlist)


class Tsostav(np.ndarray):
    """Состав материала - список имя нуклида - ядерная концентрация
>>> (U235*0.05 + U238 * 0.95 + O * 2).ro(10.5)
{'U235': 0.0011714482, 'U238': 0.022257512, 'O': 0.046857923}
    """

    def getRo(self):
        "получение плотности материала грамм на см^3"
        return np.dot(self, nuclidmass)

    def setRo(self, value):
        "установка плотности материала грамм на см^3"
        self *= (value / np.dot(self, nuclidmass))
        return self

    Ro = property(getRo, setRo, "плотность материала грамм на см^3")

    def todict(self):
        ind = self > 1e-12
        return {k:v for k, v in zip(izotlist[ind], self[ind])}

    def __repr__(self):
        return str(self.todict())

    def ro(self,v):
        c = self.copy()
        c.Ro = v
        return c



def Mix(substance, Ro=None, IsMass=False):
    """
    состав 
    >>> Mix({"U235":0.005,"O":12})
    >>> Mix("U235")
    >>> Mix("U235 0.005 O 12")
    Ro - установить заданную массовую плотность
    IsMass - приведены не ядерные концентрации а массы веществ
    """
    arr = np.zeros(nizot, dtype='f')
    if hasattr(substance, "items"):
        for k, v in substance.items():
            arr[izot2index[k]] = v
    else:
        if type(substance) is str:
            substance = substance.split()
        if len(substance) == 1:
            arr[izot2index[substance[0]]] = 1
        else:
            for k, v in zip(substance[0::2], substance[1::2]):
                arr[izot2index[k]] = float(v)
    if IsMass:
        arr/=nuclidmass
    v = arr.view(Tsostav)
    if not Ro is None:
        v.Ro = Ro
    return v


def SMix(name, Ro=None):
    """состав просто по имени ядерная концентация 1"""
    arr = np.zeros(nizot, dtype='f')
    arr[izot2index[name]] = 1
    v = arr.view(Tsostav)
    if not Ro is None:
        v.Ro = Ro
    return v


# определяем элементарные составы - и приводим при этом имена нуклидов к допустимым в питоне идентификаторам
for i in izotlist:
    name = re.sub(r"[\*\-]","_",i)
    globals()[name] = SMix(i)

def test_globals():
    assert(U238.todict()=={"U238":1})
    assert(_O_.todict()=={'*O*': 1})

def test_mix1():
    assert(Mix("U238").todict()=={"U238":1})

def test_mix2():
    assert(Mix("U238 2 O 5").todict()=={"U238":2,"O":5})

def test_mix_dict():
    assert(Mix({"U238":2,"O":5}).todict()=={"U238":2,"O":5})

def test_operations():
    assert((U238 * 2 + O * 5).todict()=={"U238":2,"O":5})

def test_Ro():
    fuel = (U235*0.05 + U238 * 0.95 + O * 2)
    fuel.Ro = 10.2
    assert(np.isclose(fuel.Ro,10.2))

def test_ro():
    fuel = (U235*0.05 + U238 * 0.95 + O * 2).ro(10.5)
    assert(np.isclose(fuel.Ro,10.5))

#Расчет твела с обогащением 14%
(TH32*0.86+U233*0.14+2*O).ro(10.1*((5.8**2-2.52**2)/5.8**2))
(AL*0.25+SI*0.75).ro(2.6)
(ZR*0.99+NB*0.01).ro(6.5*(((2.52**2-2.22**2)/5.8**2)))

#Расчет твела с обогащением 12%
(TH32*0.88+U233*0.12+2*O).ro(10.1*((5.8**2-2.52**2)/5.8**2))
(AL*0.25+SI*0.75).ro(2.6)
(ZR*0.99+NB*0.01).ro(6.5*(((2.52**2-2.22**2)/5.8**2)))

#Расчет пэлов
((B_10*0.198+B_11*0.802)*4+C).ro(2.5)
(CR*0.42+NI*0.56).ro(8)

#Расчет стержня АЗ
((B_10*0.1+B_11*0.9)*4+C).ro(2.5*(20/28)**2)
(NI*0.78+CR*0.2).ro(8.3*(((20+1)**2-20**2)/28**2))

#Оболочка твэлов
(ZR*0.99+NB*0.01).ro(6.5)


#Расчет воды
(2*H+O).ro(0.72)

#Расчет пустого канала
(2*N*0.75+2*O*0.25).ro(1.2)


#Расчет СВП с d=6.8
(2*GD55*0.148+2*GD57*0.157+GD56*2*0.695+O*3).ro(4)
(AL).ro(2.6)

#Расчет СВП с d=4.5
(2*GD55*0.148+2*GD57*0.157+GD56*2*0.695+O*3).ro(4)
(AL).ro(2.6*(3.5/4.5)**2)

#Стенка пустого АЗ
(ZR*0.975+NB*0.025).ro(6.5*((28)**2-23**2)/28**2)

(U235*0.044+U238*0.956+O*2).ro(9.8)
(B_10*0.25/100+B_11*1.25/100+AL*0.98+FE*0.5/100).ro(2.8558)

(U235*0.03+PU39*0.012+U238*0.958+O*2).ro(9.2)
