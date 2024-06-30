import json
from itertools import product

import networkx as nx
import numpy as np
import pandas as pd
from django.http import JsonResponse

from RL.Class import JsonEncoder
from RL.RL_Class.Env import Env
from RL.RL_Class.QL import QL
from RL.utils import find_closest_complete_subgraph, find_covering_subgraph_combinations, getDivisionList


def Strategy_recommend(request):
    postData = json.loads(request.body)
    queryList = postData['queryList']
    G = nx.Graph()
    G.add_edges_from(queryList)
    closest_complete_subgraph = find_closest_complete_subgraph(G)
    # completeEdgesList = list(map(lambda d: list(d.edges()), closest_complete_subgraph))
    strategyList = find_covering_subgraph_combinations(G, closest_complete_subgraph)
    # print(completeEdgesList)
    # for completeEdges in completeEdgesList:
    #     newEdgeList = []
    #     completeNodes = flat_list = list(set([item for sublist in completeEdges for item in sublist]))
    #     newEdgeList.append(completeNodes)
    #     for query in queryList:
    #         if query[0] not in completeNodes or query[1] not in completeNodes:
    #             newEdgeList.append(query)
    #     strategyList.append(newEdgeList)
    return JsonResponse({'strategyList': strategyList}, encoder=JsonEncoder)

