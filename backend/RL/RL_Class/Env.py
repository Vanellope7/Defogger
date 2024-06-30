import functools
import operator
from functools import reduce
from operator import mul

import networkx as nx
import numpy as np
import pandas as pd

from . import Laplace
from scipy.stats import laplace


def edge_importance_with_node_weight(graph, edges, node_weights, method='degree'):
    """
    计算图中每条边的重要性，并按照重要性排序，考虑节点的权重

    参数：
    - graph: NetworkX 图对象
    - node_weights: 字典，节点的重要性权重，键为节点，值为权重
    - method: 计算边重要性的方法，可选 'degree' 或 'pagerank'，默认为 'degree'

    返回值：
    - sorted_edges: 按照重要性排序的边列表
    - edge_importance_dict: 字典，键为边，值为对应的重要性
    """
    edge_importance_dict = {}

    if method == 'degree':
        centrality = nx.degree_centrality(graph)
    elif method == 'pagerank':
        centrality = nx.pagerank(graph)
    elif method == 'betweenness':
        centrality = nx.betweenness_centrality(graph)
    else:
        raise ValueError("Invalid method. Please choose 'degree' or 'pagerank'.")

    for edge in edges:
        weight_u = node_weights[edge[0]]
        weight_v = node_weights[edge[1]]
        edge_importance_dict[tuple(edge)] = (centrality[edge[0]] + centrality[edge[1]]) * (weight_u + weight_v)

    # 按照重要性对边进行排序
    # sorted_edges = sorted(edge_importance_dict.items(), key=lambda x: x[1], reverse=True)

    return edge_importance_dict


def newMergeDict(rawDict, Qlist, noise, multiQuery=[], trueQueries=[]):
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        keys = list(d.keys())
        for k, v in d.items():
            keyIdx = keys.index(k)
            new_key = parent_key + sep + str(keyIdx) if parent_key else str(keyIdx)
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((tuple(new_key.split('_')), v))
        return dict(items)

    sumQList = []
    for q in Qlist:
        t = [0]
        if type(q) == int:
            sumQList.append([])
            continue
        for v in q:
            t.append(t[-1]+v)
        sumQList.append(t)

    errorRet, queryResNum = 0, 0
    flat_dict = flatten_dict(rawDict)
    flat_dict_keys = list(flat_dict.keys())
    for query in trueQueries:
        queryIdx = list(map(lambda d: multiQuery.index(d), query))

        otherQueryAttrIdx = [multiQuery.index(attr) for attr in multiQuery if attr not in query]
        multiNoise = 1
        for attrIdx in otherQueryAttrIdx:
            if type(Qlist[attrIdx]) == int:
                multiNoise *= Qlist[attrIdx]
            else:
                multiNoise *= len(Qlist[attrIdx])
        temp = {}
        for key in flat_dict_keys:
            if temp.get(key, -1) != -1:
                continue


            GroupList = []
            for i in queryIdx:
                kiv = key[i]
                sumQ = sumQList[i]
                if len(sumQ) == 0:
                    GroupList.append([int(kiv)])
                for t in range(len(sumQ)):
                    if int(kiv) < sumQ[t]:
                        GroupList.append(list(range(sumQ[t-1], sumQ[t])))
                        break
            filterKeyList = flat_dict_keys
            for i, group in zip(queryIdx, GroupList):
                filterKeyList = list(filter(lambda d: int(d[i]) in group, filterKeyList))
            avgV = sum(list(map(lambda d: flat_dict[d], filterKeyList))) / len(filterKeyList)
            for fk in filterKeyList:
                temp[fk] = avgV
                if flat_dict[fk] == 0:
                    flat_dict[fk] = 0.5
                errorRet += (abs(temp[fk] - flat_dict[fk]) + multiNoise * noise / len(filterKeyList)) / flat_dict[fk]

    return errorRet / len(flat_dict_keys)

