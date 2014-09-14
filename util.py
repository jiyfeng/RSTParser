## util.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/13/2014 23:02:58>

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
        raise ValueError("Unrecognized label")
    return action


def action2label(action):
    """ Transform action into label
    """
    if action[0] == 'shift':
        label = action[0]
    elif action[0] == 'reduce':
        label = '-'.join(list(action))
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
