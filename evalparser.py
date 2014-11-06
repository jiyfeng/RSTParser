## evalparser.py
## Author: Yangfeng Ji
## Date: 11-05-2014
## Time-stamp: <yangfeng 11/05/2014 20:04:34>

from model import ParsingModel
from tree import RSTTree
from evaluation import Metrics

def parse(pm, fedus):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type fedus: string
    :param fedus: file name of an document (with segmented EDUs) 
    """
    with open(fedus) as fin:
        edus = fin.read().split('\n')
        if len(edus[-1]) == 0:
            edus.pop()
    pred_rst = pm.sr_parse(edus)
    return pred_rst


def writebrackets(fname, brackets):
    """ Write the bracketing results into file
    """
    print 'Writing parsing results into file {}'.format(fname)
    with open(fname, 'w') as fout:
        for item in brackets:
            fout.write(str(item) + '\n')


def evalparser(path='./examples'):
    """ Test the parsing performance
    """
    from os import listdir
    from os.path import join as joinpath
    # ----------------------------------------
    # Load the parsing model
    pm = ParsingModel()
    pm.loadmodel("parsing-model.pickle.gz")
    # ----------------------------------------
    # Evaluation
    met = Metrics(levels=['span','nuclearity','relation'])
    # ----------------------------------------
    # Read all files from the given path
    doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.edus')]
    for fedus in doclist:
        fdis = fedus.replace('edus', 'dis')
        gold_rst = RSTTree(fname=fdis)
        gold_rst.build()
        # Get brackets from gold tree
        gold_brackets = gold_rst.bracketing()
        # ----------------------------------------
        # Parsing
        pred_rst = parse(pm, fedus=fedus)
        # Get brackets from parsing results
        pred_brackets = pred_rst.bracketing()
        fbrackets = fedus.replace('edus', 'brackets')
        writebrackets(fbrackets, pred_brackets)
        # print gold_brackets
        # print pred_brackets
        # Call the evaluation function
        met.eval(gold_rst, pred_rst)
        # Print out the evaluation on different levels
    met.report()
