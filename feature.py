## feature.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/22/2014 16:27:11>


class FeatureGenerator(object):
    def __init__(self, stack, queue, doclen=None):
        """ Initialization of feature generator

        Currently, we only consider the feature generated
        from the top 2 spans from the stack, and the first
        span from the queue. However, you are available to
        use any other information for feature generation.
        - YJ
        
        :type stack: list
        :param stack: list of Node instance

        :type queue: list
        :param queue: list of Node instance

        :type doclen: int
        :param doclen: document length wrt EDUs
        """
        # Stack
        if len(stack) >= 2:
            self.span1, self.span2 = stack[-1], stack[-2]
        elif len(stack) == 1:
            self.span1, self.span2 = stack[-1], None
        else:
            self.span1, self.span2 = None, None
        # Queue
        if len(queue) > 0:
            self.span3 = queue[0]
        else:
            self.span3 = None
        # Document length
        self.doclen = doclen


    def features(self):
        """ Main function to generate features

        1, if you add any argument to this function, remember
           to give it a default value
        2, if you add any sub-function for feature generation,
           remember to call the sub-function here
        """
        features = []
        # Lexical features
        for feat in self.lexical_features():
            features.append(feat)
        # Status features
        for feat in self.status_features():
            features.append(feat)
        # Structural features
        for feat in self.structural_features():
            features.append(feat)
        return features
            
            

    def lexical_features(self, n=2):
        """ Lexical features

        I am not sure how much sense it will make when
        n > 2. Maybe I didn't realize it - YJ

        :type n: int
        :param n: n tokens at the beginning/end of Spans
        """
        features = []
        for feat in features:
            yield feat
            

    def structural_features(self):
        """ Structural features
        """
        features = []
        if self.span1 is not None:
            # Span Length wrt EDUs
            features.append(('Span1','Length-EDU',self.span1.eduspan[1]-self.span1.eduspan[0]+1))
            # Distance to the beginning of the document wrt EDUs
            features.append(('Span1','Distance-To-Begin',self.span1.eduspan[0]))
            # Distance to the end of the document wrt EDUs
            if self.doclen is not None:
                features.append(('Span1','Distance-To-End',self.doclen-self.span1.eduspan[1]))
        if self.span2 is not None:
            features.append(('Span2','Length-EDU',self.span2.eduspan[1]-self.span2.eduspan[0]+1))
            features.append(('Span2','Distance-To-Begin',self.span2.eduspan[0]))
            if self.doclen is not None:
                features.append(('Span2','Distance-To-End',self.doclen-self.span2.eduspan[1]))
        if self.span3 is not None:
            features.append(('Span3','Distance-To-Begin',self.span3.eduspan[0]))
        # Should include some features about the nucleus EDU
        for feat in features:
            yield feat
        

    def status_features(self):
        """ Features related to stack/queue status
        """
        features = []
        if (self.span1 is None) and (self.span2 is None):
            features.append(('Empty-Stack'))
        elif (self.span1 is not None) and (self.span2 is None):
            features.append(('One-Elem-Stack'))
        elif (self.span1 is not None) and (self.span2 is not None):
            features.append(('More-Elem-Stack'))
        else:
            raise ValueError("Unrecognized status in stack")
        if (self.span3 is None):
            features.append(('Empty-Queue'))
        else:
            features.append(('NonEmpty-Queue'))
        for feat in features:
            yield feat
