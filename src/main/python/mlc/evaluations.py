#! /usr/bin/env python
import matplotlib.pyplot as plt
import os, sys, json, re

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) # Path of this file
EVALUATION_PATH = os.path.join(CURRENT_PATH, "../../resources/result/")
NUM_QUERIES = 141
COLORS = {"b": "blue", "g": "green", "r": "red", "c": "cyan",
          "m": "magenta", "y": "yellow", "k": "black"}

def load_evaluation(config, metric):
    return json.load(open(os.path.join(EVALUATION_PATH, config, metric)))

def plot_evaluations(configs, metric):
    fig = plt.figure(num=1, figsize=(20, 10))
    ax = plt.subplot(111)
    for i in xrange(len(configs)):
        config = configs[i]
        color = COLORS[COLORS.keys()[i % len(COLORS)]]
        evaluation = load_evaluation(config, metric)
        ax.errorbar(range(1, NUM_QUERIES + 1), evaluation["avg"], yerr=evaluation["std"], label=config)#, color=color)
    plt.xlabel("Number of queries")
    plt.ylabel(metric)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.show()

def plot_all(all_plots):
    for metric, configs in all_plots.items():
        plot_evaluations(configs, metric)

def main(args):
    configs = os.listdir(EVALUATION_PATH)
    #configs = [config for config in configs if re.match(".*RAkEL-(4mer|random).*" ,config)]
    #configs = [config for config in configs if re.match(".*RAkEL-(.*seu|random).*" ,config)]
    metrics = ["F1 macro avg, by ex.", "F1 macro avg, by lbl", "F1 micro avg",
               "Hamming loss", "Accuracy"]
    all_plots = { metric : configs for metric in metrics }
    plot_all(all_plots)

if __name__ == '__main__':
    main(sys.argv)