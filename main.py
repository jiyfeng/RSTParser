## main.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/22/2014 17:25:39>

from data import Data
from model import ParsingModel
from tree import RSTTree
from evaluation import Metrics
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
    # ----------------------------------------
    # Load the parsing model
    pm = ParsingModel()
    pm.loadmodel("parsing-model.pickle.gz")
    # Build the gold tree from annotated file
    fname = "examples/wsj_0600.out.dis"
    gold_rst = RSTTree(fname=fname)
    gold_rst.build()
    # Get brackets from gold tree
    gold_brackets = gold_rst.bracketing()
    # ----------------------------------------
    # Parsing
    # Get all EDU texts for testing parsing
    texts = gold_rst.getedutext()
    # Build the RST tree from parsing model
    pred_rst = pm.sr_parse(texts)
    # Get brackets from parsing results
    pred_brackets = pred_rst.bracketing()
    print gold_brackets
    print pred_brackets
    # ----------------------------------------
    # Evaluation
    met = Metrics(levels=['span','nuclearity','relation'])
    # Call eval() function for evaluation on each tree pair
    # If you have multiple tree pairs, just keep calling
    # the eval() function until the end
    met.eval(gold_rst, pred_rst)
    # Print out the evaluation on different levels
    met.report()

if __name__ == '__main__':
    # Create data for offline training
    createdata()
    # Train a parsing model
    trainmodel()
    # Perform parsing on a training document
    parse()
    

    
