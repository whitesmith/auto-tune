import numpy as np
import random


class AbstractGene(object):
    """Abstract Gene Class"""
    def __init__(self, param):
        self.param = param

    def random(self):
        raise NotImplementedError("random() not implemented")


class RealGene(AbstractGene):
    def __init__(self, param, start, stop):
        super().__init__(param)
        if(stop <= start):
            raise ValueError("Stop should be higher than start")
        self.start = start
        self.stop = stop

    def random(self):
        return random.uniform(self.start, self.stop)

    def recombine(self, a, b):
        return np.mean([a, b])
