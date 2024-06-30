import itertools
import json
import random
from collections import Counter, defaultdict
from dcor import distance_correlation

import numpy as np
import pandas as pd
from django.http import JsonResponse
from scipy.stats import norm, stats, spearmanr

from RL.Class import JsonEncoder


def GetAttrCorrelation(request):
    postData = json.loads(request.body)
    queryRes = postData['queryRes']
    AttrTypeList = postData['AttrTypeList']
    keys1 = list(queryRes.keys())
    keys2 = list(queryRes[keys1[0]].keys())

    isNumerical1 = False if AttrTypeList[0] == 'A' else True
    isNumerical2 = False if AttrTypeList[1] == 'A' else True

    sample_list = []
    for key1 in keys1:
        for key2 in keys2:
            if key2 not in queryRes[key1].keys():
                continue
            if isNumerical1 and isNumerical2:
                vl1 = key1.split('-')
                vl2 = key2.split('-')
                for t in range(queryRes[key1][key2]):
                    s1, s2 = np.random.uniform(float(vl1[0]), float(vl1[1])), np.random.uniform(float(vl2[0]), float(vl2[1]))
                    sample_list.append((s1, s2))
            elif not isNumerical1 and isNumerical2:
                ki1 = keys1.index(key1)
                vl2 = key2.split('-')
                for t in range(queryRes[key1][key2]):
                    s2 = np.random.uniform(float(vl2[0]), float(vl2[1]))
                    sample_list.append((ki1, s2))
            elif isNumerical1 and not isNumerical2:
                vl1 = key1.split('-')
                s1 = np.random.uniform(float(vl1[0]), float(vl1[1]))
                for t in range(queryRes[key1][key2]):
                    ki2 = keys2.index(key2)
                    sample_list.append((s1, ki2))
            elif not isNumerical1 and not isNumerical2:
                ki1 = keys1.index(key1)
                ki2 = keys2.index(key2)
                for t in range(queryRes[key1][key2]):
                    sample_list.append((ki1, ki2))
    sample_list = np.array(sample_list)
    correlation, p = spearmanr(sample_list[:,0], sample_list[:,1])
    return JsonResponse({'correlation': correlation}, encoder=JsonEncoder)


