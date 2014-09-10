## datastructure.py
## Author: Yangfeng Ji
## Date: 08-29-2013
## Time-stamp: <yangfeng 09/09/2014 18:02:31>

class SpanNode(object):
    """ RST tree node
    """
    def __init__(self, text=None):
        """ Initialization of SpanNode

        :type text: string
        :param text: text of this span
        """
        # Text of this span / Discourse relation
        self.text, self.relation = text, None
        # EDU list of this span / Nucleus span (also list)
        self.edulist, self.nucspan = None, None
        # Nucleus single EDU
        self.nucedu = None
        # Children node
        # Each of them is a node instance
        # N-S form
        self.lnode, self.rnode = None, None
        # Relation form: NN, NS, SN
        self.form = None
        
