# -*- coding: utf-8 -*-
import math
import numpy as np


def euclidean_dist(pointA, pointB):
    try:
        if(len(pointA) != len(pointB)):
            raise Exception("expected point dimensionality to match")
        total = float(0)
        for dimension in range(0, len(pointA)):
            total += (pointA[dimension] - pointB[dimension])**2
        return math.sqrt(total)
    except:
        return 0

#高斯核函数，计算“标准化之后的” 偏移距离,返回所有的偏移距离
def gaussian_kernel(distance, bandwidth):
    tmp1=((distance)**2)
    tmp=tmp1.sum(axis=1)
    euclidean_distance = np.sqrt(tmp)
    val = (1/(bandwidth*math.sqrt(2*math.pi))) * np.exp(-0.5*((euclidean_distance / bandwidth))**2)
    return val


def multivariate_gaussian_kernel(distances, bandwidths):

    # Number of dimensions of the multivariate gaussian
    dim = len(bandwidths)

    # Covariance matrix
    cov = np.multiply(np.power(bandwidths, 2), np.eye(dim))

    # Compute Multivariate gaussian (vectorized implementation)
    exponent = -0.5 * np.sum(np.multiply(np.dot(distances, np.linalg.inv(cov)), distances), axis=1)
    val = (1 / np.power((2 * math.pi), (dim/2)) * np.power(np.linalg.det(cov), 0.5)) * np.exp(exponent)

    return val

def getcrosspoint(f0,f1):
    k0=f0[0]
    m0=f0[1]
    k1=f1[0]
    m1=f1[1]
    a0=k0
    b0=-1
    c0=m0
    a1=k1
    b1=-1
    c1=m1
    d = a0 * b1 - a1 * b0
    x = (b0 * c1 - b1 * c0)*1.0 / d
    y = (c0 * a1 - c1 * a0)*1.0 / d
    return [x,y]

def get_centerpoint(lis):
    area = 0.0
    x,y = 0.0,0.0

    a = len(lis)
    for i in range(a):
        lat = lis[i][0]     #weidu
        lng = lis[i][1]      #jingdu

        if i == 0:
            lat1 = lis[-1][0]
            lng1 = lis[-1][1]
            #print lis[-1][0]
            #print lis[-1][1]

        else:
            lat1 = lis[i-1][0]
            lng1 = lis[i-1][1]

        fg = (lat*lng1 - lng*lat1)/2.0

        area += fg
        x += fg*(lat+lat1)/3.0
        y += fg*(lng+lng1)/3.0

    x = x/area
    y = y/area

    return [x,y]

def calc_angle(lis):
    x_point_s=lis[0][0]
    y_point_s=lis[0][1]
    x_point_e=lis[1][0]
    y_point_e=lis[1][1]
    angle=0
    y_se= y_point_e-y_point_s;
    x_se= x_point_e-x_point_s;
    if x_se==0 and y_se>0:
        angle = 360
    if x_se==0 and y_se<0:
        angle = 180
    if y_se==0 and x_se>0:
        angle = 90
    if y_se==0 and x_se<0:
        angle = 270
    if x_se>0 and y_se>0:
       angle = math.atan(x_se/y_se)*180/math.pi
    elif x_se<0 and y_se>0:
       angle = 360 + math.atan(x_se/y_se)*180/math.pi
    elif x_se<0 and y_se<0:
       angle = 180 + math.atan(x_se/y_se)*180/math.pi
    elif x_se>0 and y_se<0:
       angle = 180 + math.atan(x_se/y_se)*180/math.pi
    return angle