def mergeDict(rawDict, mergeSizeList, noise, multiQuery=[], trueQueries=[]):

    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        keys = list(d.keys())
        for k, v in d.items():
            keyIdx = keys.index(k)
            new_key = parent_key + sep + str(keyIdx) if parent_key else str(keyIdx)
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((tuple(new_key.split('_')), v))
        return dict(items)

    errorRet, queryResNum = 0, 0
    flat_dict = flatten_dict(rawDict)
    flat_dict_keys = list(flat_dict.keys())
    for query in trueQueries:
        queryIdx = list(map(lambda d: multiQuery.index(d), query))
        temp = {}
        totalRate = reduce(mul, mergeSizeList)
        for i in queryIdx:
            size = mergeSizeList[i]
            if size == 1:
                for key in flat_dict_keys:
                    newKey = list(key)
                    temp[key] = flat_dict[key]
            else:
                for key in flat_dict_keys:
                    newKey = list(key)
                    newKey[i] = str((int(newKey[i])) // size)
                    tnewKey = tuple(newKey)
                    temp[tnewKey] = temp.get(tnewKey, 0)
                    temp[tnewKey] += flat_dict[key]
        for key in flat_dict_keys:
            newKey = list(key)
            for i, size in enumerate(mergeSizeList):
                if size == 1:
                    continue
                else:
                    newKey = list(key)
                    if i > len(newKey)-1:
                        print('xxx')
                    newKey[i] = str((int(newKey[i])) // size)
            newKey = tuple(newKey)
            if flat_dict[key] == 0:
                flat_dict[key] = 0.5
            errorRet += (abs(temp[newKey] / totalRate - flat_dict[key]) + noise / totalRate) / flat_dict[key]
        queryResNum += len(temp.keys())

    return errorRet / len(flat_dict_keys), queryResNum


class Env:
    def __init__(self, queryList, queryRet, AttrSensitive, isRawQuery, rawQueryList):
        # 多查询的解决方案 以及 多查询的准确率方案
        self.queryList = queryList
        self.rawQueryList = rawQueryList
        self.isRawQuery = isRawQuery
        self.x = 0
        self.map = np.arange(len(queryList))
        self.data = pd.read_csv('./Data/cost_of_living_us.csv')
        self.minGranularityQueryRet = []

        self.sensitivities = []
        self.Attrs = list(set(item for sublist in queryList for item in sublist))
        self.queryAttrs = queryList
        self.queryGraph = nx.Graph()

        rawQueryEdgeList = []
        for rawquery in rawQueryList:
            if len(rawquery) > 2:
                for i in range(len(rawquery)):
                    for j in range(len(rawquery)):
                        if i < j:
                            rawQueryEdgeList.append((rawquery[i], rawquery[j]))
            else:
                rawQueryEdgeList.append(rawquery)
        self.queryGraph.add_edges_from(rawQueryEdgeList)
        node_weights = {}
        for attr, isSensitive in AttrSensitive.items():
            if isSensitive:
                node_weights[attr] = 1
            else:
                node_weights[attr] = 0

        eid = self.edge_importance_dict = edge_importance_with_node_weight(self.queryGraph, rawQueryList, node_weights, method='betweenness')
        self.multiAttr2QueryMap = {}
        if not isRawQuery:
            # 处理多属性的 edge important
            for query in queryList:
                if eid.get(tuple(query), -1) == -1:
                    self.multiAttr2QueryMap[tuple(query)] = []
                    eid[tuple(query)] = 0
                    for otherQuery in rawQueryList:
                        if otherQuery[0] in query and otherQuery[1] in query:
                            eid[tuple(query)] += eid[tuple(otherQuery)]
                            self.multiAttr2QueryMap[tuple(query)].append(tuple(otherQuery))
        # self.queryRange = queryRange
        # self.minQueryGranularity = mgl
        self.minGranularityQueryRet = queryRet


        # self.curQueryGranularity = [10000, 10000, 10000, 10000]
        # for index, query in enumerate(queryList):
        #     attr = query[1]
        #     value_min, value_max, minGranularity = self.queryRange[index][0], self.queryRange[index][1], self.minQueryGranularity[index]
        #     # 最小粒度查询结果
        #     bins = list(range(value_min, value_max + minGranularity, minGranularity))
        #     labels = [f'Range_{i}~{i+minGranularity}' for i in range(value_min, value_max, minGranularity)]
        #     df_count = pd.cut(self.data[attr], bins=bins, labels=labels, right=False)
        #     self.minGranularityQueryRet.append(df_count.value_counts().sort_index().replace(0, 1))
            # 当前查询结果
            # bins = list(range(value_min, value_max + granularity, granularity))
            # labels = [f'Range_{i}~{i+granularity}' for i in range(value_min, value_max, granularity)]
            # df_count = pd.cut(self.data[attr], bins=bins, labels=labels, right=False)
            # self.queryRet.append(df_count.value_counts().sort_index())
            # self.queryRet.append(self.data[attr].value_counts().values)
            # self.sensitivities.append(self.data[attr].value_counts().values.max())
            # if self.data[attr].dtype in ['int64', 'float64']:
            #     self.queryRange.append([self.data[attr].min(), self.data[attr].max()])
            # else:
            #     self.queryRange.append([])

    def get_observation(self):
        return self.map[self.x]  # 返回现在在所

    def get_target(self, action, state, rateList, simulateResult, queryIdx):
        state_after = state + 1
        score = self.newGetAccuracy(action, state, rateList, simulateResult, queryIdx)

        return state_after, score

    # def getAccuracy(self, action, state):
    #     L = Laplace(1/action)
    #     # 50% 噪声的平均误差
    #     return L.laplace_F(0.5) - L.laplace_F(-0.5)

    def getAccuracy(self, action, state, rateList, simulateResult, queryIdx):
        noise = laplace.ppf(0.95, loc=0, scale=1 / action)
        curQueryRet = self.minGranularityQueryRet[state-1]
        if len(self.queryList[queryIdx]) > 2:
            error, queryResNum = mergeDict(simulateResult, rateList, noise, self.queryList[queryIdx], self.multiAttr2QueryMap[tuple(self.queryList[queryIdx])])
        else:
            error, queryResNum = mergeDict(simulateResult, rateList, noise, self.queryList[queryIdx], [self.queryList[queryIdx]])
        noiseDiv = functools.reduce(operator.mul, rateList)
        noiseMul = 1
        singleAcc = error #  + noise / noiseDiv * noiseMul
        queryWeight = self.edge_importance_dict[tuple(self.queryList[queryIdx])]
        multiAcc = 0
        # for i in range(len(curQueryRet)-1):
        #     curSlope = curQueryRet[i+1] / curQueryRet[i]
        #     upSlope = (curQueryRet[i+1]+noise) / (curQueryRet[i]-noise)
        #     downSlope = (curQueryRet[i + 1] - noise) / (curQueryRet[i] + noise)
        #     multiAcc += max(upSlope-curSlope, curSlope-downSlope)
        # multiAcc /= len(curQueryRet)-1
        return queryWeight * (singleAcc + multiAcc)


    def newGetAccuracy(self, action, state, g, simulateResult, queryIdx):
        noise = laplace.ppf(0.95, loc=0, scale=1 / action)
        if len(self.queryList[queryIdx]) > 2:
            error = newMergeDict(simulateResult, g, noise, self.queryList[queryIdx], self.multiAttr2QueryMap[tuple(self.queryList[queryIdx])])
        else:
            error = newMergeDict(simulateResult, g, noise, self.queryList[queryIdx], [self.queryList[queryIdx]])

        singleAcc = error #  + noise / noiseDiv * noiseMul
        queryWeight = self.edge_importance_dict[tuple(self.queryList[queryIdx])]
        multiAcc = 0
        return queryWeight * (singleAcc + multiAcc)

    def retry(self):  # 初始化
        self.x = 0
        self.count = 0
