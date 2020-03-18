# -*- coding: utf-8 -*-
import mean_shift as ms
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
from mean_shift_utils import getcrosspoint
from mean_shift_utils import get_centerpoint
from getangle import calc_angle
from PointsList import PointsList
from MeanShiftTest import MeanShiftTest
from log import Log
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#直接读取scv文件中的点集合，返回np.ndarray 数组直接用 [[],[],[]....[]]
def load_points(filename):
    data = genfromtxt(filename, delimiter=',')
    return data

def run():
    reference_points = load_points("data2.csv")
    mean_shifter = ms.MeanShift()
    #将参数传进去，得到返回结果  参数：点集合X  邻居阈值bandwidth
    mean_shift_result = mean_shifter.cluster(reference_points, kernel_bandwidth=3)
    print "Original Point     Shifted Point  Cluster ID"
    print "============================================"
    x1=[]
    y1=[]
    x2=[]
    y2=[]
    set0x=[]
    set0y=[]
    set1x=[]
    set1y=[]
    set2x=[]
    set2y=[]
    for i in range(len(mean_shift_result.shifted_points)):
        original_point = mean_shift_result.original_points[i]
        converged_point = mean_shift_result.shifted_points[i]
        cluster_assignment = mean_shift_result.cluster_ids[i]
        print "%i,(%5.6f,%5.6f)  ->  (%5.6f,%5.6f)  cluster %i" % (i,original_point[0], original_point[1], converged_point[0], converged_point[1], cluster_assignment)
        x1.append(original_point[0])
        y1.append(original_point[1])
        x2.append(converged_point[0])
        y2.append(converged_point[1])
        if cluster_assignment==0:
            set0x.append(original_point[0])
            set0y.append(original_point[1])
        if cluster_assignment==1:
            set1x.append(original_point[0])
            set1y.append(original_point[1])
        if cluster_assignment==2:
            set2x.append(original_point[0])
            set2y.append(original_point[1])



    plot1 = plt.plot(x1, y1, 's',label='original poinits')
    plot2 = plt.plot(x2, y2, 's',label='new points')
    #plot3 = plt.plot(x1np,yvals0,'r',color='black',label='0')
    #plot3 = plt.plot(x1np,yvals1,'r',color='gray',label='1')
    #plot3 = plt.plot(x1np,yvals2,'r',color='blue',label='2')
    #plot4=plt.plot([rtcp[0]],[rtcp[1]],'s',color='red',label='3')

    plt.legend(loc=4) #指定legend的位置右下角
    plt.title('algorithm')

    #plt.xlim(-30,20 )
    #plt.ylim(-10,20)
    plt.show()

def load_points1(filename):
    data = genfromtxt(filename, delimiter=',')
    print data
    rt_data1=[]
    rt_data2=[]
    rt_data3=[]
    #每一行数据
    for d in data:
        tmp=[]
        #根据小区标识，来区分组别
        print d[2]
        if abs(d[2]) < 1.0e-9 :
            #加上第一列，  #加上第二列
            tmp.append(d[0])
            tmp.append(d[1])
            rt_data1.append(tmp)
        elif abs(d[2]-1) < 1.0e-9 :
            #加上第一列，  #加上第二列
            tmp.append(d[0])
            tmp.append(d[1])
            rt_data2.append(tmp)
        elif abs(d[2]-2) < 1.0e-9 :
            #加上第一列，  #加上第二列
            tmp.append(d[0])
            tmp.append(d[1])
            rt_data3.append(tmp)
        else:
            pass
        pass
    rt_data1=np.array(rt_data1)
    rt_data2=np.array(rt_data2)
    rt_data3=np.array(rt_data3)
    return rt_data1,rt_data2,rt_data3
    pass
