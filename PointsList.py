# -*- coding: utf-8 -*-
import numpy as np
from numpy import genfromtxt
from mean_shift_utils import  euclidean_dist
from mean_shift import MeanShift
import point_grouper as pg
import copy
def load_points1(filename):
    data = genfromtxt(filename, delimiter=',')
    return data

#传进来文件名，变成一个总的列表，然后返回一个pointslist对象
class PointsList():
    #不同的群组的个数
    groupnums=0
    filename=''
    datafirst=[]
    typelist=[]
    data={}
    def __init__(self,filename):
        self.filename=filename
        self.load_points_from_file(self.filename)
        self.transfertodata()
        #self.datafirst.sort()

        # print '过滤前'
        # print len(self.data)
        # print self.data
        # #self.filt()
        # print '过滤后'
        # #print len(self.data['LTE.734474.51'])
        # print self.data
        pass
    def load_points_from_file(self,filename):
        #将数据填入datafirst 第一列是字符，第二列，第三列是浮点数
        fileobj = open(filename, mode='rb')
        head = fileobj.readline().strip().decode('utf-8')
        nextline = fileobj.readline().strip().decode('utf-8')
        while len(nextline) > 0:
            tmplist=[]
            datalist = nextline.split(',')
            type = datalist[0]
            lon = float(datalist[2])/100000.0
            lat = float(datalist[3])/100000.0
            rsrp=float(datalist[4])
            if rsrp<-1000:
                nextline = fileobj.readline().strip().decode('utf-8')
                continue
            if type not in self.typelist:
                self.typelist.append(type)
            tmplist.append(type)
            tmplist.append(lon)
            tmplist.append(lat)
            tmplist.append(rsrp)
            self.datafirst.append(tmplist)
            nextline = fileobj.readline().strip().decode('utf-8')
        self.groupnums=len(self.typelist)
        fileobj.close()

    def transfertodata(self):
       for t in self.typelist:
           tmplist=[]
           for i in range(len(self.datafirst)):
                tmpll=[]
                if self.datafirst[i][0]==t:
                    tmpll.append(self.datafirst[i][1])
                    tmpll.append(self.datafirst[i][2])
                    tmpll.append(self.datafirst[i][3])
                    tmplist.append(tmpll)
           tmplist=np.array(tmplist)
           self.data[t]=tmplist
    def allpointsnum(self):
        return len(self.datafirst)
    #获取群组个数
    def getgroupnums(self):
        return self.groupnums
    def getallxarraylist(self):
        x=[]
        for i in range(self.allpointsnum()):
            x.append(self.datafirst[i][1])
        x=np.array(x)
        return x
    def getallyarraylist(self):
        x=[]
        for i in range(self.allpointsnum()):
            x.append(self.datafirst[i][2])
        x=np.array(x)
        return x
        pass
    def getxarraylistbytype(self,t):
        x=[]
        for i in range(len(self.data[t])):
            x.append(self.data[t][i][0])
        return x
    def getyarraylistbytype(self,t):
        x=[]
        for i in range(len(self.data[t])):
            x.append(self.data[t][i][1])
        return x
    def getcenterpoint_from_array(self,shift_points):

        points=shift_points.tolist()
        sumx=0.0
        sumy=0.0
        for point in points:
            sumx+=point[0]
            sumy+=point[1]
        x=sumx/len(points)
        y=sumy/len(points)
        return [x,y]
    def getunsameindex(self,lis):
        lis=lis.tolist()
        index=[]
        tmplist=[]
        dic={}
        for l in lis:
            if l not in tmplist:
                tmplist.append(l)
                dic[l]=1
            else:
                dic[l]+=1
        num=0
        for l in tmplist:
            if dic[l]>num:
                num=dic[l]
                p=l
        #找到了最大的num 以及下表p，遍历表lis，只要不是这个的，统统加入进去

        for i in range(len(lis)):
            if lis[i]!=p:
                index.append(i)

        return index

    def filt(self):
        #直接从data里面过滤去
        point_grouper = pg.PointGrouper()
        for t in self.typelist:
            group_assignments = point_grouper.group_points(self.data[t].tolist())

            tmplist=self.data[t].tolist()
            tmplist1=copy.deepcopy(tmplist)

            for i in self.getunsameindex(group_assignments):

                val=tmplist1[i]
                tmplist.remove(val)

            self.data[t]=np.array(tmplist)
    def getxnplis(self):
        tmplist=[]
        for i in range(len(self.datafirst)):
            tmpll=[]
            tmpll.append(self.datafirst[i][1])
            tmpll.append(self.datafirst[i][3])
            tmplist.append(tmpll)
        return np.array(tmplist)

    def getynplis(self):
        tmplist=[]
        for i in range(len(self.datafirst)):
            tmpll=[]
            tmpll.append(self.datafirst[i][2])
            tmpll.append(self.datafirst[i][3])
            tmplist.append(tmpll)
        return np.array(tmplist)
        pass
    def getxylist(self):
        tmplist=[]
        for i in range(len(self.datafirst)):
            tmpll=[]
            tmpll.append(self.datafirst[i][1])
            tmpll.append(self.datafirst[i][2])
            tmplist.append(tmpll)
        return np.array(tmplist)

    def getxyzlist(self):
        tmplist=[]
        for i in range(len(self.datafirst)):
            tmpll=[]
            tmpll.append(self.datafirst[i][1])
            tmpll.append(self.datafirst[i][2])
            tmpll.append(self.datafirst[i][3])
            tmplist.append(tmpll)
        return tmplist
        pass

if __name__=="__main__":
    pl=PointsList('LTE_CELL_GRID.csv')   #14 14
    print(pl.filename)
    pass