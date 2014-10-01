## tree.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 10/01/2014 15:01:09>

""" Any operation about an RST tree should be here
1, Build general/binary RST tree from annotated file
2, Binarize a general RST tree to the binary form
3, Generate bracketing sequence for evaluation
4, Write an RST tree into file (not implemented yet)
5, Generate Shift-reduce parsing action examples
6, Get all EDUs from the RST tree
- YJ
"""

from datastructure import *
from buildtree import *
from feature import FeatureGenerator
from parser import SRParser
from util import extractrelation


class RSTTree(object):
    def __init__(self, fname=None, tree=None):
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


    def bracketing(self):
        """ Generate brackets according an Binary RST tree
        """
        nodelist = postorder_DFT(self.tree, [])
        nodelist.pop() # Remove the root node
        brackets = []
        for node in nodelist:
            relation = extractrelation(node.relation)
            b = (node.eduspan, node.prop, relation)
            brackets.append(b)
        return brackets


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
        # Start simulating the shift-reduce parsing
        for action in actionlist:
            # Generate features
            fg = FeatureGenerator(stack, queue)
            features = fg.features()
            samplelist.append(features)
            # Change status of stack/queue
            sr = SRParser(stack, queue)
            sr.operate(action)
            # stack, queue = sr.getstatus()
        return (actionlist, samplelist)


    def getedutext(self):
        """ Get all EDU text here
        """
        edunodelist = getedunode(self.tree)
        texts = []
        for node in edunodelist:
            texts.append(node.text)
        return texts


    def gettree(self):
        """ Get the RST tree
        """
        return self.tree

def test():
    fname = "examples/wsj_0603.out.dis"
    rst = RSTTree(fname)
    rst.build()
    # actionlist, samplelist = rst.generate_samples()
    # print actionlist
    # print samplelist
    # for (action, sample) in zip(actionlist, samplelist):
    #     print action
    print rst.bracketing()
    print '----------------------------'
    rst = RSTTree("examples/wsj_0600.out.dis")
    rst.build()
    print rst.bracketing()


if __name__ == '__main__':
    test()
