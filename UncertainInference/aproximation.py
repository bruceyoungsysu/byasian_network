import random
from copy import copy
from util import *


def sampling(bn):
    sample = {}
    for node in bn.nodes:
        ran = random.uniform(0, 1)
        answer = normalization(node.query(sample))
        if ran <= answer[0]:
            sample[node.name] = 1
        else:
            sample[node.name] = 0
    return sample


def prior_sampling(bn, n):
    samples = []
    count = []
    for i in range(n):
        sam = sampling(bn)
        if sam in samples:
            count[samples.index(sam)] += 1
        else:
            samples.append(sam)
            count.append(1)
    return samples, count


def estimate(samples, count, variable):
    count_true, count_false = 0, 0
    for i in range(len(count)):
        sample = samples[i]
        if sample[variable]:
            count_true += count[i]
        else:
            count_false += count[i]
    return count_true, count_false


def rejection_sampleing(samples, count, evidence):
    new_samples = copy(samples)
    new_count = copy(count)
    for i in range(len(count)):
        sample = samples[i]
        for e in evidence.keys():
            if sample[e] != evidence[e]:
                new_samples.remove(sample)
                new_count.remove(count[i])
    return new_samples, new_count


def lik_weight(bn, evidence):
    w = 1
    sample = {}
    for node in bn.nodes:
        if node.name in evidence.keys():
            answer = node.query(sample)
            print(answer)
            w *= answer[0] if evidence[node.name] == 1 else answer[1]
            print(w)
            sample[node.name] = evidence[node.name]
        else:
            ran = random.uniform(0, 1)
            answer = normalization(node.query(sample))
            if ran <= answer[0]:
                sample[node.name] = 1
            else:
                sample[node.name] = 0
    return sample, w


def likweight_sampling(bn, evidence, n):
    samples = []
    count = []
    for i in range(n):
        sam, w = lik_weight(bn, evidence)
        if sam in samples:
            count[samples.index(sam)] += w
        else:
            samples.append(sam)
            count.append(w)
    return samples, count


def random_node(bn, evidence):
    base = []
    for node in bn.nodes:
        if node.name not in evidence.keys():
            base.append(node)
    return random.choice(base)


def get_mb(node):
    mbs = node.parents + node.children
    for child in node.children:
        mbs += child.parents
    mb_names = set(map(lambda x: x.name, mbs))
    mb_names.remove(node.name)
    return mb_names


def Gibbs(bn, evidence, n, query):
    init_samp = sampling(bn)
    for key in init_samp.keys():
        init_samp[key] = random.choice([0, 1]) if key not in evidence.keys() else evidence[key]
    init_samp = {'J': 1, 'M': 1, 'B': 1, 'A': 1, 'E': 1}
    sample = init_samp
    count_true, count_false = 0, 0
    for i in range(n):
        random_nd = random_node(bn, evidence)
        sample.pop(random_nd.name)
        # get markov blanket nodes
        mb_names = get_mb(random_nd)
        new_evidence = {}
        for name in mb_names:
            if name in sample.keys():
                new_evidence[name] = sample[name]
        print(random_nd.name)
        print(new_evidence)
        answer = normalization(random_nd.query(new_evidence))
        print(answer)
        ran = random.uniform(0, 1)
        if ran <= answer[0]:
            sample[random_nd.name] = 1
        else:
            sample[random_nd.name] = 0
        if sample[query] == 1:
            count_true += 1
        else:
            count_false += 1
    return count_true, count_false


def markov_query(node, sample):
    prob = 1
    nprob = 1
    cur_evidence = {}
    for parent in node.parents:
        cur_evidence[parent.name] = sample[parent.name]
    prob *= node.query(cur_evidence)[0]
    nprob *= node.query(cur_evidence)[1]
    # the probability of all children
    for child in node.children:
        print(child.name)
        child_evidence = {}
        for p in child.parents:
            child_evidence[p.name] = sample[p.name]
        child_evidence[node.name] = 1
        prob *= child.query_with_val(sample[child.name], child_evidence)
        child_evidence[node.name] = 0
        nprob *= child.query_with_val(sample[child.name], child_evidence)
    return prob, nprob