def run1():
    #函数返回两个集合，
    reference_points1,reference_points2,reference_points3 = load_points1("data3.csv")
    print reference_points1,reference_points2,reference_points3
    #print "ref : "+str(len(reference_points))
    #print 'ref: '
    #print len(reference_points)
    #生成对象
    mean_shifter = ms.MeanShift()
    #将参数传进去，得到返回结果  参数：点集合X  邻居阈值bandwidth
    result1 = mean_shifter.cluster_cell(reference_points1, kernel_bandwidth=3)
    result2 = mean_shifter.cluster_cell(reference_points2, kernel_bandwidth=3)
    result3 = mean_shifter.cluster_cell(reference_points3, kernel_bandwidth=3)
    #返回结果是，原始点集合，转换之后的点集合，最后的集群序号
    print "Original Point     Shifted Point  Cluster ID"
    print "============================================"
    #将三个群的点分别转换成列表表示
    orig_points1=reference_points1.tolist()
    orig_points2=reference_points2.tolist()
    orig_points3=reference_points3.tolist()
    x=[]
    y=[]

    set0x=[]
    set1x=[]
    set2x=[]
    set0y=[]
    set1y=[]
    set2y=[]
    for point in orig_points1:
        x.append(point[0])
        y.append(point[1])
        set0x.append(point[0])
        set0y.append(point[1])
    for point in orig_points2:
        x.append(point[0])
        y.append(point[1])
        set1x.append(point[0])
        set1y.append(point[1])
    for point in orig_points3:
        x.append(point[0])
        y.append(point[1])
        set2x.append(point[0])
        set2y.append(point[1])
    #开始拟合
    #开始拟合
    s0x = np.array(set0x)
    s0y = np.array(set0y)
    s1x = np.array(set1x)
    s1y = np.array(set1y)
    s2x = np.array(set2x)
    s2y = np.array(set2y)

    #用1次多项式拟合  这是 k b
    f0 = np.polyfit(s0x, s0y, 1)
    f1 = np.polyfit(s1x, s1y, 1)
    f2 = np.polyfit(s2x, s2y, 1)
    print f2

    #这是多项式
    p0 = np.poly1d(f0)
    print('p0 is :\n',p0)
    p1 = np.poly1d(f1)
    print('p1 is :\n',p1)
    p2 = np.poly1d(f2)
    print('p2 is :\n',p2)

    #得到拟合值
    #x1.append(-29)
    x1np=np.array(x)
    yvals0 = p0(x1np)
    yvals1 = p1(x1np)
    yvals2 = p2(x1np)
    #x1.pop(-29)

    #得到三个交点
    pc0=getcrosspoint(f0,f1)
    pc1=getcrosspoint(f1,f2)
    pc2=getcrosspoint(f0,f2)

    print '三个交点'
    print pc0
    print pc1
    print pc2

    #得到三个交点的重心
    print '密度中心：'
    print result1,result2,result3
    print '交点的重心：'
    rtcp=get_centerpoint([pc0,pc1,pc2])
    #print '密度中心的的重心：'
    #rtcp=get_centerpoint([result1,result2,result3])

    print rtcp

    print calc_angle([rtcp,result1])
    print calc_angle([rtcp,result2])
    print calc_angle([rtcp,result3])
    #


    x2=[]
    y2=[]

    x2.append(result1[0])
    y2.append(result1[1])
    x2.append(result2[0])
    y2.append(result2[1])
    x2.append(result3[0])
    y2.append(result3[1])


    plot1 = plt.plot(x, y, 's',label='original poinits')
    plot2 = plt.plot(x2, y2, 's',label='new points')
    plot3 = plt.plot(x1np,yvals0,'r',color='black',label='0')
    plot3 = plt.plot(x1np,yvals1,'r',color='gray',label='1')
    plot3 = plt.plot(x1np,yvals2,'r',color='blue',label='2')
    plot4=plt.plot([rtcp[0]],[rtcp[1]],'s',color='red',label='3')

    #plt.legend(loc=1) #指定legend的位置右下角
    #plt.title('algorithm')

    #plt.xlim(-30,20 )
    #plt.ylim(-10,20)
    #plt.show()


if __name__ == '__main__':
    #run1()
    #0.0003  迭代时间最长
    #0.003   差不多的 但是结果没变啊。
    mst=MeanShiftTest('data/data10.csv')
    #mst.run(0.03)
    #mst.run2(0.003)
    mst.run1(0.03)
    #bandwidth=0.000003


