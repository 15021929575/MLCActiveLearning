#! /usr/bin/env python
"""Sorts the output label file of DH into a the same format DH takes in
"""

import sys, os

def sort(labels_file, output_file):
    lines = labels_file.readlines()
    labels = [None] * len(lines)
    for line in lines:
        split_line = line.split(" ")
        labels[int(split_line[0])] = split_line[1]
    for label in labels:
        output_file.write(label)

if __name__ == "__main__":
    labels_file = open(sys.argv[1])
    output_file = open(sys.argv[2], "w")
    sort(labels_file, output_file)
