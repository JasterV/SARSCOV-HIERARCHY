from ete3 import Tree, TreeStyle
from os import environ

environ['QT_QPA_PLATFORM']='offscreen'

class HierarchyTree:
    def __init__(self, table, labels=None):
        self.__table = table
        self.__labels = labels

    def build_tree(self):
        hierarchy_table = self.__table
        closest_pair = tuple()
        while len(hierarchy_table) > 1:
            closest_pair = self.find_closest_pair(hierarchy_table)
            new_relation = self.build_relation(closest_pair, hierarchy_table)
            hierarchy_table = self.refactor_table(
                closest_pair, new_relation, hierarchy_table)
        self._show_tree(str(closest_pair))

    def _show_tree(self, tuple_repr):
        for key in self.__labels:
            tuple_repr = tuple_repr.replace(key, self.__labels[key])
        t = Tree(tuple_repr + ";")
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.mode = "c"
        ts.arc_start = -180  # 0 degrees = 3 o'clock
        ts.arc_span = 180
        print(t)

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
