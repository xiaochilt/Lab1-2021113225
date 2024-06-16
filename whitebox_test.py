import pytest
from collections import defaultdict
import random
# 导入你的randomWalk函数
from lab1_gui import randomWalk


# 测试随机游走算法对正常路径的行为
def test_random_walk_normal_path():
    graph = {
        'A': {'B': 1},
        'B': {'C': 1},
        'C': {}
    }
    visited_nodes = randomWalk(graph)
    # 检查是否从A, B或C开始
    assert visited_nodes[0] in ['A', 'B', 'C']
    # 检查后续节点
    assert visited_nodes[1:] in [['B', 'C'], ['C'], []]


# 测试随机游走算法对存在重复边的情况的行为
def test_random_walk_repeated_edge():
    graph = {
        'A': {'B': 1},
        'B': {'A': 1, 'C': 1},
        'C': {}
    }
    visited_nodes = randomWalk(graph)
    # 检查是否从A, B或C开始
    assert visited_nodes[0] in ['A', 'B', 'C']
    # 检查后续节点
    assert visited_nodes[1:] in [['B', 'A'], ['B', 'C'], ['C'], []]


class ResultTextWalk:
    def __init__(self):
        self.text = ""

    def set(self, text):
        self.text = text


def random_walk(oriented_graph, result_text_walk):
    if oriented_graph:
        walk = randomWalk(oriented_graph)
        result_text_walk.set("随机游走路径：" + " -> ".join(walk))
    else:
        result_text_walk.set("文本为空，无法游走！")


# 测试当有向图为空时随机游走算法的行为
def test_random_walk_empty_graph():
    graph = {}
    result_text_walk = ResultTextWalk()
    random_walk(graph, result_text_walk)
    assert result_text_walk.text == "文本为空，无法游走！"


# 测试当只有一个节点且无边时随机游走算法的行为
def test_random_walk_single_node_no_edges():
    graph = {'A': {}}
    visited_nodes = randomWalk(graph)
    assert visited_nodes == ['A']


# 测试当只有一个节点且有边时随机游走算法的行为
def test_random_walk_single_node_with_edges():
    graph = {'A': {'B': 1}, 'B': {}}
    visited_nodes = randomWalk(graph)
    # 检查是否从A或B开始
    assert visited_nodes[0] in ['A', 'B']
    # 检查后续节点
    assert visited_nodes[1:] in [['B'], []]


# 测试当只有两个节点且有一条边时随机游走算法的行为
def test_random_walk_two_nodes_one_edge():
    graph = {'A': {'B': 1}, 'B': {}}
    visited_nodes = randomWalk(graph)
    assert visited_nodes == ['A', 'B']


# 测试当只有两个节点且有两条边构成环时随机游走算法的行为
def test_random_walk_two_nodes_with_cycle():
    graph = {'A': {'B': 1}, 'B': {'A': 1}}
    visited_nodes = randomWalk(graph)
    assert 'A' in visited_nodes
    assert 'B' in visited_nodes


# 使用pytest运行测试
pytest.main()