def RL_recommend(request):
    postData = json.loads(request.body)
    # [[attr...],...]  [{}, {}]
    queryList, simulateResult = postData['queryList'], postData['simulateResult']
    N = postData['N']
    epsilon, attrTypeMap = postData['epsilon'], postData['attrTypeMap']
    AttrSensitive, rawQueryList = postData['AttrSensitive'], postData['rawQueryList']
    ExplorationProgressVal = postData['ExplorationProgressVal']
    isRawQuery = postData['isRawQuery']
    AttrRange = postData['AttrRange']
    # 过滤 queryList 中的完全非敏感查询
    tempQueryList, tempQueryRet = [], []
    for i in range(len(queryList)):
        if AttrSensitive[queryList[i][0]] or AttrSensitive[queryList[i][1]]:
            tempQueryList.append(queryList[i])
            tempQueryRet.append(simulateResult[i])
    queryList = tempQueryList
    simulateResult = tempQueryRet


    queryRateNumList = [len(query) for query in queryList]
    retList = []

    queryNum = len(queryList)
    total_epsilon = epsilon
    TIMES = 30
    if N < 10000:
        TIMES = 80
    actions = list(map(lambda d: round(d, 2), np.linspace(0.05, total_epsilon, round(epsilon/0.05))))
    people = QL(actions, queryNum, queryList, attrTypeMap, ExplorationProgressVal, epsilon, N, AttrRange)  # 生成QLearn主体的对象，包含left和right
    site = Env(queryList, simulateResult, AttrSensitive, isRawQuery, rawQueryList)  # 生成测试环境
    for episode in range(TIMES):
        # if episode % (TIMES // 10) == 0:
        #     people.change_greedy(people.epsilon + 0.1)
        # state = site.get_observation()  # 观察初始环境
        # site.draw()  # 生成图像
        # time.sleep(0.3)  # 暂停
        state = 1

        cur_epsilon = total_epsilon
        epsilonRetList = []
        totalRateList = []
        leftQueryIdxList = list(range(queryNum))
        queryIdxList = []
        # 先获取所有的 action
        for i in range(queryNum):
            action, rateList, queryIdx = people.choose_action(i + 1, cur_epsilon, len(queryList[i]), leftQueryIdxList)  # 获得下一步方向
            queryIdxList.append(queryIdx)
            leftQueryIdxList.remove(queryIdx)
            cur_epsilon -= action
            cur_epsilon = round(cur_epsilon, 2)
            epsilonRetList.append(action)
            totalRateList.append(rateList)
        # epsilonRetList = shuffle_list(epsilonRetList)
        cur_epsilon = total_epsilon
        leftQueryIdxList = list(range(queryNum))
        for i in range(queryNum):
            cur_epsilon -= epsilonRetList[i]
            cur_epsilon = round(cur_epsilon, 2)
            queryIdx = queryIdxList[i]
            state_after, score = site.get_target(epsilonRetList[i], state, totalRateList[i], simulateResult[queryIdx], queryIdx)  # 获得下一步的环境的实际情况
            leftQueryIdxList.remove(queryIdx)
            people.learn(state, epsilonRetList[i], score, state_after, cur_epsilon, totalRateList[i], queryIdx, leftQueryIdxList)  # 根据所处的当前环境对各个动作的预测得分和下一步的环境的实际情况更新当前环境的q表
            state = state_after  # 状态更新
    print(people.q_table)



    firstEpsilonAllocateSeries = people.q_table[1][people.q_table[1] != 0]
    minReward = firstEpsilonAllocateSeries.min()
    firstEpsilonAllocate = firstEpsilonAllocateSeries[firstEpsilonAllocateSeries == firstEpsilonAllocateSeries.min()].index[0]
    print(people.q_table[1][people.q_table[1] != 0].min())
    leftEpsilon = firstEpsilonAllocate[1]
    firstQueryIdx = firstEpsilonAllocate[2][0]
    leftQueryIdxList = list(range(queryNum))
    leftQueryIdxList.remove(firstQueryIdx)

    granularityMap = people.getGranularityMap()
    minEpsilonAllocate = [firstEpsilonAllocate]
    for i in range(2, queryNum + 1):
        learnColumns = []
        for e in np.arange(1, round(leftEpsilon * 20) + 1, 1):
            e = round(e / 20, 2)
            for idx in leftQueryIdxList:
                for rl in pd.MultiIndex.from_product([granularityMap[attr] for attr in queryList[idx]]):
                    learnColumns.append((round(e, 2), round(leftEpsilon - e, 2), tuple([idx, *rl])))
        learnColumns = pd.MultiIndex.from_tuples(learnColumns)
        curEpsilonAllocateSeries = people.q_table[i][learnColumns][people.q_table[i][learnColumns] != 0]
        curEpsilonAllocate = \
        curEpsilonAllocateSeries[curEpsilonAllocateSeries == curEpsilonAllocateSeries.min()].index[0]

        leftEpsilon = curEpsilonAllocate[1]
        minEpsilonAllocate.append(curEpsilonAllocate)
        leftQueryIdxList.remove(curEpsilonAllocate[2][0])
    QuerySeq = list(map(lambda d: d[2][0], minEpsilonAllocate))
    QueryEpsilonList = list(map(lambda d: d[0], minEpsilonAllocate))
    QueryGranularity = list(map(lambda d: d[2][1:], minEpsilonAllocate))

    QueryGranularityTemp = []
    for i in QuerySeq:
        curQuery = queryList[i]
        data = simulateResult[i]
        epsilon = QueryEpsilonList[i]
        granularityMap = {}
        for attr in curQuery:
            if granularityMap.get(attr, -1) == -1:
                if attrTypeMap[attr] == '#':
                    granularityMap[attr] = getDivisionList(len(AttrRange[attr])-1)
                else:
                    granularityMap[attr] = [len(AttrRange[attr])]
        Glist = list(map(lambda d: granularityMap[d], curQuery))
        GGroups = list(product(*Glist))
        minV = float('inf')
        minG = ''
        for g in GGroups:
            curV = site.newGetAccuracy(epsilon, 0, g, data, i)
            if curV < minV:
                minV = curV
                minG = g
        print(minG)
        if len(QuerySeq) == 1:
            print(site.newGetAccuracy(epsilon, 0, ((1,1,1,1,4), 3, (1,1,1,2,1,2)), data, i))
            print(site.newGetAccuracy(epsilon, 0, minG, data, i))
        QueryGranularityTemp.append(minG)

    return JsonResponse({'QuerySeq': QuerySeq, 'QueryEpsilonList': QueryEpsilonList, 'QueryGranularity': QueryGranularityTemp, 'minReward': minReward}, encoder=JsonEncoder)


