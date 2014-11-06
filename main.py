## main.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 11/06/2014 10:06:38>

from data import Data
from model import ParsingModel
from tree import RSTTree
from evaluation import Metrics
from cPickle import load
from util import reversedict
from evalparser import evalparser
import gzip

def createdata(path):
    """ Create training data by calling the Data class

    :type path: string
    :param path: path to the training document folder
    """
    data = Data()
    data.builddata(path)
    # Change the threshold if you want to filter
    #   out the low-frequency features
    data.buildvocab(thresh=1)
    data.buildmatrix()
    data.savematrix("training-data.pickle.gz")
    data.savevocab("vocab.pickle.gz")


def trainmodel():
    """ Training a model with data and save it into file
    """
    fvocab = "vocab.pickle.gz"
    fdata = "training-data.pickle.gz"
    D = load(gzip.open(fvocab))
    vocab, labelidxmap = D['vocab'], D['labelidxmap']
    D = load(gzip.open(fdata))
    trnM, trnL  = D['matrix'], D['labels']
    idxlabelmap = reversedict(labelidxmap)
    pm = ParsingModel(vocab=vocab, idxlabelmap=idxlabelmap)
    pm.train(trnM, trnL)
    pm.savemodel("parsing-model.pickle.gz")


if __name__ == '__main__':
    # Create data for offline training
    print 'Create data ...'
    createdata(path="./examples")
    # Train a parsing model
    print 'Training a parsing model ...'
    trainmodel()
    # Evaluate on dev/test documents
    print 'Evaluating the parsing performance ...'
    evalparser(path='./examples', report=True)
    

    
