import itertools
import json
import random
from collections import Counter

import numpy as np
import pandas as pd
from django.http import JsonResponse
from scipy.stats import norm

from RL.Class import JsonEncoder


def CorrelatedHistogram(request):
    postData = json.loads(request.body)
    [f1, f2, f3] = postData['firstAttr']
    [s1, s2, s3] = postData['secondAttr']
    attrList = postData['attrList']
    sample_size = postData['size']
    correlate = postData['correlate']


    isNumerical1 = False
    isNumerical2 = False
    if f1:
        sampleCategories1 = list(f2.keys())
        sampleMap1 = {string: idx for idx, string in enumerate(sampleCategories1)}
        RsampleMap1 = {idx: string for idx, string in enumerate(sampleCategories1)}
        HistogramData1 = np.array(list(f2.values()))
        HistogramKey1 = list(f2.keys())
        hist1 = HistogramData1 / sum(HistogramData1)
        temp = np.random.choice(len(hist1), size=sample_size, p=hist1)
        sample1 = []
        for d in temp:
            keys = HistogramKey1[d].split('-')
            if len(keys) > 1:
                sample1.append(random.uniform(float(keys[0]), float(keys[1])))
                isNumerical1 = True
            else:
                sample1.append(d)
    else:
        HistogramKey1 = []
        if type(f3[0]) != str:
            for i in range(len(f3)):
                if i != 0:
                    HistogramKey1.append(f3[i-1] + '-' + f3[i])
            isNumerical1 = True
            sample1 = f2
        else:
            HistogramKey1 = f3
            sampleMap1 = {string: idx for idx, string in enumerate(HistogramKey1)}
            sample1 = list(map(lambda d: sampleMap1[d], f2))

    if s1:
        sampleCategories2 = list(s2.keys())
        sampleMap2 = {string: idx for idx, string in enumerate(sampleCategories2)}
        RsampleMap2 = {idx: string for idx, string in enumerate(sampleCategories2)}
        HistogramData2 = np.array(list(s2.values()))
        HistogramKey2 = list(s2.keys())
        hist2 = HistogramData2 /  sum(HistogramData2)
        temp = np.random.choice(len(hist2), size=sample_size, p=hist2)
        sample2 = []
        for d in temp:
            keys = HistogramKey2[d].split('-')
            if len(keys) > 1:
                sample2.append(random.uniform(float(keys[0]), float(keys[1])))
                isNumerical2 = True
            else:
                sample2.append(d)
    else:
        HistogramKey2 = []
        if type(s3[0]) != str:
            for i in range(len(s3)):
                if i != 0:
                    HistogramKey2.append(s3[i-1] + '-' + s3[i])
            isNumerical2 = True
            sample2 = s2
        else:
            HistogramKey2 = s3
            sampleMap2 = {string: idx for idx, string in enumerate(HistogramKey2)}
            sample2 = list(map(lambda d: sampleMap2[d], s2))

    correlation_matrix = np.array([[1.0, correlate],
                                   [correlate, 1.0]])
    mvnorm_samples = np.random.multivariate_normal(mean=np.zeros(2), cov=correlation_matrix, size=sample_size)

    # 将正态样本转换为具有直方图分布的样本
    u1 = norm.cdf(mvnorm_samples[:, 0])
    u2 = norm.cdf(mvnorm_samples[:, 1])


    if True:
        cLen = len(HistogramKey1)
        countMap = Counter(sample1)
        now = 0
        sum_list = []
        for i in range(cLen):
            sum_list.append(now + countMap[i])
            now = sum_list[-1]
        pre = 0
        idx = 0
        for v in sum_list:
            if v == sample_size:
                upper_indices = np.array(range(sample_size))
            else:
                upper_indices = np.argpartition(u1, v)[:v]
            lower_indices = np.argpartition(u1, pre)[:pre]
            intersection_count = np.setdiff1d(upper_indices, lower_indices)
            if not isNumerical1:
                u1[intersection_count] = idx
            else:
                u1[intersection_count] = idx
            idx += 1
            pre = v
    if not isNumerical2:
        cLen = len(HistogramKey2)
        countMap = Counter(sample2)
        now = 0
        sum_list = []
        for i in range(cLen):
            sum_list.append(now + countMap[i])
            now = sum_list[-1]
        pre = 0
        idx = 0
        for v in sum_list:
            if v == sample_size:
                upper_indices = np.array(range(sample_size))
            else:
                upper_indices = np.argpartition(u2, v)[:v]
            lower_indices = np.argpartition(u2, pre)[:pre]
            intersection_count = np.setdiff1d(upper_indices, lower_indices)
            u2[intersection_count] = idx
            idx += 1
            pre = v

    corRet = {}
    for key1 in HistogramKey1:
        corRet[key1] = {}
        for key2 in HistogramKey2:
            if isNumerical1 and isNumerical2:
                c1 = key1.split('-')
                c2 = key2.split('-')
                corRet[key1][key2] = len(list(filter(lambda d: float(c1[0])<=d[0]<float(c1[1]) and float(c2[0])<=d[1]<float(c2[1]), correlated_samples)))
            elif not isNumerical1 and not isNumerical2:
                corRet[key1][key2] = len(list(
                    filter(lambda d: d[0] == sampleMap1[key1] and d[1] == sampleMap2[key2],
                           correlated_samples)))
            elif not isNumerical1 and isNumerical2:
                c2 = key2.split('-')
                corRet[key1][key2] = len(list(
                    filter(lambda d: d[0] == sampleMap1[key1] and float(c2[0]) <= d[1] < float(c2[1]),
                           correlated_samples)))
            elif isNumerical1 and not isNumerical2:
                c1 = key1.split('-')
                corRet[key1][key2] = len(list(
                    filter(lambda d: float(c1[0]) <= d[0] < float(c1[1]) and d[1] == sampleMap2[key2],
                           correlated_samples)))
    # 附带的敏感属性分布直方图结果
    # sensitiveRet = {}
    # for condition in SensitiveHistogramKey:
    #     sensitiveRet[str(condition)] = len(list(filter(lambda d: float(condition[0])<=d[1]<float(condition[1]), correlated_samples)))

    return JsonResponse({'corRet': corRet}, encoder=JsonEncoder)