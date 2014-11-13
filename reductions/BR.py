#! /usr/bin/env python

def transform(multilabels, num_labels):
   """Creates a binary labeling for every label
   """
   binary_labels = [[None] * len(multilabels) for label in xrange(num_labels)]
   for data in xrange(len(multilabels)):
      for label in xrange(num_labels):
         if label in multilabels[data]:
            binary_labels[label][data] = 1
         else:
            binary_labels[label][data] = 0
   return binary_labels
