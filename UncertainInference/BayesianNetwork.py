from util import *
from copy import deepcopy,copy


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.visited = False
        self.models = {}
        self.index = {}
        self.models_f = {}
        self.index_f = {}

    def query(self, evidence):
        answer = [0, 0]
        models = model_set(self.index, evidence)
        for k in models:
            answer = list(map(lambda x, y: x+y, answer, self.models[k]))
        return answer

    def query_with_val(self, value, evidence):
        answer = [0, 0]
        models = model_set(self.index, evidence)
        for k in models:
            answer = list(map(lambda x, y: x + y, answer, self.models[k]))
        return answer[abs(1-value)]

    def markov_query(self, val, sample):
        prob = 1
        cur_evidence = {}
        for parent in self.parents:
            cur_evidence[parent.name] = sample[parent.name]
        prob *= self.query_with_val(val, cur_evidence)
        # the probability of all children
        for child in self.children:
            child_evidence = {}
            for p in child.parents:
                child_evidence[p.name] = sample[p.name]
            child_evidence[self.name] = val
            prob *= child.query_with_val(sample[child.name], child_evidence)
        return prob


class BayesianNetwork:
    def __init__(self):
        self.nodes = []
        self.root = None
        self.index = {}

    def put(self, node):
        self.nodes.append(node)
        if node.name not in self.index.keys():
            self.index[node.name] = node
        else:
            raise NameError('Please try another name for the node !')

    def topological_sort(self):  # by bfs

        def explore(node, queue, result):
            node.visited = True
            queue.remove(node)
            result.append(node)
            queue += node.children
            if not queue:
                return result
            for q in queue:
                if not q.visited:
                    explore(q, queue, result)

        queue = []
        result = []
        return explore(self.root, queue, result)

    def enumeration(self, query, evidence):
        def enumerate_all(nodes, evi):
            if not nodes: return 1
            new_nodes = copy(nodes)
            n = new_nodes.pop(0)
            n_name = n.name
            res = n.query(evi)
            if n_name in evi.keys():
                y = res[0] if evi[n_name] == 1 else res[1]
                return y * enumerate_all(new_nodes, evi)
            else:
                new_evi1 = deepcopy(evi)
                new_evi2 = deepcopy(evi)
                new_evi1[n_name] = 1
                new_evi2[n_name] = 0
                r1 = res[0] * enumerate_all(new_nodes, new_evi1)
                r2 = res[1] * enumerate_all(new_nodes, new_evi2)
                return r1+r2

        answers = []
        for q in query:
            answer = []
            evidence1 = deepcopy(evidence)
            evidence1[q] = 1  # extend evidence
            answer.append(enumerate_all(self.nodes, evidence1))
            evidence2 = deepcopy(evidence)
            evidence2[q] = 0  # extend evidence
            answer.append(enumerate_all(self.nodes, evidence2))
            answers += list(map(lambda x: x/sum(answer), answer))
        return answers
