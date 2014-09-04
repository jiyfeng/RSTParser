## datastructure.py
## Author: Yangfeng Ji
## Date: 08-29-2013
## Time-stamp: <yangfeng 09/03/2014 17:41:03>

class SpanNode(object):
    """ RST tree node
    """
    def __init__(self, form=None, relation=None):
        # Text of this span / Discourse relation
        self.text, self.relation = None, relation
        # EDU list of this span / Nucleus span
        self.edulist, self.nucspan = None, None
        # Nucleus single EDU
        self.nucedu = None
        # Children node
        # Each of them is a node instance
        # N-S form
        self.lnode, self.rnode = None, None
        # Relation form: NN, NS, SN
        self.form = form
        
