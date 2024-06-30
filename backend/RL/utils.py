import itertools
import random

import networkx as nx

def are_edges_same(graph1, graph2):
    return nx.is_isomorphic(graph1, graph2)
    # return sorted(graph1.edges()) == sorted(graph2.edges())

def is_valid_cover(graph, cover):
    if len(cover) == 0:
        return False
    else:
        return are_edges_same(graph, nx.compose_all(cover))

def edges_are_contained(subgraph, current_cover):
    if len(current_cover) == 0:
        return False
    for graph in current_cover:
        subgraphEdgeNum = len(subgraph.edges())
        cover_graphNum = len(graph.edges())
        if subgraphEdgeNum > cover_graphNum:
            LG = subgraph
            SG = graph
        else:
            SG = subgraph
            LG = graph
        # for edge in SG.edges():
        #     if edge not in LG.edges():
        #         break
        # else:
        #     return True
        for edge in SG.edges():
            if edge in LG.edges():
                return True
    return False


def backtrack(graph, subgraphs, current_cover, valid_covers):
    if is_valid_cover(graph, current_cover):
        valid_covers.append(list(current_cover))

    if not subgraphs:
        return

    # 从剩余的子图中选择一个子图进行尝试
    for i, subgraph in enumerate(subgraphs):
        if(len(subgraph.edges()) == 2) and len(current_cover) == 1:
            print('xxx')
        if edges_are_contained(subgraph, current_cover):
            continue
        current_cover.append(subgraph)
        backtrack(graph, subgraphs[i + 1:], current_cover, valid_covers)
        current_cover.pop()



def find_covering_subgraph_combinations(graph, subgraphs):
    valid_covers = []
    backtrack(graph, subgraphs, [], valid_covers)
    ret = []
    for cover in valid_covers:
        temp = []
        for graph in cover:
            edges = list(graph.edges())
            if len(edges) > 1:
                temp.append(list(graph.nodes()))
            else:
                temp.extend(edges)
        ret.append(temp)
    return ret


def shuffle_list(lst):
    n = len(lst)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    return lst

def get_subgraphs(graph):
    nodes = list(graph.nodes)
    all_subgraphs = []

    # Generate all possible combinations of nodes
    for r in range(1, len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            subgraph = graph.subgraph(subset)
            if nx.is_connected(subgraph):
                all_subgraphs.append(subgraph)
    return all_subgraphs


def keep_largest_contained_graph(graphs):
    largest_contained_graphs = []
    for G in graphs:
        is_contained = False
        for H in graphs:
            if G != H and set(G.nodes()).issubset(set(H.nodes())) and set(G.edges()).issubset(set(H.edges())):
                is_contained = True
                break
        if not is_contained:
            largest_contained_graphs.append(G)
    return largest_contained_graphs


def find_closest_complete_subgraph(graph):
    max_edges = 0
    max_subgraphs = []

    # 遍历图中所有的子图
    for subgraph in get_subgraphs(graph):
        num_edges = subgraph.number_of_edges()
        num_nodes = subgraph.number_of_nodes()
        # 计算完全图的边数
        complete_graph_edges = num_nodes * (num_nodes - 1) // 2

        # 判断子图是否接近完全图
        if num_nodes >= 2 and num_edges > complete_graph_edges / 2:
            max_subgraphs.append(subgraph)
    return max_subgraphs # keep_largest_contained_graph(max_subgraphs)


def getDivisionList(n):
    def backtrack(start, path, target):
        # 如果目标和为0，说明当前路径满足条件，将其添加到结果集中
        if target == 0:
            result.append(tuple(path[:]))  # 添加path的副本，以避免后续修改影响结果
            return
            # 如果目标和已经小于0，说明当前路径不可能满足条件，直接返回
        if target < 0:
            return
            # 尝试所有可能的正整数作为下一个元素
        for i in range(1, n + 1):
            # 将当前元素添加到路径中
            path.append(i)
            # 递归调用，目标和减去当前元素，下一个可能的元素至少为i（保证数组元素不重复）
            backtrack(i, path, target - i)
            # 回溯，移除当前元素，尝试其他可能性
            path.pop()

    result = []  # 存储结果集
    backtrack(1, [], n)  # 从1开始尝试，初始路径为空，目标和为n
    return result



