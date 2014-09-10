# RST Parser #

## Basic Description ##

RST parser trained on RST discourse treebank.

## Code Structure ##

- tree.py: RST Tree, including:
    - Read string to build a RST tree
    - Binarization of a general RST tree
    - Write an RST tree into string
- parser.py: shift-reduce parsing algorithm
    - Change the status of stack/queue according specific parsing action
- feature.py: feature generation module. Generating feature from 
    - current EDUs; 
    - current span; 
    - document structure; 
    - current queue/stack status;
- datastructure.py: data structure used in this project, including:
    - SpanNode: node structure of an RST tree
- model.py: including all parameters for parser and feature generation process
- learn.py: learning framework for shift-reduce parsing

### Data structure ###

A list of data structures which will be used in this project
- Node: which is one node of RST tree, should include all necessary information about a span

### Shift-reduce parsing ###

One SR paser mantain a stack and a queue. At the very beginning, all elements are in the queue and the stack is empty. The basic function of a SR parser is, given a parsing action, to change stack and queue status. 

### Feature generation ###

In this task, feature generation is based the status of the stack/queue. 

### Model ###

Taking the output from feature generation, and performing a classification task for determining the parsing action

### Learn ### 

Learn the model parameters