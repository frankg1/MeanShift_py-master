# -*- coding: utf-8 -*-
from PointsList import PointsList
from sklearn import preprocessing
import  numpy as np
from mean_shift_utils import get_centerpoint
from writetoshp import createshp
import pandas as pd
import os
from log import Log
import time
workspace=os.path.abspath('.')
class Vector():
    pl=None
    log=Log("ts")
    def __init__(self):
        self.pl=PointsList("Cell_grid1.csv")

        pass
    def getxz(self,lis):
        #从三元数组中得到二元数组  np.array
        tmplist=[]
        for i in range(len(lis)):
            tmpll=[]
            tmpll.append(lis[i][0])
            tmpll.append(lis[i][2])
            tmplist.append(tmpll)
        return np.array(tmplist)
    def getyz(self,lis):
        #从三元数组中得到二元数组  np.array
        tmplist=[]
        for i in range(len(lis)):
            tmpll=[]
            tmpll.append(lis[i][1])
            tmpll.append(lis[i][2])
            tmplist.append(tmpll)
        return np.array(tmplist)

    def getxy(self,lis):
        #从三元数组中得到二元数组  np.array
        tmplist=[]
        for i in range(len(lis)):
            tmpll=[]
            tmpll.append(lis[i][0])
            tmpll.append(lis[i][1])
            tmplist.append(tmpll)
        return tmplist
        pass
    def run(self):
        result=[]
        for t in self.pl.typelist:
            try:
                tmp=[]
                xyz=self.pl.data[t]    #[[x,y,z]......[]]
                if len(xyz)<20:
                    continue
                xz=self.getxz(xyz)
                yz=self.getyz(xyz)
                #归1化
                X_scaled = preprocessing.scale(xz)
                Y_scaled = preprocessing.scale(yz)

                X_scaled=X_scaled.tolist()
                dx=[]
                dy=[]
                for i in range(len(X_scaled)):
                    dx.append(X_scaled[i][0])
                    dy.append(X_scaled[i][1])
                dx=np.array(dx)
                dy=np.array(dy)
                f1=np.polyfit(dx, dy, 1)

                Y_scaled=Y_scaled.tolist()
                dx=[]
                dy=[]
                for i in range(len(Y_scaled)):
                    dx.append(Y_scaled[i][0])
                    dy.append(Y_scaled[i][1])
                dx=np.array(dx)
                dy=np.array(dy)
                f2=np.polyfit(dx, dy, 1)

                xy=self.getxy(xyz)
                c=get_centerpoint(xy)
                c1=[c[0]+f1[0],c[1]+f2[0]]

                tmp.append(t)
                tmp.append(c[0])
                tmp.append(c[1])
                tmp.append(c1[0])
                tmp.append(c1[1])
                result.append(tmp)
                #createshp(xyz,c,c1,t)

            except Exception as e:
                self.log.error(e)
                continue
        dframe = pd.DataFrame(result)
        dframe.to_csv(workspace+"\\t1.csv", mode='a', index=True, header=False, encoding='utf-8', columns=None)

if __name__=='__main__':
    a=time.time()
    v=Vector()
    b=time.time()
    v.run()
    c=time.time()

    print(b-a)
    print(c-b)
    # dframe = pd.DataFrame([[1,2,3],[2,3,4]])
    # dframe.to_csv(workspace+"\\test.csv", mode='a', index=True, header=False, encoding='utf-8',
    #                                           columns=None)
    pass