from graphviz import Digraph


class HierarchyTree:
    def __init__(self):
        self.__dot = Digraph("Hierarchy Sars-Cov-2")

    def add_relation(self, pair):
        node1, node2 = tuple(map(lambda x: str(x).translate(
            str.maketrans({'(': '', ')': '', "'": ''})), pair))
        new_node = f"{node1}, {node2}"
        self.__dot.edge(node1, new_node)
        self.__dot.edge(node2, new_node)

    def show(self):
        self.__dot.render("hierarchy.gv")
