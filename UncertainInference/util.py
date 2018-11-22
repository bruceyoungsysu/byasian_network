import math


def models_gen(chars):
    # generate symbols and all models from chars
    chars_index = {}
    models = []
    char_len = len(chars)
    for i in range(pow(2, char_len)):
        models.append(i)
    for i in range(char_len):
        chars_index[chars[i]] = pow(2, char_len - i - 1)
    return list(reversed(models)), chars_index


def model_set(chars_index, assignment):
    model = [0]
    for key in chars_index.keys():
        val = chars_index[key]
        position = int(math.log(val, 2))
        if key in assignment.keys():
            # if not model:
            #     model.append(0)
            assigned_val = assignment[key]
            model = list(map(lambda x:set_bit(x, position, assigned_val), model))
        else:
            model_true = list(map(lambda x: set_bit(x, position, 1), model))
            model_false = list(map(lambda x: set_bit(x, position, 0), model))
            model = model_true + model_false
    return model


def set_bit(bin, pos, val):
    bin ^= (bin & (1 << pos)) ^ (val << pos)
    return bin


def swap_bit(v, x, y):
    ret = v & (~(1 << x)) & (~(1 << y))
    ret = ret | (((v >> y) & 1) << x) | (((v >> x) & 1) << y)
    return ret


def normalization(answer):
    return list(map(lambda x: x/sum(answer), answer))


if __name__ == '__main__':
    #print(swap_bit(4,1,0))
    print(normalization([1,2,3]))