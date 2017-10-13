import numpy as np
import random


class AbstractGene(object):
    """Abstract Gene Class"""
    def __init__(self, param, value):
        self.param = param
        self.value = value

    def __str__(self):
        return "%s: %s" % (self.param, self.value)

    def __repr__(self):
        return "AbstractGene(%s, %s)" % (self.param, self.value)

    def random_value(self):
        raise NotImplementedError("random_value(self) not implemented")


class RealGene(AbstractGene):
    def __init__(self, param, dist, minimum=None, maximum=None, value=None):
        super().__init__(param, value)

        if(minimum != None and maximum != None and maximum <= minimum):
            raise ValueError("Maximum should be higher than minimum")

        self.dist = dist
        self.minimum = minimum
        self.maximum = maximum

        if value == None:
            self.random_value()

    def random_value(self):
        self.value = self.dist.rvs()
        return self.value

    def global_mutation(self):
        self.random_value()

    def local_mutation(self):
        loc = self.value
        scale = self.dist.std() / 5.0
        self.value = np.random.normal(loc=loc, scale=scale)
        if self.minimum != None:
            self.value = max(self.minimum, self.value)
        if self.maximum != None:
            self.value = min(self.maximum, self.value)

