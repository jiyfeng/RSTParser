## data.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/13/2014 18:43:57>

""" Construct data for training/dev/test data.
Following three steps:
1, build data
2, build vocab (optional, not necessary if vocabs are given)
3, build matrix
4, save/get matrix
5, save/get vocabs (optional, necessary if new)
"""

from collections import defaultdict
from tree import RSTTree
from cPickle import dump
import os, numpy, gzip

class Data(object):
    def __init__(self, vocab=None, labelmap={}):
        """ Initialization

        :type vocab: dict
        :param vocab: collections of {feature:index}

        :type labelmap: dict
        :param labelmap: collections of {label:index}
        """
        self.vocab, self.labelmap = vocab, labelmap
        self.actionlist = []
        self.samplelist = []
        self.M, self.L = None, None

        
    def builddata(self, path):
        """ Build a list of feature list from a given path

        :type path: string
        :param path: data path, where all data files are saved
        """
        files = [os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith('.dis')]
        for fname in files:
            rst = RSTTree(fname=fname)
            rst.build()
            actionlist, samplelist = rst.generate_samples()
            self.actionlist += actionlist
            self.samplelist += samplelist
        

    def buildmatrix(self):
        """ Read the results from builddata, and construct
            data matrix
        """
        nSample, nFeat = len(self.samplelist), len(self.vocab)
        self.M = ssp.lil_matrix((nSample, nFeat))
        self.L = [-1]*nSample
        for (sidx, sample) in enumerate(self.samplelist):
            label = action2label(self.actionlist[sidx])
            vec = vectorize(sample, self.vocab)
            lidx = self.labelmap[label]
            self.M[sidx, :] = vec
            self.L.append(lidx)
        self.L = numpy.array(self.L)


    def buildvocab(self, thresh):
        """ Build dict from the current data

        :type thresh: int
        :param thresh: lower thresh for filtering features
        """
        featcounts = defaultdict(int)
        for (action, sample) in zip(self.actionlist, self.samplelist):
            for feat in sample:
                featcounts[feat] += 1
            # Create label mapping
            label = action2label(action)
            try:
                labelindex = self.labelmap[label]
            except KeyError:
                nlabel = len(self.labelmap)
                self.labelmap[label] = nlabel
        # Filter features
        index = 0
        for (feat, val) in featcounts.iteritems():
            if val >= thresh:
                self.vocab[feat] = index
                index += 1


    def savematrix(self, fname):
        """ Save matrix into file

        :type fname: string
        :param fname: 
        """
        if not fname.endswith(".gz"):
            fname += ".gz"
        D = {'matrix':self.M, 'labels':self.L}
        with gzip.open(fname, 'w') as fout:
            dump(D, fout)
        print 'Save data matrix into file: {}'.format(fname)
        

    def getvocab(self):
        """ Get feature vocab and label mapping
        """
        return (self.vocab, self.labelmap)


    def getmatrix(self):
        """ Get data matrix and labels
        """
        return (self.M, self.L)
        

    def savevocab(self, fname):
        """ Save vocab into file

        :type fname: string
        :param fname: 
        """
        if not fname.endswith('.gz'):
            fname += '.gz'
        D = {'vocab':self.vocab, 'labelmap':self.labelmap}
        with gzip.open(fname, 'w') as fout:
            dump(D, fout)
        print 'Save vocab into file: {}'.format(fname)
