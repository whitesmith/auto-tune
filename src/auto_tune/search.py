import numpy as np
import random
import copy

from auto_tune.evo.genes import AbstractGene
from auto_tune.evo.individual import Individual


class GPSearchCV(object):
    def __init__(self, model, params, pop_size, n_child, n_iter, data, target, pop=None):
        if not hasattr(params, '__iter__'):
            raise ValueError("params should be an iterable")
        for param in params:
            if not isinstance(param, AbstractGene):
                raise ValueError("params should be an iterable of AbstractGene objects")

        self.model = model
        self.params = params
        self.pop_size = pop_size
        self.n_child = n_child
        self.n_iter = n_iter
        self.pop = pop
        self.data = data
        self.target = target

        if self.pop is None:
            self.generate_pop()
        self.best_score = 0
        self.best_estimator = self.pop[0]

    def generate_pop(self):
        self.pop = [Individual(copy.copy(self.model), self.params, self.data, self.target) for _ in range(self.pop_size)]

    # Roullete parental selection
    def generate_offspring(self):
        num_parents = 2
        sum_score = np.sum(list(map(lambda x: x.mean_score, self.pop)))
        offspring = []
        for i in range(self.n_child):
            parents = []
            for j in range(num_parents):
                r = random.uniform(0, sum_score)
                s = 0
                for ind in self.pop:
                    s += ind.mean_score
                    if r <= s:
                        parents.append(ind)
                        break
            phenome = parents[0].recombine(parents[-1])
            offspring.append(Individual(copy.copy(self.model), self.params, self.data, self.target, phenome=phenome))
        self.pop.extend(offspring)

    # Elitist environmental selection
    def environmental_selection(self):
        to_remove = sorted(self.pop, key=lambda x: x.mean_score)[:len(self.pop)-self.pop_size]
        for ind in to_remove:
            self.pop.pop(self.pop.index(ind))

    def scores_pop(self):
        return list(map(lambda x: x.mean_score, self.pop))

    def step(self):
        self.generate_offspring()
        self.environmental_selection()

        for ind in self.pop:
            if ind.mean_score > self.best_score:
                self.best_estimator = ind
                self.best_score = ind.mean_score

    def evolve(self):
        for _ in range(self.n_iter-1):
            self.step()
