## main.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/16/2014 13:27:53>

from data import Data
from model import ParsingModel
from tree import RSTTree
from cPickle import load
from util import reversedict
import gzip

def createdata():
    """ Create training data by calling the Data class
    """
    path = "./examples"
    data = Data()
    data.builddata(path)
    data.buildvocab(thresh=1)
    data.buildmatrix()
    data.savematrix("tmp-data.pickle.gz")
    data.savevocab("tmp-vocab.pickle.gz")


def trainmodel():
    """ Training a model with data and save it into file
    """
    fvocab = "tmp-vocab.pickle.gz"
    fdata = "tmp-data.pickle.gz"
    D = load(gzip.open(fvocab))
    vocab, labelidxmap = D['vocab'], D['labelidxmap']
    D = load(gzip.open(fdata))
    trnM, trnL  = D['matrix'], D['labels']
    idxlabelmap = reversedict(labelidxmap)
    pm = ParsingModel(vocab=vocab, idxlabelmap=idxlabelmap)
    pm.train(trnM, trnL)
    pm.savemodel("parsing-model.pickle.gz")

def parse():
    """ Test the parsing performance
    """
    pm = ParsingModel()
    pm.loadmodel("parsing-model.pickle.gz")
    fname = "examples/wsj_0600.out.dis"
    rst = RSTTree(fname)
    rst.build()
    texts = rst.getedutext()
    print texts
    T = pm.sr_parse(texts)
    print T.text

if __name__ == '__main__':
    # Create data for offline training
    createdata()
    # Train a parsing model
    trainmodel()
    # Perform parsing on a training document
    parse()
    

    
