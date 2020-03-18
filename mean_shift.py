# -*- coding: utf-8 -*-
import numpy as np
import point_grouper as pg
import mean_shift_utils as ms_utils

MIN_DISTANCE = 0.00000001


class MeanShift(object):
    def __init__(self, kernel=ms_utils.gaussian_kernel):
        #默认传进来的高斯核函数
        if kernel == 'multivariate_gaussian':
            kernel = ms_utils.multivariate_gaussian_kernel
        self.kernel = kernel

    def cluster(self, points, kernel_bandwidth, iteration_callback=None):
        if(iteration_callback):
            iteration_callback(points, 0)
        #将这些点的集合变成np的数组
        shift_points = np.array(points)
        #最大最小距离？
        max_min_dist = 1
        iteration_number = 0

        #shape[0] 代表行数，[true........]  多少个点就多少个，这就是个标志位
        still_shifting = [True] * points.shape[0]

        #应该是这个最小的欧氏距离小到一定的程度，我就停止移位我的点
        while max_min_dist > MIN_DISTANCE:
            # print max_min_dist
            max_min_dist = 0
            iteration_number += 1

            #这个小循环遍历每一个点集合X
            for i in range(0, len(shift_points)):
                if not still_shifting[i]:    #标志位，如果没有漂移过
                    continue
                p_new = shift_points[i]
                p_new_start = p_new
                #这个点已经漂移完了
                p_new = self._shift_point(p_new, points, kernel_bandwidth)
                #计算漂移的欧氏距离
                dist = ms_utils.euclidean_dist(p_new, p_new_start)
                #一轮轮得到最小的欧氏距离
                if dist > max_min_dist:
                    max_min_dist = dist
                if dist < MIN_DISTANCE:
                    still_shifting[i] = False
                shift_points[i] = p_new
            if iteration_callback:
                iteration_callback(shift_points, iteration_number)
        point_grouper = pg.PointGrouper()
        group_assignments = point_grouper.group_points(shift_points.tolist())
        return MeanShiftResult(points, shift_points, group_assignments)

    #传进来的都是一个小区的，所以都是一个类别，只需要返回一个密度中心点就行，
    def cluster_cell(self, points, kernel_bandwidth, iteration_callback=None):
        if(iteration_callback):
            iteration_callback(points, 0)
        #将这些点的集合变成np的数组
        shift_points = np.array(points)
        #最大最小距离？
        max_min_dist = 1
        iteration_number = 0

        #shape[0] 代表行数，[true........]  多少个点就多少个，这就是个标志位
        still_shifting = [True] * points.shape[0]

        #应该是这个最小的欧氏距离小到一定的程度，我就停止移位我的点
        while max_min_dist > MIN_DISTANCE:
            # print max_min_dist
            max_min_dist = 0
            iteration_number += 1

            #这个小循环遍历每一个点集合X
            for i in range(0, len(shift_points)):
                if not still_shifting[i]:    #标志位，如果没有漂移过
                    continue
                p_new = shift_points[i]
                p_new_start = p_new
                #这个点已经漂移完了
                p_new = self._shift_point(p_new, points, kernel_bandwidth)
                #计算漂移的欧氏距离
                dist = ms_utils.euclidean_dist(p_new, p_new_start)
                #一轮轮得到最小的欧氏距离
                if dist > max_min_dist:
                    max_min_dist = dist
                if dist < MIN_DISTANCE:
                    still_shifting[i] = False
                shift_points[i] = p_new
            if iteration_callback:
                iteration_callback(shift_points, iteration_number)
        #此处一个基站只有一个密度中心,所以求shift_points 的均值
        print "iter:"
        print iteration_number
        return self.getcenterpoint_from_array(shift_points)

    def getcenterpoint_from_array(self,shift_points):
        #print 'orignal shifted points'
        #print shift_points
        points=shift_points.tolist()
        sumx=0.0
        sumy=0.0
        for point in points:
            sumx+=point[0]
            sumy+=point[1]
        x=sumx/len(points)
        y=sumy/len(points)
        return [x,y]
    def getcenterpoint_from_array_most(self,shift_points):
        points=shift_points.tolist()
        cnt={}
        cntlist=[]
        tmp={}
        for p in points:

            p1=str(p)
            if p1 not in cntlist:#说明不在 第一次，那么cnt中加上
                cntlist.append(p)
                cnt[p1]=1
            else: #说明有啊，cnt里面继续++
                cnt[p1]=cnt[p1]+1
        num=0

        for l in cntlist:   #返回最大的 众数
            l0=str(l)
            if num<cnt[l0]:
                num=cnt[l0]
                rtl=l
        return rtl
        pass
    def _shift_point(self, point, points, kernel_bandwidth):
        # from http://en.wikipedia.org/wiki/Mean-shift
        points = np.array(points)

        # numerator
        #这是分母
        #返回了所有的点的偏移距离
        point_weights = self.kernel(point-points, kernel_bandwidth)
        #这是分子
        #这个函数的意思是，将这个东西进行重复输出
        tiled_weights = np.tile(point_weights, [len(point), 1])
        # denominator
        denominator = sum(point_weights)
        #得到计算最后的点
        shifted_point = np.multiply(tiled_weights.transpose(), points).sum(axis=0) / denominator
        #此处得到了一个二维的点
        return shifted_point

        # ***************************************************************************
        # ** The above vectorized code is equivalent to the unrolled version below **
        # ***************************************************************************
        # shift_x = float(0)
        # shift_y = float(0)
        # scale_factor = float(0)
        # for p_temp in points:
        #     # numerator
        #     dist = ms_utils.euclidean_dist(point, p_temp)
        #     weight = self.kernel(dist, kernel_bandwidth)
        #     shift_x += p_temp[0] * weight
        #     shift_y += p_temp[1] * weight
        #     # denominator
        #     scale_factor += weight
        # shift_x = shift_x / scale_factor
        # shift_y = shift_y / scale_factor
        # return [shift_x, shift_y]


class MeanShiftResult:
    def __init__(self, original_points, shifted_points, cluster_ids):
        self.original_points = original_points
        self.shifted_points = shifted_points
        self.cluster_ids = cluster_ids
