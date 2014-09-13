## feature.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/13/2014 17:33:03>


class FeatureGenerator(object):
    def __init__(self, stack, queue):
        """ Initialization of feature generator

        :type stack: list
        :param stack: list of Node instance

        :type queue: list
        :param queue: list of Node instance
        """
        self.stack = stack
        self.queue = queue


    def features(self):
        """ Main function to generate features
        """
        return []


    def lexical_features(self, n):
        """ Lexical features

        :type n: int
        :param n: n tokens at the beginning/end of EDUs
        """
        pass


    def structural_features(self):
        """ Structural features
        """
        pass
