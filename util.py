## util.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/16/2014 13:09:09>

from scipy.sparse import lil_matrix

def label2action(label):
    """ Transform label to action
    """
    items = label.split('-')
    if len(items) == 1:
        action = (items[0], None, None)
    elif len(items) == 3:
        action = tuple(items)
    else:
        raise ValueError("Unrecognized label: {}".format(label))
    return action


def action2label(action):
    """ Transform action into label
    """
    if action[0] == 'Shift':
        label = action[0]
    elif action[0] == 'Reduce':
        label = '-'.join(list(action))
    else:
        raise ValueError("Unrecognized parsing action: {}".format(action))
    return label


def vectorize(features, vocab):
    """ Transform a feature list into a numeric vector
        with a given vocab
    """
    vec = lil_matrix((1, len(vocab)))
    for feat in features:
        try:
            fidx = vocab[feat]
            vec[0,fidx] += 1.0
        except KeyError:
            pass
    return vec


def extractrelation(s, level=0):
    """ Extract discourse relation on different level
    """
    return s.lower().split('-')[0]


def reversedict(dct):
    """ Reverse the {key:val} in dct to
        {val:key}
    """
    # print labelmap
    newmap = {}
    for (key, val) in dct.iteritems():
        newmap[val] = key
    return newmap
