import yaml, os
from evaluations import plot_evaluations

def main():
    current_path = os.path.dirname(os.path.realpath(__file__)) # Path of this file

    evaluations = {"10mer Euclidean" : ("r", yaml.load(open(os.path.join(current_path,
                   "../../data/hclusts/hclust-10mer-seuclidean/evaluations.yaml")))),
                   "Random" : ("b", yaml.load(open(os.path.join(current_path,
                   "../../data/hclusts/hclust-random/evaluations.yaml"))))}
    metrics = ["Hamming Loss", "Accuracy"]
    plot_evaluations(evaluations, metrics)
