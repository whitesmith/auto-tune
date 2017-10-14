import numpy as np
import random
import copy

from sklearn.model_selection import cross_val_score


class Individual(object):
    def __init__(self, model, genome, data, target, mutation_probability=0.05):
        self.model = model
        self.genome = genome
        self.data = data
        self.target = target
        self.mutation_probability = mutation_probability

        self.set_model_attributes()
        self.calculate_scores()

        print(self)

    def __str__(self):
        return "%s: %f (std dev. %f)" % (self.genome, self.mean_score, self.std_score)

    def __repr__(self):
        return self.__str__()

    def set_model_attributes(self):
        params = {}
        for gene in self.genome:
            params[gene.param] = gene.value
        self.model.set_params(**params)
        # setattr(self.model, gene.param, gene.value)

    def calculate_scores(self):
        self.scores = cross_val_score(self.model, self.data, self.target, cv=5)
        self.mean_score = np.mean(self.scores)
        self.std_score = np.std(self.scores)

    """ Apply in place mutation """
    def mutate(self):
        if random.random() < self.mutation_probability:
            ind = random.randint(0, len(self.genome)-1)
            self.genome[ind].global_mutation()
            self.set_model_attributes()
            self.calculate_scores()

    """ Copy individual and apply local mutation on a single gene """
    """ Return the new individual """
    def generate_child(self):
        new_genome = copy.deepcopy(self.genome)
        ind = random.randint(0, len(new_genome)-1)
        new_genome[ind].local_mutation()

        new_individual = Individual(copy.deepcopy(self.model), new_genome, self.data, self.target)

        return new_individual

