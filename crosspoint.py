# -*- coding: utf-8 -*-
class Point(object):
    x =0
    y= 0
    # 定义构造方法
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def GetLinePara(line):
    line.a =line.p1.y - line.p2.y;
    line.b = line.p2.x - line.p1.x;
    line.c = line.p1.x *line.p2.y - line.p2.x * line.p1.y;


def GetCrossPoint(l1,l2):

    GetLinePara(l1);
    GetLinePara(l2);
    d = l1.a * l2.b - l2.a * l1.b
    p=Point()
    p.x = (l1.b * l2.c - l2.b * l1.c)*1.0 / d
    p.y = (l1.c * l2.a - l2.c * l1.a)*1.0 / d
    return p;
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
    p=Point()
    x = (b0 * c1 - b1 * c0)*1.0 / d
    y = (c0 * a1 - c1 * a0)*1.0 / d
    return [x,y]


p1=Point(1,1)
p2=Point(3,3)
line1=Line(p1,p2)

p3=Point(2,3.1)
p4=Point(3.1,2)

#p3=Point(1,0)
#p4=Point(2,1)
line2=Line(p3,p4)
Pc = GetCrossPoint(line1,line2);

#如何考虑垂直 水平的问题，
print("Cross point:", Pc.x, Pc.y);
print ("new ",getcrosspoint([0,1],[-1,5.1]) )