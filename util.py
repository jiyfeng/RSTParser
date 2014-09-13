## util.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/13/2014 18:21:35>

from scipy.sparse import lil_matrix

def label2action(label):
    pass


def action2label(action):
    pass


def vectorize(features, vocab):
    vec = lil_matrix((1, len(vocab)))
    for feat in features:
        try:
            fidx = vocab[feat]
            vec[0,fidx] += 1.0
        except KeyError:
            pass
    return vec