def CorrelatedHistogram(request):
    postData = json.loads(request.body)
    QueryResList = postData['QueryResList']
    QueryBinRangeList = postData['QueryBinRangeList']
    sample_size = postData['size']
    correlate = postData['correlate']
    AttrTypeList = postData['AttrTypeList']
    attrNum = len(QueryResList)

    CurQueryResList = GranularitySwitch(QueryResList, QueryBinRangeList, AttrTypeList)
    keysList = list(map(lambda d: list(d.keys()), CurQueryResList))
    isNumericalList = list(map(lambda d: True if d =='#' else False, AttrTypeList)) #[False if len(keys[0].split('-')) == 1 else True for keys in keysList]
    valuesList = list(map(lambda d: list(d.values()) / np.sum(list(d.values())), CurQueryResList))
    sumPList = []
    for values in valuesList:
        sum_p = [0]
        for v in values:
            sum_p.append(sum_p[-1] + v)
        sumPList.append(sum_p)


    for i in range(len(correlate)):
        for j in range(len(correlate[i])):
            if correlate[i][j] is None:
                correlate[i][j] = 0
    correlation_matrix = np.array(correlate)
    mvnorm_samples = np.random.multivariate_normal(mean=np.zeros(attrNum), cov=correlation_matrix, size=sample_size)

    # 将正态样本转换为具有直方图分布的样本
    uList = []
    for i in range(attrNum):
        u = norm.cdf(mvnorm_samples[:, i])
        uList.append(u)
    samplesHistList = []
    for i in range(attrNum):
        samples_hist = norm2histogram(uList[i], keysList[i], sumPList[i], isNumericalList[i])
        samplesHistList.append(samples_hist)
    ret = []
    for i in range(attrNum):
        for j in range(attrNum):
            if i != j:
                corRet = {}
                ret.append([corRet])
                keys1, keys2 = keysList[i], keysList[j]
                isNumerical1, isNumerical2 = isNumericalList[i], isNumericalList[j]
                samples_hist1, samples_hist2 = samplesHistList[i], samplesHistList[j]
                for key1 in keys1:
                    corRet[key1] = {}
                    for key2 in keys2:
                        if isNumerical1 and isNumerical2:
                            c1 = key1.split('-')
                            c2 = key2.split('-')
                            corRet[key1][key2] = np.sum(
                                (samples_hist1 < float(c1[1])) & (samples_hist1 > float(c1[0])) & (
                                            samples_hist2 < float(c2[1])) & (samples_hist2 > float(c2[0])))
                        elif not isNumerical1 and not isNumerical2:
                            k1Idx = keys1.index(key1)
                            k2Idx = keys2.index(key2)
                            corRet[key1][key2] = np.sum((samples_hist1 == k1Idx) & (samples_hist2 == k2Idx))
                        elif not isNumerical1 and isNumerical2:
                            k1Idx = keys1.index(key1)
                            c2 = key2.split('-')
                            corRet[key1][key2] = np.sum((samples_hist1 == k1Idx) & (samples_hist2 < float(c2[1])) & (
                                        samples_hist2 > float(c2[0])))
                        elif isNumerical1 and not isNumerical2:
                            c1 = key1.split('-')
                            k2Idx = keys2.index(key2)
                            corRet[key1][key2] = np.sum(
                                (samples_hist1 < float(c1[1])) & (samples_hist1 > float(c1[0])) & (
                                            samples_hist2 == k2Idx))
            else:
                corRet = {}
                ret.append([corRet])
                keys1 = keysList[i]
                isNumerical1 = isNumericalList[i]
                samples_hist1 = samplesHistList[i]
                for key1 in keys1:
                    if isNumerical1:
                        c1 = key1.split('-')
                        corRet[key1] = np.sum(
                            (samples_hist1 < float(c1[1])) & (samples_hist1 > float(c1[0])))
                    elif not isNumerical1:
                        k1Idx = keys1.index(key1)
                        corRet[key1] = np.sum((samples_hist1 == k1Idx))

    return JsonResponse({'ret': ret}, encoder=JsonEncoder)


def GranularitySwitch(QueryResList, QueryBinRangeList, AttrTypeList):
    queryNum = len(QueryResList)
    ret = []
    for i in range(queryNum):
        minGK = list(QueryResList[i].keys())
        minGV = list(QueryResList[i].values())
        curGK = QueryBinRangeList[i]
        isC = AttrTypeList[i] == 'A'
        if len(minGK) == len(curGK)-1 or (len(minGK) == len(curGK) and isC):
            ret.append(QueryResList[i])
        else:
            minScope = list(map(lambda d: int(d), minGK[0].split('-')))
            minWidth = minScope[1] - minScope[0]
            temp = {}
            minGKIdx = 0
            for idx in range(1, len(curGK)):
                num = int((curGK[idx] - curGK[idx-1]) / minWidth)
                temp['{0}-{1}'.format(curGK[idx-1], curGK[idx])] = sum(minGV[minGKIdx:minGKIdx+num])
                minGKIdx += num
            ret.append(temp)
    return ret

def norm2histogram(data, keys, p_list, isNumerical):
    for i in range(len(p_list)):
        if i != 0:
            if isNumerical:
                condition = (data < p_list[i]) & (data > p_list[i-1])
                keysList = keys[i-1].split('-')
                data[condition] = np.random.uniform(float(keysList[0]), float(keysList[1]), np.sum(condition))
            else:
                condition = (data < p_list[i]) & (data > p_list[i - 1])
                data[condition] = i-1
    return data