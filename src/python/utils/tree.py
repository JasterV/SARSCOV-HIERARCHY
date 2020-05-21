from graphviz import Graph


class HierarchyTree:
    def __init__(self, table, labels=None):
        self.__dot = Graph("Hierarchy Sars-Cov-2",
                           node_attr={'shape': 'plaintext'})
        self.__table = table
        self.__labels = labels

    def build_tree(self):
        hierarchy_table = self.__table
        while len(hierarchy_table) > 1:
            closest_pair = self.find_closest_pair(hierarchy_table)
            self._add_relation(closest_pair)
            new_relation = self.build_relation(closest_pair, hierarchy_table)
            hierarchy_table = self.refactor_table(
                closest_pair, new_relation, hierarchy_table)

    def show(self):
        self.__dot.render("hierarchy")

    def _add_relation(self, pair):
        node1, node2 = tuple(map(self.__transform, pair))
        new_node = f"{node1},{node2}"
        self.__dot.edge(new_node, node1)
        self.__dot.edge(new_node, node2)

    def __transform(self, value):
        value = str(value).translate(
            str.maketrans({'(': '', ')': '', "'": ''}))
        if self.__labels is None:
            return value
        return ','.join(map(lambda x: self.__labels[x.strip()], value.split(',')))

    @staticmethod
    def find_closest_pair(table):
        closest_pairs = list()
        for key, value in table.items():
            closest_id, distance = min(value.items(), key=lambda x: x[-1])
            closest_pairs.append((key, closest_id, distance))
        sample1, sample2, _ = min(closest_pairs, key=lambda x: x[-1])
        return sample1, sample2

    @staticmethod
    def build_relation(pair, table):
        relation = dict()
        for elem in pair:
            for key, value in table[elem].items():
                if key not in pair:
                    relation.setdefault(key, []).append(value)
        relation = {key: min(relation[key]) for key in relation}
        return relation

    @staticmethod
    def refactor_table(pair, relation, table):
        new_table = dict()
        new_table[pair] = relation
        for id1, value in table.items():
            if id1 not in pair:
                new_table[id1] = {id2: distance for id2, distance in value.items()
                                  if id2 not in pair}
                new_table[id1][pair] = relation[id1]
        return new_table
