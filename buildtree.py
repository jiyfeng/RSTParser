## buildtree.py
## Author: Yangfeng Ji
## Date: 09-10-2014
## Time-stamp: <yangfeng 09/11/2014 16:46:39>

from datastructure import *

def checkcontent(label, c):
    """ Check whether the content is legal

    :type label: string
    :param label: parsing label, such 'span', 'leaf'

    :type c: list
    :param c: list of tokens
    """
    if len(c) > 0:
        raise ValueError("{} with content={}".format(label, c))


def createtext(lst):
    """ Create text from a list of tokens

    :type lst: list
    :param lst: list of tokens
    """
    newlst = []
    for item in lst:
        item = item.replace("_!","")
        newlst.append(item)
    text = ' '.join(newlst)
    # Lower-casing
    return text.lower()


def BFT(tree):
    """ Breadth-first treavsal on general RST tree
    """
    queue = [tree]
    bft_nodelist = []
    while queue:
        node = queue.pop(0)
        bft_nodelist.append(node)
        queue += node.nodelist
    return bft_nodelist


def BFTbin(tree):
    """ Breadth-first treavsal on binary RST tree
    """
    queue = [tree]
    bft_nodelist = []
    while queue:
        node = queue.pop(0)
        bft_nodelist.append(node)
        if node.lnode is not None:
            queue.append(node.lnode)
        if node.rnode is not None:
            queue.append(node.rnode)
    return bft_nodelist


def processtext(tokens):
    """ Preprocessing token list for filtering '(' and ')' in text

    :type tokens: list
    :param tokens: list of tokens
    """
    within_text = False
    for (idx, tok) in enumerate(tokens):
        if "_!" in tok:
            within_text = not within_text
        if ('(' in tok) and (within_text):
            tok = tok.replace('(','-LB-')
        if (')' in tok) and (within_text):
            tok = tok.replace(')','-RB-')
        tokens[idx] = tok
    return tokens
    

def createnode(node, content):
    """ Assign value to an SpanNode instance

    :type node: SpanNode instance
    :param node: A new node in an RST tree

    :type content: list
    :param content: content from stack
    """
    for c in content:
        # print 'type(c) = {}'.format(type(c))
        if isinstance(c, SpanNode):
            # Sub-node
            node.nodelist.append(c)
            c.pnode = node
        elif c[0] == 'span':
            node.eduspan = (c[1], c[2])
        elif c[0] == 'relation':
            node.relation = c[1]
        elif c[0] == 'leaf':
            node.eduspan = (c[1], c[1])
            node.nucspan = (c[1], c[1])
            node.nucedu = c[1]
        elif c[0] == 'text':
            node.text = c[1]
        else:
            raise ValueError("Unrecognized property: {}".format(c[0]))
    return node


def buildtree(text):
    """ Build tree from *.dis file
    """
    tokens = text.strip().replace('\n','').replace('(', ' ( ').replace(')', ' ) ').split()
    queue = processtext(tokens)
    # print 'queue = {}'.format(queue)
    stack = []
    while queue:
        token = queue.pop(0)
        if token == ')':
            # If ')', start processing
            content = [] # Content in the stack
            while stack:
                cont = stack.pop()
                if cont == '(':
                    break
                else:
                    content.append(cont)
            content.reverse() # Reverse to the original order
            # Parse according to the first content word
            if len(content) < 2:
                raise ValueError("content = {}".format(content))
            label = content.pop(0)
            if label == 'Root':
                node = SpanNode(prop=label)
                node = createnode(node, content)
                stack.append(node)
            elif label == 'Nucleus':
                node = SpanNode(prop=label)
                node = createnode(node, content)
                stack.append(node)
            elif label == 'Satellite':
                node = SpanNode(prop=label)
                node = createnode(node, content)
                stack.append(node)
            elif label == 'span':
                # Merge
                beginindex = int(content.pop(0))
                endindex = int(content.pop(0))
                stack.append(('span', beginindex, endindex))
            elif label == 'leaf':
                # Merge 
                eduindex = int(content.pop(0))
                checkcontent(label, content)
                stack.append(('leaf', eduindex, eduindex))
            elif label == 'rel2par':
                # Merge
                relation = content.pop(0)
                checkcontent(label, content)
                stack.append(('relation',relation))
            elif label == 'text':
                # Merge
                txt = createtext(content)
                stack.append(('text', txt))
            else:
                raise ValueError("Unrecognized parsing label: {}".format(label))
        else:
            # else, keep push into the stack
            stack.append(token)
    return stack[-1]
        

