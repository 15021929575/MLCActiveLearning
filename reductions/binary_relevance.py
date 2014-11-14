from utils import *
from evaluations import evaluate
from numpy.random import permutation

def multilabels_to_binary_labels(multilabels, num_labels):
    data_size = len(multilabels)
    binary_labels = [[None] * data_size for label in xrange(num_labels)]
    for data in xrange(len(multilabels)):
        for label in xrange(num_labels):
            if label in multilabels[data]:
                binary_labels[label][data] = 1
            else:
                binary_labels[label][data] = 0
    return binary_labels

def binary_labels_to_multilabels(binary_labels):
    data_size = len(binary_labels[0])
    num_labels = len(binary_labels)
    multilabels = [None] * data_size
    for data in xrange(data_size):
        multilabels[data] = set()
        for label in xrange(num_labels):
            if binary_labels[label][data] == 1:
                multilabels[data].add(label)
        # TENTATIVE -- If no labels are found, pick a random subset
        if len(multilabels[data]) == 0:
            multilabels[data] = set(permutation(range(num_labels)).tolist())
    return multilabels

def main():
    import os
    
    current_path = os.path.dirname(os.path.realpath(__file__)) # Path of this file
    output_path = os.path.join(current_path, "../test_data")

    (multilabels_file_path, tree_file_path) = get_default_paths(output_path)
    num_labels = 4

    multilabels = read_multilabels_file(multilabels_file_path)
    binary_labels = multilabels_to_binary_labels(multilabels, num_labels)
    predictions = [None] * num_labels
    for label in xrange(num_labels):
        path = os.path.join(output_path, "label_" + str(label))
        if not os.path.exists(path):
            os.makedirs(path)
        predictions[label] = dh(num_labels, tree_file_path,
            binary_labels[label], path, period=1)
    multilabel_predictions = {}
    for iteration in predictions[0]:
        iteration_predictions = [None] * num_labels
        for label in xrange(num_labels):
            iteration_predictions[label] = predictions[label][iteration]
        multilabel_predictions[iteration] = \
            binary_labels_to_multilabels(iteration_predictions)
        write_multilabels_file(multilabel_predictions[iteration],
            os.path.join(output_path, "predictions_at_iteration_" + str(iteration)))
    evaluations = evaluate(multilabel_predictions, multilabels, num_labels)
    dump(evaluations, os.path.join(output_path, "evaluations"))
    dump(multilabel_predictions, os.path.join(output_path, "predictions"))
