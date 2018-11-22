import copy
import math
from util import *
from BayesianNetwork import Node


class Factor:
    def __init__(self):
        self.index = {}
        self.models = {}


def factorize(node, var, val):
    fac = Factor
    if var == node.name:
        fac.models = node.models
        fac.index_ = node.index
    elif var in node.parents:
        fac.index, fac.models = flat(node)
        pos_var = int(math.log(fac.index[var], 2))
        fac.index, fac.models = swap(fac, 0, pos_var)
        fac.index.pop(0)
        new_models = {}
        for m in fac.models.keys():
            if m & 1 == val: new_models[m >> 1] = fac.models[m]
    return fac


def flat(node):
    index_f = copy(node.index)
    models_f = {}
    for k in node.index.keys():
        index_f[k] *= 2
    index_f[node.name] = 1
    for m in node.models.keys():
        models_f[m << 1 | 1] = node.models[m][0]
        models_f[m << 1] = node.models[m][1]
    return index_f, models_f


def defactorize(fac, val, pos):
    new_fac = Factor
    for i in fac.index.keys():
        if fac.index[i] >= pos:
            fac.index[i] <<= 1
    fac.index[pos] = val
    for model in fac.models.keys:
        new_model = model << 1
        for i in range(pos):
            set_bit(new_model, i, model >> i)
            new_fac[set_bit(new_model, pos, 1)] = new_fac[set_bit(new_model, pos, 0)] = fac[model]
    return new_fac


def swap(fac, pos1, pos2):
    # swap the position in index
    temp = fac.index[pos1]
    fac.index[pos1] = fac.index[pos2]
    fac.index[pos2] = temp
    # swap the position in models
    new_models = {}
    for k in fac.models.keys():
        bin = swap_bit(k, pos1, pos2)
        new_models[bin] = fac.models[k]
    return fac.index, new_models


def sync_fac(fac1, fac2):
    # sync between two factors
    diff1 = set(fac1.index.keys()) - set(fac2.index.keys())
    for var in diff1:
        defactorize(fac2, var, fac1.index(var))
    diff2 = set(fac2.index.keys()) - set(fac1.index.keys())
    for var in diff2:
        defactorize(fac1, var, fac2.index(var))
    # then swap the necessary index


def fac_product(fac1, fac2):
    res = copy(fac1)
    for var in fac2.index_f.keys():
        if var in fac1.index_f.keys():
            for model in fac1.models_f.keys():
                var_res = model & fac1.index_f[var]


def elimination(bn, query, evidence):
    # query is a list, evidence is a dict
    hidden = [x for x in bn.nodes if x not in query]
    # order hidden some way
    for node in bn.nodes:
        for evi in evidence.keys():
            node.factorize(evi, evidence[evi])
    for hvar in hidden:
        for node in bn.nodes:
            pass
