## parser.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/03/2014 17:50:19>

""" Shift-reduce parser
"""

from datastructure import *

class SRParser(object):
    def __init__(self):
        """ Initialization
        """
        self.Stack = []
        self.Queue = []


    def init(self, texts):
        """ Using text to initialize Queue

        :type texts: list of string
        :param texts: a sequence of EDUs for parsing
        """
        pass


    def parselabel(self, label):
        items = label.split('-')
        if len(items) == 1:
            return (label, None, None)
        elif len(items) == 3:
            return (items[0], items[1], items[2])
        else:
            raise ValueError("Unrecognized parsing label")
            

    def operate(self, label):
        """ According to parsing label to modify the status of
            the Stack/Queue

        Need a special exception for parsing error -YJ

        :type label: string
        :param label: one specific parsing action, for example
                      reduce-NS-elaboration
        """
        action, form, relation = self.parselabel(label)
        if action == 'shift':
            node = self.Queue.pop(0)
            self.Stack.append(node)
        elif action == 'reduce':
            rnode = self.Stack.pop()
            lnode = self.Stack.pop()
            # Create a new node
            node = SpanNode(form, relation)
            # Children node
            node.lnode, node.rnode = lnode, rnode
            # Node text
            node.text = lnode.text + " " + rnode.text
            # EDU list
            node.edulist = lnode.edulist + rnode.edulist
            # Nuc span / Nuc EDU
            if form == 'NN':
                node.nucspan = lnode.edulist + rnode.edulist
                node.nucedu = lnode.nucedu
            elif form == 'NS':
                node.nucspan = lnode.edulist
                node.nucedu = lnode.nucedu
            elif form == 'SN':
                node.nucspan = rnode.edulist
                node.nucedu = rnode.nucedu
            else:
                raise ValueError("Unrecognized form: {}".format(form))

            
