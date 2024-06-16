import pytest
import networkx as nx
from lab1 import build_oriented_graph, queryBridgeWords  # 确保从正确的模块导入函数


def test_words_not_in_graph():
    # 等价类：两个词都不在图中
    graph = {
        'this': {'is'},
        'is': {'a'},
        'a': {'test'},
        'test': {'text'},
        'text': {'for'},
        'for': {'the'},
        'the': {'graph'}}
    # 期望返回 None
    assert queryBridgeWords(graph, 'not', 'exist') is None


def test_one_word_not_in_graph():
    # 等价类：一个词在图中，另一个词不在图中
    graph = {
        'this': {'is'},
        'is': {'a'},
        'a': {'test'},
        'test': {'text'},
        'text': {'for'},
        'for': {'the'},
        'the': {'graph'}}
    # 期望返回 None
    assert queryBridgeWords(graph, 'this', 'not') is None


def test_no_bridge_words():
    # 等价类：两个词在图中，但没有桥接词
    graph = {
        'this': {'is'},
        'is': {'a'},
        'a': {'test'},
        'test': {'text'},
        'text': {'for'},
        'for': {'the'},
        'the': {'graph'}}
    # 期望返回一个空集
    assert queryBridgeWords(graph, 'is', 'for') == set()


def test_one_bridge_word():
    # 等价类：有一个桥接词
    graph = {
        'this': {'is'},
        'is': {'a'},
        'a': {'test'},
        'test': {'text'},
        'text': {'for'},
        'for': {'the'},
        'the': {'graph'},
        'bridge': {'text'}}
    # 期望返回包含桥接词的集合
    assert queryBridgeWords(graph, 'test', 'for') == {'text'}


def test_multiple_bridge_words():
    # 等价类：有多个桥接词
    # 创建一个图，其中'a'和'b'都是'start'和'end'之间的桥接词
    graph = {
        'start': {
            'a', 'b'}, 'a': {
            'middle', 'end'}, 'b': {
                'middle', 'end'}, 'middle': {}, 'end': {}}
    # 期望返回包含所有桥接词的集合
    assert queryBridgeWords(graph, 'start', 'end') == {'a', 'b'}


def test_both_words_in_graph_no_bridge():
    # 边界值测试：两个词都在图中，但不存在桥接词
    graph = {'word1': {}, 'word2': {}}
    assert queryBridgeWords(graph, 'word1', 'word2') == set()


def test_both_words_in_graph_one_bridge():
    # 边界值测试：两个词都在图中，且存在一个桥接词
    graph = {'word1': {'bridge'}, 'bridge': {'word2'}, 'word2': {}}
    assert queryBridgeWords(graph, 'word1', 'word2') == {'bridge'}


def test_both_words_in_graph_multiple_bridges():
    # 边界值测试：两个词都在图中，且存在多个桥接词
    graph = {
        'word1': {
            'bridge1',
            'bridge2'},
        'bridge1': {'word2'},
        'bridge2': {'word2'},
        'word2': {}}
    assert queryBridgeWords(graph, 'word1', 'word2') == {'bridge1', 'bridge2'}
