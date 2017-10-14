import numpy as np
import random
import copy

from auto_tune.evo.genes import AbstractGene
from auto_tune.evo.individual import Individual
from auto_tune.evo.population import Population


class GPSearchCV(object):
    def __init__(self, model, params, pop_size, n_child, n_iter, data, target, pop=None, verbose=0):
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
        self.verbose = verbose

        if self.pop is None:
            self.generate_pop()

        if self.verbose >= 1:
            self._print_population()

        self.best_score = 0
        self.best_estimator = self.pop.individuals[0]

    def generate_pop(self):
        individuals = []
        for _ in range(self.pop_size):
            genome = copy.deepcopy(self.params)
            for gene in genome:
                gene.random_value()
            individuals.append(Individual(copy.deepcopy(self.model), genome, self.data, self.target))
        self.pop = Population(individuals)
    
    def scores_pop(self):
        return list(map(lambda x: x.mean_score, self.pop))

    def step(self):
        self.pop.evolve(self.n_child)

        if self.verbose >= 1:
            self._print_population()

        for ind in self.pop.individuals:
            if ind.mean_score > self.best_score:
                self.best_estimator = ind
                self.best_score = ind.mean_score

    def evolve(self):
        for _ in range(self.n_iter-1):
            self.step()

    def _print_population(self):
        print("\n###### Population")
        for ind in self.pop.individuals:
            print(ind)
        print("######\n")



