try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from BayesianNetwork import Node, BayesianNetwork
import re
from util import *
from aproximation import *


def parse_vars(file):
    bn = BayesianNetwork()
    tree = ET.parse(file)
    root = tree.getroot()
    char_index = []
    for n in root.iter('VARIABLE'):
        name = n.find('NAME').text
        char_index.append(name)
        globals()['node_' + name] = Node(name)
        bn.put(globals()['node_' + name])
    return char_index, bn


def parse_def(file):
    tree = ET.parse(file)
    root = tree.getroot()
    for n in root.iter('DEFINITION'):
        fr = n.find('FOR').text
        given = n.findall('GIVEN')
        for g in given:
            try:
                globals()['node_' + g.text].children.append(globals()['node_' + fr])
                globals()['node_' + fr].parents.append(globals()['node_' + g.text])
            except KeyError:
                print('Variable not found !')

        a = re.split('\s', n.find('TABLE').text)
        while '' in a: a.remove('')
        parents_index = []
        for p in globals()['node_' + fr].parents:
            parents_index.append(p.name)
        models, chars_index = models_gen(parents_index)
        globals()['node_' + fr].index = chars_index
        for i in range(len(models)):
            globals()['node_' + fr].models[models[i]] = [float(a[2*i]), float(a[2*i+1])]


if __name__ == '__main__':
    file_path = '../examples/aima-alarm.xml'
    index, bn = parse_vars(file_path)
    parse_def(file_path)
    # print(node_A.index)
    # print(node_A.models)
    print(bn.enumeration(['A'], {'J':1, 'M':1, 'B':1, 'E':1}))
    #print(normalization(node_A.query({'J':1, 'M':1, 'B':1, 'E':1})))
    print(markov_query(node_A, {'J':1, 'M':1, 'B':1, 'E':1, 'A':1}))
    print(node_A.markov_query(0, {'J':1, 'M':1, 'B':1, 'E':1, 'A':1}))
    # samples, count = prior_sampling(bn, 100000)
    # estimate(samples, count, 'B')
    # samples_r, count_r = rejection_sampleing(samples, count, {'J':1, 'M':1})
    # print(estimate(samples_r, count_r, 'B'))
    # print(lik_weight(bn, {'J':1,'M':1}))
    # print(likweight_sampling(bn, {'J':1,'M':1}, 100000))

    # print(Gibbs(bn, {'J': 1, 'M': 1}, 10, 'A'))

