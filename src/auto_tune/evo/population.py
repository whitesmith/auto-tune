import numpy as np
import random


class Population(object):
    def __init__(self, individuals):
        self.individuals = individuals

    def _rws(self, pointers):
        individuals = sorted(self.individuals, key=lambda x: x.mean_score, reverse=True)
        scores = list(map(lambda x: x.mean_score, individuals))
        chosen = []
        f = 0
        i = 0
        l = len(pointers)
        for ind in individuals:
            f += ind.mean_score
            while pointers[i] <= f:
                chosen.append(ind)
                i += 1
                if i >= l:
                    break
            if i >= l:
                break

        return chosen

    def _sus(self, num):
        F = np.sum(list(map(lambda x: x.mean_score, self.individuals)))
        N = num
        P = float(F)/N
        start = random.uniform(0,P)
        pointers = [start + i*P for i in range(N)]

        return self._rws(pointers)

    """
    Select "num" items from "pop" of Individuals based SUS 
    There might be repeated individuals
    """
    def select(self, num):
        return self._sus(num)

    """ Remove "num" items from "pop" of Individuals in place, uses SUS """
    def remove(self, num):
        num_to_keep = len(self.individuals) - num
        to_keep = self._sus(num_to_keep)
        to_remove = list(set(self.individuals)-set(to_keep))
        for individual in to_remove[:num]:
            self.individuals.pop(self.individuals.index(individual))

    """ Evolve generation: produces "num" children, and removes worst solutions """
    def evolve(self, num):
        parents = self.select(num)
        for parent in parents:
            self.individuals.append(parent.generate_child())
        self.remove(num)

