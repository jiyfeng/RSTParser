# RST Parser #

## Basic Description ##

RST parser trained on RST discourse treebank.

## Code Structure ##

- parser.py: shift-reduce parsing algorithm
- learn.py: learning framework for shift-reduce parsing
- feature.py: feature generation module. Generating feature from (1) current EDU; (2) current span; (3) document structure; (4) current queue/stack status
- datastructure.py: data structure used in this project
--* tree.py: discourse tree structure (reuse from original code). Including everything in the RST tree
--* node.py: RST node (reuse from original code, pure data structure)
- model.py: including all parameters for parser and feature generation process

