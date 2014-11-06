## datastructure.py
## Author: Yangfeng Ji
## Date: 08-29-2013
## Time-stamp: <yangfeng 11/06/2014 10:33:23>

class SpanNode(object):
    """ RST tree node
    """
    def __init__(self, prop):
        """ Initialization of SpanNode

        :type prop: string
        :param prop: property of this span wrt its parent node.
                     Only two possible values: Nucleus or Satellite
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
        

class ParseError(Exception):
    """ Exception for parsing
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ActionError(Exception):
    """ Exception for illegal parsing action
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
