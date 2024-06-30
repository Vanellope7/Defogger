import networkx as nx

def are_edges_same(graph1, graph2):
    return sorted(graph1.edges()) == sorted(graph2.edges())

def is_valid_cover(graph, cover):
    if len(cover) == 0:
        return False
    else:
        return are_edges_same(graph, nx.compose_all(cover))

def edges_are_contained(subgraph, current_cover):
    cover_graph = nx.compose_all(cover)
    for edge in subgraph.edges():
        if edge not in cover_graph.edges():
            return False
    return True


def backtrack(graph, subgraphs, current_cover, valid_covers):
    if is_valid_cover(graph, current_cover):
        valid_covers.append(list(current_cover))

    if not subgraphs:
        return

    # 从剩余的子图中选择一个子图进行尝试
    for i, subgraph in enumerate(subgraphs):
        if edges_are_contained(subgraph, current_cover):
            continue
        current_cover.append(subgraph)
        backtrack(graph, subgraphs[i + 1:], current_cover, valid_covers)
        current_cover.pop()


def find_covering_subgraph_combinations(graph, subgraphs):
    valid_covers = []
    backtrack(graph, subgraphs, [], valid_covers)
    return valid_covers


# 示例用法
if __name__ == "__main__":
    # 原图
    original_graph = nx.Graph()
    original_graph.add_edges_from([(1, 2), (1, 3), (2, 4)])

    # 子图列表
    subgraph_list = []
    subgraph_list.append(nx.Graph([(1, 2), (1, 3)]))
    subgraph_list.append(nx.Graph([(1, 2), (2, 4)]))
    subgraph_list.append(nx.Graph([(1, 2)]))
    subgraph_list.append(nx.Graph([(2, 4)]))
    subgraph_list.append(nx.Graph([(1, 3)]))

    # 寻找覆盖子图组合
    covering_subgraph_combinations = find_covering_subgraph_combinations(original_graph, subgraph_list)
    print("Covering subgraph combinations:")
    for cover in covering_subgraph_combinations:
        for graph in cover:
            print(graph.edges())
        print('-----')
