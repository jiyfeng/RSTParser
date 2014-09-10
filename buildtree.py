## buildtree.py
## Author: Yangfeng Ji
## Date: 09-10-2014
## Time-stamp: <yangfeng 09/10/2014 14:38:44>

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
    """ Breadth-first treavsal on tree
    """
    pass


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
        print 'type(c) = {}'.format(type(c))
        if isinstance(c, SpanNode):
            # Sub-node
            node.nodelist.append(c)
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
    tokens = text.strip().replace('\n','').replace('(', ' ( ').replace(')', ' ) ').split()
    queue = processtext(tokens)
    print 'queue = {}'.format(queue)
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
        
    
def test():
    fname = "examples/wsj_0603.out.dis"
    text = open(fname, 'r').read()
    T = buildtree(text)


if __name__ == '__main__':
    test()
