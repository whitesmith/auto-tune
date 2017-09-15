import numpy as np

from sklearn.model_selection import cross_val_score


class Individual(object):
    def __init__(self, model, genome, data, target, phenome=None):
        self.model = model
        self.genome = genome
        self.phenome = phenome
        self.data = data
        self.target = target

        if self.phenome is None:
            self.phenome = [g.random() for g in self.genome]

        for i in range(len(self.phenome)):
            setattr(self.model, self.genome[i].param, self.phenome[i])

        self.scores = cross_val_score(self.model, self.data, self.target, cv=5)
        self.mean_score = np.mean(self.scores)
        self.std_score = np.std(self.scores)

    def recombine(self, other):
        phenome = []
        for i in range(len(self.phenome)):
            phenome.append(self.genome[i].recombine(self.phenome[i], other.phenome[i]))
