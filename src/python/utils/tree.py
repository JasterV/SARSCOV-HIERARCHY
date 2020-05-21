from graphviz import Graph


class HierarchyTree:
    def __init__(self, labels=None):
        self.__dot = Graph("Hierarchy Sars-Cov-2",
                           node_attr={'shape': 'plaintext'})
        self.__labels = labels

    def add_relation(self, pair):
        node1, node2 = tuple(map(self.__transform, pair))
        new_node = f"{node1},{node2}"
        self.__dot.edge(new_node, node1)
        self.__dot.edge(new_node, node2)

    def show(self):
        self.__dot.render("hierarchy")

    def __transform(self, value):
        value = str(value).translate(
            str.maketrans({'(': '', ')': '', "'": ''}))
        if self.__labels == None:
            return value
        return ','.join(map(lambda x: self.__labels[x.strip()], value.split(',')))
