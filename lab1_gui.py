import random
import re
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import tkinter as tk
from tkinter import filedialog

global oriented_graph  # 声明全局变量


def preprocess_text(text):
    # 将文本中的标点符号和非字母字符替换为空格
    cleaned_text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # 将所有字符转换为小写
    cleaned_text = cleaned_text.lower()
    # 将换行符和回车符替换为空格
    cleaned_text = re.sub(r'[\n\r]', ' ', cleaned_text)
    # 移除多余的空格
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text


def build_oriented_graph(text):
    # 将文本分割成单词列表
    words = text.split()
    # 创建一个字典来存储单词的相邻关系和权重
    graph = defaultdict(Counter)

    # 构建有向图
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        # 更新图的权重
        graph[current_word][next_word] += 1

    return graph



def showDirectedGraph(graph):
    G = nx.DiGraph()

    # 添加节点和边
    for word, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(word, neighbor, weight=weight)

    # 绘制有向图
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # 保存绘制的图形为文件
    plt.savefig("oriented_graph.png", format="PNG")
    plt.show()



def queryBridgeWords(graph, word1, word2):
    # 检查word1和word2是否存在于图中
    if word1 not in graph or word2 not in graph:
        # 如果任一词不在图中，返回特定的信息
        return None

    # 初始化桥接词集合
    bridge_words = set()

    # 检查word1的所有后继词
    for word3 in graph[word1]:
        # 如果word3也是word2的前驱词，则它是桥接词
        if word2 in graph[word3]:
            bridge_words.add(word3)

    # 如果找到了桥接词，返回桥接词集合
    return bridge_words


def generateNewText(graph, inputText):
    processed_text = preprocess_text(inputText)
    words = processed_text.split()
    new_text = []

    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        bridge_words = queryBridgeWords(graph, current_word, next_word)

        # 检查find_bridge_words的返回值
        if bridge_words is None:
            # 如果word1或word2不在图中，不插入桥接词，直接添加当前词
            new_text.append(current_word)
        elif not bridge_words:
            # 如果没有桥接词，只添加当前词
            new_text.append(current_word)
        else:
            # 如果存在桥接词
            bridge_word = random.choice(list(bridge_words))  # 确保bridge_words是列表形式
            new_text.extend([current_word, bridge_word])

    new_text.append(words[-1])  # 添加最后一个词

    return ' '.join(new_text)


def calcShortestPath(graph, word1, word2):
    # dijkstra算法找到最短距离
    dist_list = {}
    pre_nodes = {}
    visited_nodes = []
    min_dist = None
    min_dist_node = None
    nodes_list = list(graph.keys())
    if word1 not in nodes_list or word2 not in nodes_list:
        return None
    for node in nodes_list:
        if node == word1:
            dist_list[node] = 0
        elif node in graph[word1].keys():
            dist_list[node] = 1
        else:
            dist_list[node] = 100
    for i in range(len(dist_list)):
        sort_dist = sorted(dist_list.items(), key=lambda item: item[1])
        for node, dist in sort_dist:
            if node not in visited_nodes:
                min_dist_node = node
                min_dist = dist
                visited_nodes.append(min_dist_node)
                break
        try:
            for node in graph[min_dist_node].keys():
                if dist_list[node] >= min_dist + 1:
                    dist_list[node] = min_dist + 1
                    pre_nodes[node] = min_dist_node
        except:
            pass
    # 生成最短路径
    shortest_path = []
    try:
        shortest_path.insert(0, word2)
        pre_node = pre_nodes[word2]
        while True:
            shortest_path.insert(0, pre_node)
            if pre_node == word1:
                break
            pre_node = pre_nodes[pre_node]
    except:
        pass

    # 画图
    G = nx.DiGraph()
    # 添加节点和边
    for word, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(word, neighbor, weight=weight)
    # 绘制有向图
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='lightgray')
    nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='blue')
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v in zip(shortest_path, shortest_path[1:])],
                           edge_color='red', width=2)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels={(u, v): labels[u, v] for u, v in zip(shortest_path, shortest_path[1:])})
    plt.show()

    return shortest_path


def randomWalk(graph):
    visited_nodes = []
    visited_edges = []
    current_node = random.choice(list(graph.keys()))
    while True:
        visited_nodes.append(current_node)
        if current_node not in graph or not graph[current_node]:
            # 如果当前节点没有出边，结束游走
            return visited_nodes
        next_node = random.choice(list(graph[current_node].keys()))
        for edge in visited_edges:
            # 如果出现重复边，结束游走
            if [current_node, next_node] == edge:
                return visited_nodes
        visited_edges.append([current_node, next_node])
        current_node = next_node