def binarizetree(tree):
    """ Convert a general RST tree to a binary RST tree

    :type tree: instance of SpanNode
    :param tree: a general RST tree
    """
    queue = [tree]
    while queue:
        node = queue.pop(0)
        queue += node.nodelist
        # Construct binary tree
        if len(node.nodelist) == 2:
            node.lnode = node.nodelist[0]
            node.rnode = node.nodelist[1]
            # Parent node
            node.lnode.pnode = node
            node.rnode.pnode = node
        elif len(node.nodelist) > 2:
            # Remove one node from the nodelist
            node.lnode = node.nodelist.pop(0)
            newnode = SpanNode(node.nodelist[0].prop)
            newnode.nodelist += node.nodelist
            # Right-branching
            node.rnode = newnode
            # Parent node
            node.lnode.pnode = node
            node.rnode.pnode = node
            # Add to the head of the queue
            # So the code will keep branching
            # until the nodelist size is 2
            queue.insert(0, node)
        # Clear nodelist for the current node
        node.nodelist = []
    return tree


def backprop(tree):
    """ Starting from leaf node, propagating node
        information back to root node
    """
    treenodes = BFTbin(tree)
    treenodes.reverse()
    for node in treenodes:
        if (node.lnode is not None) and (node.rnode is not None):
            # Non-leaf node
            node.eduspan = __getspaninfo(node.lnode, node.rnode)
            node.text = __gettextinfo(node.lnode, node.rnode)
            if node.relation is None:
                # If it is a new node
                node.relation = __getrelationinfo(node.lnode, node.rnode)
            node.form, node.nucspan = __getforminfo(node.lnode, node.rnode)
        elif (node.lnode is None) and (node.rnode is not None):
            # Illegal node
            pass
        elif (node.lnode is not None) and (node.rnode is None):
            # Illegal node
            pass
        else:
            # Leaf node
            pass
    return treenodes[-1]


def __getspaninfo(lnode, rnode):
    """ Get span size for parent node
    """
    eduspan = (lnode.eduspan[0], rnode.eduspan[1])
    return eduspan


def __getforminfo(lnode, rnode):
    """ Get Nucleus/Satellite form and Nucleus span
    """
    if (lnode.prop=='Nucleus') and (rnode.prop=='Satellite'):
        nucspan = lnode.eduspan
        form = 'NS'
    elif (lnode.prop=='Satellite') and (rnode.prop=='Nucleus'):
        nucspan = rnode.eduspan
        form = 'SN'
    elif (lnode.prop=='Nucleus') and (rnode.prop=='Nucleus'):
        nucspan = (lnode.eduspan[0], rnode.eduspan[1])
        form = 'NN'
    else:
        raise ValueError("")
    return (form, nucspan)


def __getrelationinfo(lnode, rnode):
    """ Get relation information
    """
    if (lnode.prop=='Nucleus') and (rnode.prop=='Nucleus'):
        relation = lnode.relation
    else:
        print 'lnode.prop = {}'.format(lnode.prop)
        print 'rnode.prop = {}'.format(rnode.prop)
        raise ValueError("Error when find relation for new node")
    return relation


def __gettextinfo(lnode, rnode):
    """ Get text span for parent node
    """
    text = lnode.text + " " + rnode.text
    return text
        

def test():
    fname = "examples/wsj_0603.out.dis"
    text = open(fname, 'r').read()
    T = buildtree(text)
    T = binarizetree(T)
    T = backprop(T)
    print T.text


if __name__ == '__main__':
    test()
