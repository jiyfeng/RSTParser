## datastructure.py
## Author: Yangfeng Ji
## Date: 08-29-2013
## Time-stamp: <yangfeng 09/11/2014 16:46:21>

class SpanNode(object):
    """ RST tree node
    """
    def __init__(self, prop):
        """ Initialization of SpanNode

        :type text: string
        :param text: text of this span
        """
        # Text of this span / Discourse relation
        self.text, self.relation = None, None
        # EDU span / Nucleus span (begin, end) index
        self.eduspan, self.nucspan = None, None
        # Nucleus single EDU
        self.nucedu = None
        # Property
        self.prop = prop
        # Children node
        # Each of them is a node instance
        # N-S form (for binary RST tree only)
        self.lnode, self.rnode = None, None
        # Parent node
        self.pnode = None
        # Node list (for general RST tree only)
        self.nodelist = []
        # Relation form: NN, NS, SN
        self.form = None
        
