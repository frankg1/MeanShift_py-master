# -*- coding: utf-8 -*-
from PointsList import PointsList
from sklearn import preprocessing
import  numpy as np
from mean_shift_utils import get_centerpoint
from writetoshp import createshp



def listprocess(lis):
    lis.sort()
    min=lis[0]
    for i in range(len(lis)):
        lis[i]=(lis[i]-min)*100.0
    return lis

if __name__=="__main__":
    pl=PointsList('cellgrid.csv')

    #对两边分别做拟合

    #作两边分别做归0化
    xl=pl.getxnplis()
    X_scaled = preprocessing.scale(xl)

    yl=pl.getynplis()
    Y_scaled = preprocessing.scale(yl)

    print(X_scaled)
    print("------------------------------")
    print(Y_scaled)


    print(X_scaled.mean(axis=0))
    print(X_scaled.std(axis=0))

    print(Y_scaled.mean(axis=0))
    print(Y_scaled.std(axis=0))

    X_scaled=X_scaled.tolist()
    dx=[]
    dy=[]
    for i in range(len(X_scaled)):
        dx.append(X_scaled[i][0])
        dy.append(X_scaled[i][1])
    dx=np.array(dx)
    dy=np.array(dy)
    f1=np.polyfit(dx, dy, 1)
    p = np.poly1d(f1)
    print(f1)
    print(p)

    Y_scaled=Y_scaled.tolist()
    dx=[]
    dy=[]
    for i in range(len(Y_scaled)):
        dx.append(Y_scaled[i][0])
        dy.append(Y_scaled[i][1])
    dx=np.array(dx)
    dy=np.array(dy)
    f2=np.polyfit(dx, dy, 1)
    p = np.poly1d(2)
    print(f2)
    print(p)
    a=[(0,0),(0.08869,-0.2142)]  #向量已经得出来了

    #得出中心点

    #返回两个数组   [[].......[]]     [[],[].......[]]
    xy=pl.getxylist()
    c=get_centerpoint(xy)
    print(c)
    c1=[c[0]+f1[0],c[1]+f2[0]]
    print(c1)

    X=pl.getxyzlist()
    createshp(X,c,c1)