def save_walk_to_file(walk, filename="random_walk.txt"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("\n".join(walk))

def open_file_dialog():
    global oriented_graph  # 声明全局变量
    file_path = filedialog.askopenfilename(
        title="选择文本文件",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        processed_text = preprocess_text(text)
        print(processed_text)

        # 构建有向图
        oriented_graph = build_oriented_graph(processed_text)

        # 绘制有向图并保存为文件
        showDirectedGraph(oriented_graph)

def query_bridge_words(oriented_graph, entry_word1, entry_word2, result_text):
    word1 = entry_word1.get().lower()
    word2 = entry_word2.get().lower()
    if word1 and word2:
        bridge_words = queryBridgeWords(oriented_graph, word1, word2)
        if bridge_words is None:
            result_text.set(f"No {word1} or {word2} in the graph!")
        elif not bridge_words:
            result_text.set(f"No bridge words from {word1} to {word2}!")
        else:
            bridge_words_str = ", ".join(bridge_words)
            result_text.set(f"The bridge words from {word1} to {word2} are: {bridge_words_str}")
    else:
        result_text.set("请输入单词！")


def generate_new_text(oriented_graph, entry_new_text, result_text):
    new_text = entry_new_text.get()
    if new_text:
        result = generateNewText(oriented_graph, new_text)
        result_text.set(result)
    else:
        result_text.set("请输入内容！")


def calc_shortest_path(oriented_graph, entry_word1_shortest, entry_word2_shortest, result_text_shortest):
    word1 = entry_word1_shortest.get().lower()
    word2 = entry_word2_shortest.get().lower()
    if word1 and word2:
        shortest_path = calcShortestPath(oriented_graph, word1, word2)
        if shortest_path:
            result_text_shortest.set(f"最短路径为: {' '.join(shortest_path)}, 长度为: {len(shortest_path)}")
        elif shortest_path is None:
            result_text_shortest.set(f"错误：单词 '{word1}' 和 '{word2}' 不可达。")
        else:
            result_text_shortest.set(f"单词 '{word1}' 到 '{word2}' 之间没有路径。")
    else:
        result_text_shortest.set("请输入单词！")


def random_walk(oriented_graph, result_text_walk):
    if oriented_graph:
        walk = randomWalk(oriented_graph)
        result_text_walk.set("随机游走路径：" + " -> ".join(walk))
        save_walk_to_file(walk, "random_walk.txt")
    else:
        result_text_walk.set("文本为空，无法游走！")


def main():
    global oriented_graph  # 声明全局变量
    # 创建主窗口
    root = tk.Tk()
    root.title("文本处理")

    # 创建打开文件对话框的按钮
    load_file_button = tk.Button(root, text="选择文本文件", command=open_file_dialog)
    load_file_button.pack(pady=10)

    # 创建查询桥接词的部分
    frame_query = tk.Frame(root)
    frame_query.pack(padx=10, pady=10)

    label_word1 = tk.Label(frame_query, text="第一个单词:")
    label_word1.grid(row=0, column=0)

    entry_word1 = tk.Entry(frame_query)
    entry_word1.grid(row=0, column=1)

    label_word2 = tk.Label(frame_query, text="第二个单词:")
    label_word2.grid(row=0, column=2)

    entry_word2 = tk.Entry(frame_query)
    entry_word2.grid(row=0, column=3)

    button_query = tk.Button(frame_query, text="查询桥接词",
                             command=lambda: query_bridge_words(oriented_graph, entry_word1, entry_word2, result_word))
    button_query.grid(row=0, column=4)

    result_word = tk.StringVar()
    result_label = tk.Label(frame_query, textvariable=result_word)
    result_label.grid(row=1, columnspan=5)

    # 创建生成新文本的部分
    frame_generate = tk.Frame(root)
    frame_generate.pack(padx=10, pady=10)

    label_new_text = tk.Label(frame_generate, text="输入新文本:")
    label_new_text.grid(row=0, column=0)

    entry_new_text = tk.Entry(frame_generate, width=50)
    entry_new_text.grid(row=0, column=1)

    button_generate = tk.Button(frame_generate, text="生成新文本",
                                command=lambda: generate_new_text(oriented_graph, entry_new_text, result_text))
    button_generate.grid(row=0, column=2)

    result_text = tk.StringVar()
    result_label = tk.Label(frame_generate, textvariable=result_text)
    result_label.grid(row=1, columnspan=5)

    # 创建计算最短路径的部分
    frame_shortest = tk.Frame(root)
    frame_shortest.pack(padx=10, pady=10)

    label_word1_shortest = tk.Label(frame_shortest, text="第一个单词:")
    label_word1_shortest.grid(row=0, column=0)

    entry_word1_shortest = tk.Entry(frame_shortest)
    entry_word1_shortest.grid(row=0, column=1)

    label_word2_shortest = tk.Label(frame_shortest, text="第二个单词:")
    label_word2_shortest.grid(row=0, column=2)

    entry_word2_shortest = tk.Entry(frame_shortest)
    entry_word2_shortest.grid(row=0, column=3)

    button_shortest = tk.Button(frame_shortest, text="计算最短路径",
                                command=lambda: calc_shortest_path(oriented_graph, entry_word1_shortest,
                                                                   entry_word2_shortest, result_text_shortest))
    button_shortest.grid(row=0, column=4)

    result_text_shortest = tk.StringVar()
    result_label_shortest = tk.Label(frame_shortest, textvariable=result_text_shortest)
    result_label_shortest.grid(row=1, columnspan=5)

    # 创建随机游走的部分
    frame_walk = tk.Frame(root)
    frame_walk.pack(padx=10, pady=10)

    button_walk = tk.Button(frame_walk, text="随机游走", command=lambda: random_walk(oriented_graph, result_text_walk))
    button_walk.pack()

    result_text_walk = tk.StringVar()
    result_label_walk = tk.Label(frame_walk, textvariable=result_text_walk)
    result_label_walk.pack()

    # 运行主循环
    root.mainloop()



if __name__ == "__main__":
    main()
