import argparse
import json
import time

import scipy
import scipy.stats
import numpy as np

from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import GridSearchCV

from auto_tune.evo.genes import RealGene
from auto_tune.evo.individual import Individual
from auto_tune.search import GPSearchCV

# Utility function to report best scores
def report(results, n_top=3):
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

parser = argparse.ArgumentParser(description='Benchmark auto-tune against other solutions')
parser.add_argument("--dataset", dest='dataset', default='iris', choices=['iris', 'digits', 'wine', 'breast_cancer'], help='which dataset to test on (default: iris)')
parser.add_argument("--algorithm", dest='algorithm', default='svm.SVC', choices=['svm.SVC'], help='which algorithm to test on (default: svm.SVC)')
parser.add_argument("--search-method", dest='search_method', default='auto-tune', choices=['auto-tune', 'grid', 'random'], help='search method to test against (default: auto-tune)')
parser.add_argument("--search-cv", dest='search_cv', type=int, default=3, help="search cross validation to be used (default: 3")
parser.add_argument("--search-auto-tune-pop-size", dest='search_auto_tune_pop_size', type=int, default=20, help='auto-tune population size (default: 20)')
parser.add_argument("--search-auto-tune-num-child", dest='search_auto_tune_num_child', type=int, default=5, help='auto-tune number of children (default: 5)')
parser.add_argument("--search-auto-tune-num-gen", dest='search_auto_tune_num_gen', type=int, default=10, help='auto-tune number of generations (default: 10)')
parser.add_argument("--search-auto-tune-params", dest='search_auto_tune_params', default='["RealGene(\\"C\\", scipy.stats.uniform(0.000001, 100), minimum=0.00000001)"]', help='auto-tune search params in the form of a json to be evaled (default: "[\\"RealGene(\\\\"C\\\\", scipy.stats.uniform(0.000001, 100))\\"]"')
parser.add_argument("--search-grid-params", dest='search_grid_params', default='{"C": [0.001, 0.01, 0.1, 1, 10]}', help='search params for the grid method in the form of a JSON string to be converted to a dict (default: {"kernel": ["rbf"], "C": [1,10]})')

args = parser.parse_args()

# Set dataset
if args.dataset == 'iris':
    dataset = datasets.load_iris()
elif args.dataset == 'digits':
    dataset = datasets.load_digits()
elif args.dataset == 'wine':
    dataset = datasets.load_wine()
elif args.dataset == 'breast_cancer':
    dataset = datasets.load_breast_cancer()
else:
    print("Error: invalid dataset")
    exit(-1)

# Set algorithm
if args.algorithm == 'svm.SVC':
    algorithm = svm.SVC()
else:
    print("Error: invalid algorithm")
    exit(-1)

# Get cv
search_cv = args.search_cv
if search_cv <= 0:
    print("Error: search-cv should be a positive number")
    exit(-1)

# Get auto_tune search params
safe_dict = {}
safe_dict['RealGene'] = RealGene
safe_dict['scipy.stats.uniform'] = scipy.stats.uniform

search_auto_tune_params_unprocessed = json.loads(args.search_auto_tune_params)
if type(search_auto_tune_params_unprocessed) is not list:
    print("Error: invalid search-auto-tune-params, it should be a list")
    exit(-1)

search_auto_tune_params = []
for p in search_auto_tune_params_unprocessed:
    # TODO fix security issue with eval, possible solution, but still doesnt work:
    # search_auto_tune_params.append(eval(p, {"__builtins__":None}, safe_dict))
    search_auto_tune_params.append(eval(p))

# Get grid search params
search_grid_params = json.loads(args.search_grid_params)
if type(search_grid_params) is not dict:
    print("Error: invalid search-grid-params, it should be a dict")


# Run search cv
start = time.time()
if args.search_method == "auto-tune":
    search = GPSearchCV(algorithm, search_auto_tune_params, args.search_auto_tune_pop_size, args.search_auto_tune_num_child, args.search_auto_tune_num_gen, dataset.data, dataset.target, verbose=1)
    for i in range(args.search_auto_tune_num_gen):
        print("----------------")
        print("Generation #%d" % i)
        print("----------------")
        search.step()
        print(search.best_estimator.model)
        print(search.best_estimator.genome)
        print(search.best_estimator.mean_score)
        print()
elif args.search_method == "grid":
    search = GridSearchCV(algorithm, search_grid_params, cv=search_cv)
    search.fit(dataset.data, dataset.target)
    report(search.cv_results_)
# TODO implement random search_method

stop = time.time()
print("Method took %.2f seconds" % (stop-start))
