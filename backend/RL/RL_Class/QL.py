import itertools

import numpy as np
import pandas as pd

from RL.utils import getDivisionList



class QL:
    def __init__(self, actions, queryNum, queryList, attrTypeMap, ExplorationProgressVal, epsilon, N, AttrRange, learning_rate=1.0, reward_decay=1.0, e_greedy=0):
        self.N = N
        self.total_epsilon = epsilon
        self.queryList = queryList
        self.attrTypeMap = attrTypeMap
        self.actions = actions  # 初始化可以进行的各种行为，传入为列表
        self.lr = learning_rate  # 学习率，用于更新Q_table的值
        self.EP = ExplorationProgressVal
        self.qn = queryNum
        self.gamma = reward_decay  # 当没有到达终点时，下一环境对当前环境的影响  !!!这里必须设置为 1.0，因为目前每次查询的准确率是等效的，并不存在后拿的奖励 劣于 先拿的奖励的情况
        self.epsilon = e_greedy  # 随机选择几率为1-e_greedy，当处于e_greedy内时，不随机选择。
        self.AttrRange = AttrRange
        # self.columns = multiColumn = pd.MultiIndex.from_product([self.actions, [0] + self.actions, [1, 2, 4]])
        q_table = self.q_table = [{} for i in range(queryNum+1)] #pd.DataFrame(columns=multiColumn, dtype=np.float64)  # 生成q_table，列向量为columns

        temp = []
        granularityMap = {}
        for i in range(queryNum):
            productList = [[i]]
            for attr in queryList[i]:
                if attrTypeMap[attr] == '#':
                    if granularityMap.get(attr, -1) == -1:
                        granularityMap[attr] = getDivisionList(len(AttrRange[attr])-1)
                else:
                    if granularityMap.get(attr, -1) == -1:
                        granularityMap[attr] = [len(AttrRange[attr])]

                productList.append(granularityMap[attr])
            temp.extend(itertools.product(*productList))
        self.granularityMap = granularityMap
        for i in range(1, queryNum+1):
            multiColumn = pd.MultiIndex.from_product([self.actions, [0] + self.actions, temp])
            q_table[i] = pd.Series([0]*len(multiColumn), index=multiColumn, dtype=object)
            print('xxx')
        # print(q_table)

    def change_greedy(self, new_greedy):
        self.epsilon = new_greedy

    def choose_action(self, observation, cur_epsilon, queryAttrNum, leftQueryIdxList):
        queryNum = self.qn

        # if observation == queryNum:
        #     leftAction = list(filter(lambda d: d == cur_epsilon, self.actions))
        # else:
        leftAction = list(filter(lambda d: d <= round(cur_epsilon-(queryNum-observation)*0.05, 2), self.actions))
        action_list = [(key, value) for key, value in self.q_table[observation-1].items() if key[0] in leftAction and key[2][0] in leftQueryIdxList] #self.q_table[observation-1][self.q_table.columns.get_level_values(0).isin(leftAction)]
        rateList = []
        if np.random.uniform() < self.epsilon:  # 如果在epsilon几率内
            opt = np.random.choice(min(action_list, key=lambda d: d[1])[0])
            action, queryIdx, rateList = opt[0], opt[2][0], opt[2][1:]  # 选出当前observation中Q值最大的方向
        else:
            action = np.random.choice(leftAction)  # 如果不在epsilon内，则随机选择一个动作
            queryIdx = np.random.choice(leftQueryIdxList)
            curQuery = self.queryList[queryIdx]
            queryAttrNum = len(curQuery)
            for i in range(queryAttrNum):
                if self.attrTypeMap[curQuery[i]] == '#':
                    idx = np.random.choice(range(len(self.granularityMap[curQuery[i]])))
                    rateList.append(self.granularityMap[curQuery[i]][idx])
                else:
                    rateList.append(self.granularityMap[curQuery[i]][0])
        return action, rateList, queryIdx  # 返回应当做的action

    def getGranularityMap(self):
        return self.granularityMap

    def learn(self, observation_now, action, score, observation_after, cur_epsilon, rateList, queryIdx, leftQueryIdxList):
        queryNum = self.qn
        learnColumns = []
        attrTypeMap = self.attrTypeMap
        AttrRange = self.AttrRange

        if observation_now != queryNum:
            for e in np.arange(1, round(cur_epsilon * 20) + 1, 1):
                e = round(e / 20, 2)
                for idx in leftQueryIdxList:
                    for rl in pd.MultiIndex.from_product([self.granularityMap[attr] for attr in
                                                      self.queryList[idx]]):
                        learnColumns.append((round(e, 2), round(cur_epsilon - e, 2), tuple([idx, *rl])))

            q_predict = self.q_table[observation_now][(action, cur_epsilon, tuple([queryIdx, *rateList]))]  # 获得当前状态下，当前所作动作所对应的预测得分
            learnColumns = pd.MultiIndex.from_tuples(learnColumns)
            nextStateList = self.q_table[observation_after][learnColumns]
            posNextStateList = nextStateList[nextStateList != 0]
            if len(posNextStateList) == 0:
                q_target = score
            else:
                q_target = score + self.gamma * posNextStateList.min()  # 如果未完成则取下一个环境若干个动作中的最大得分作为这个环境的价值传递给当前环境
            # 根据所处的当前环境对各个动作的预测得分和下一步的环境的实际情况更新当前环境的q表
            self.q_table[observation_now][(action, cur_epsilon, tuple([queryIdx, *rateList]))] += self.lr * (q_target - q_predict)
        else:
            p = self.EP / 100
            N = self.N
            self.q_table[observation_now][(action, cur_epsilon, tuple([queryIdx, *rateList]))] = score + N/10 * (1+p)/2 * abs(p - (1-cur_epsilon/self.total_epsilon))
            # if self.EP < 50:
            #     self.q_table[observation_now][(action, cur_epsilon, tuple([queryIdx, *rateList]))] = score - 150 * (1-self.EP/100) * cur_epsilon  # 设置剩余预算奖励
            # else:
            #     self.q_table[observation_now][(action, cur_epsilon, tuple([queryIdx, *rateList]))] = score - 60 * (
            #                 1 - self.EP / 100) * cur_epsilon  # 设置剩余预算奖励

