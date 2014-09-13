## tree.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/13/2014 17:34:28>

""" Any operation about an RST tree should be here
"""

from datastructure import *
from buildtree import *
from feature import FeatureGenerator
from parser import SRParser


class RSTTree(object):
    def __init__(self, fname, tree=None):
        """ Initialization

        :type text: string
        :param text: dis file content
        """
        self.fname = fname
        self.binary = True
        self.tree = tree


    def build(self):
        """ Build BINARY RST tree
        """
        text = open(self.fname).read()
        self.tree = buildtree(text)
        self.tree = binarizetree(self.tree)
        self.tree = backprop(self.tree)


    def write(self, fname):
        """ Write tree into file

        :type fname: string
        :param fname: tree file name
        """
        pass


    def generate_samples(self):
        """ Generate samples from an binary RST tree
        """
        # Sample list
        samplelist = []
        # Parsing action
        actionlist = decodeSRaction(self.tree)
        # Initialize queue and stack
        queue = getedunode(self.tree)
        stack = []
        # Starting to simulate the shift-reduce parsing
        for action in actionlist:
            # Generate features
            fg = FeatureGenerator(stack, queue)
            features = fg.features()
            samplelist.append(features)
            # Change status of stack/queue
            sr = SRParser(stack, queue)
            sr.operate(action)
            stack, queue = sr.getstatus()
        return (actionlist, samplelist)
        

def test():
    fname = "examples/wsj_0603.out.dis"
    rst = RSTTree(fname, binary=True)
    rst.build()
    actionlist, samplelist = rst.generate_samples()
    print actionlist
    print samplelist


if __name__ == '__main__':
    test()
