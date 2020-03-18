# -*- coding: utf-8 -*-
import mean_shift as ms
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
from mean_shift_utils import getcrosspoint
from mean_shift_utils import get_centerpoint
from getangle import calc_angle
from PointsList import PointsList
from itertools import combinations
from haversine import haversine
from log import Log


class MeanShiftTest():
    pointslist=None
    #返回的结果集合 就是密度中心
    resultSet={}
    groupnums=0
    mean_shifter=None
    fdic={}
    pdic={}
    yvalsdic={}
    crosspoints=[]
    weightpoint=[]
    amuzith={}
    distances=[]
    res=[]
    log=Log('meanshift')
    def __init__(self,filename):
        self.pointslist=PointsList(filename)
        self.groupnums=self.pointslist.getgroupnums()
        self.mean_shifter= ms.MeanShift()
        #self.mean_shifter= ms.MeanShift('multivariate_gaussian')
    #运行漂移函数 结果集合得到结果
    def runmeanshift(self,kernel_bandwidth=0.003):
        for t in self.pointslist.typelist:
            tmplist=self.mean_shifter.cluster_cell(self.pointslist.data[t], kernel_bandwidth)
            self.res=self.mean_shifter.cluster(self.pointslist.data[t], kernel_bandwidth)
            #tmplist=self.mean_shifter.cluster_cell(self.pointslist.data[t], [3,3])
            self.resultSet[t]=tmplist
    #运行拟合函数
    def polyfitfunction(self):
        for t in self.pointslist.typelist:
            d=self.pointslist.data[t]  #得到的是numpy的数组
            d=d.tolist()
            dx=[]
            dy=[]
            for i in range(len(d)):
                dx.append(d[i][0])
                dy.append(d[i][1])
            dx=np.array(dx)
            dy=np.array(dy)
            f=np.polyfit(dx, dy, 1)
            self.fdic[t]=f
            p = np.poly1d(f)
            self.pdic[t]=p
            xlnp=self.pointslist.getallxarraylist()
            yvals = p(xlnp)
            self.yvalsdic[t]=yvals

    #求出了这一堆交点
    def crosspointfunction(self):   #排列组合，使用组合数
        numlist=range(self.pointslist.groupnums)
        orderlist=combinations(numlist,2)   #两两组合
        orderlist=list(orderlist)
        for l in orderlist:
            self.crosspoints.append(getcrosspoint(self.fdic[self.pointslist.typelist[l[0]]],self.fdic[self.pointslist.typelist[l[1]]]))

    #求出来交点的重心点
    def weightpointfunction(self):
        self.weightpoint=get_centerpoint(self.crosspoints)

    #求出来方位角
    def anglefunction(self):
        for t in self.pointslist.typelist:
            self.amuzith[t]=calc_angle([self.weightpoint,self.resultSet[t]])
    def getdistance(self):
        #如何计算，重心点和每一个点里面的
        for i in range(self.pointslist.allpointsnum()):
            #print self.weightpoint
            #print self.pointslist.datafirst[i]
            tmp=haversine(self.weightpoint[0],self.weightpoint[1],108.379097,22.825278)
            self.distances.append(tmp)
        pass
    def getdistance2(self):
        for i in range(self.pointslist.allpointsnum()):
            #print self.weightpoint
            #print self.pointslist.datafirst[i]
            tmp=haversine(self.crosspoints[0][0],self.crosspoints[0][1],108.350903,22.815278)
            self.distances.append(tmp)
        pass
    def draw2(self):
        #先画原来的点
        x=self.pointslist.getallxarraylist()
        y=self.pointslist.getallyarraylist()
        plot1 = plt.plot(x, y, 's',label='original poinits')
        plot2 = plt.plot(self.crosspoints[0][0],self.crosspoints[0][1], 's',label='交点')
        for t in self.pointslist.typelist:
            plot3 = plt.plot(x,self.yvalsdic[t],'r',color='black',label=t)

        plt.show()
        pass
    def draw(self):
        x=self.pointslist.getallxarraylist()
        y=self.pointslist.getallyarraylist()
        i=0
        colorlist=['red','blue','black']
        ci=0
        for t in self.pointslist.typelist:
            plot1 = plt.plot(self.pointslist.getxarraylistbytype(t), self.pointslist.getyarraylistbytype(t), 's',color=colorlist[ci],label=t)
            plot2 = plt.plot(self.crosspoints[i][0],self.crosspoints[i][1], 's',color='yellow',label='crosspoint')
            plot3 = plt.plot(x,self.yvalsdic[t],'r',color=colorlist[ci],label=t)
            ci=(ci+1)%3
            i+=1
        plot4 = plt.plot(self.weightpoint[0],self.weightpoint[1], 's',label='weightpoint')


        x_major_locator=MultipleLocator(1)
        #把x轴的刻度间隔设置为1，并存在变量里
        y_major_locator=MultipleLocator(1)
        #把y轴的刻度间隔设置为10，并存在变量里
        ax=plt.gca()
        #ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        #把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)
        #把y轴的主刻度设置为10的倍数
        plt.xlim(100,150)
        #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
        plt.ylim(20,30)
        #把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白

        plt.legend(loc=4)
        plt.title('algorithm')
        plt.show()

    def draw1(self):
        #先画原来的点
        x=self.pointslist.getallxarraylist()
        #x.sort()
        #print ('sort x  ',x)
        y=self.pointslist.getallyarraylist()
        i=0
        colorlist=['red','blue','black']
        ci=0
        xx=[]
        yy=[]


        for i in range(len(self.res.shifted_points)):
            xx.append(self.res.shifted_points[i][0])
            yy.append(self.res.shifted_points[i][1])

        for t in self.pointslist.typelist:
            #print (self.pointslist.getxarraylistbytype(t),self.pointslist.getyarraylistbytype(t))
            plot1 = plt.plot(self.pointslist.getxarraylistbytype(t), self.pointslist.getyarraylistbytype(t), 's',color=colorlist[ci],label=t)
            #print 'resultset'
            #print self.resultSet[t]
            plot1 = plt.plot(self.resultSet[t][0], self.resultSet[t][1], 's',color=colorlist[ci+1],label='density center')
            #print ('this set:',self.resultSet[t][1], self.resultSet[t][1] )
            #plot1=plt.plot(xx,yy, 's',color=colorlist[ci+2],label='miduzhongxins')
            #plot2 = plt.plot(self.crosspoints[i][0],self.crosspoints[i][1], 's',color='yellow',label='crosspoint')
            plot3 = plt.plot(x,self.yvalsdic[t],'r',color=colorlist[ci],label=t)
            #x.sort()
            #print x
            #print 'xxx'
            ci=(ci+1)%3
            i+=1
        #plot4 = plt.plot(self.weightpoint[0],self.weightpoint[1], 's',label='weightpoint')
        x_major_locator=MultipleLocator(1)
        #把x轴的刻度间隔设置为1，并存在变量里
        y_major_locator=MultipleLocator(1)
        #把y轴的刻度间隔设置为10，并存在变量里
        ax=plt.gca()
        #ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        #把x轴的主刻度设置为1的倍数
        ax.yaxis.set_major_locator(y_major_locator)
        #把y轴的主刻度设置为10的倍数
        plt.xlim(100,150)
        #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
        plt.ylim(20,30)
        #把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白




        plt.legend(loc=4)
        plt.title('algorithm')
        plt.show()
        pass

    def logtofile(self):
        #self.log.debug("各个类别的Points")
        #for t in self.pointslist.typelist:
         #   self.log.debug(self.pointslist.data[t])
        self.log.debug("各个类别的密度中心")
        self.log.debug(self.resultSet)
        self.log.debug("拟合结果，线性函数")
        self.log.debug(self.pdic)
        self.log.debug("直线的交点(s)")
        self.log.debug(self.crosspoints)
        self.log.debug("交点的重心点")
        self.log.debug(self.weightpoint)
        self.log.debug("各自的方位角")
        self.log.debug(self.amuzith)
        self.log.debug('各自的距离')
        self.log.debug(self.distances)
        self.log.close()
    def info(self):
        #print "各个类别的Points"
        #for t in self.pointslist.typelist:
         #   print self.pointslist.data[t]
        print"各个类别的密度中心"
        print self.resultSet
        print "拟合结果，线性函数"
        print self.pdic
        print "直线的交点(s)"
        print self.crosspoints
        print "交点的重心点"
        print self.weightpoint
        print "各自的方位角"
        print self.amuzith
        print '各自的距离'
        print self.distances
    def run(self,bandwitdth):
        self.runmeanshift(bandwitdth)
        self.polyfitfunction()
        self.crosspointfunction()
        self.weightpointfunction()
        self.anglefunction()
        self.getdistance()
        self.info()
        self.logtofile()
        self.draw()
    def run1(self,bandwitdth):
        self.runmeanshift(bandwitdth)
        self.polyfitfunction()
        #self.crosspointfunction()
        #self.weightpointfunction()
        #self.anglefunction()
        #self.getdistance()
        self.info()
        self.logtofile()
        self.draw1()
    def run2(self,bandwitdth):
        self.runmeanshift(bandwitdth)
        self.polyfitfunction()
        self.crosspointfunction()
        #self.weightpointfunction()
        #self.anglefunction()
        self.getdistance2()
        self.info()
        self.logtofile()
        self.draw2()