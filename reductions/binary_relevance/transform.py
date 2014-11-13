#! /usr/bin/env python

import sys, os

def transform(labels_file, output_dir, num_labels):
   binary_label_files = [open(os.path.join(output_dir, "label_" + str(l)), "w") \
                         for l in xrange(num_labels)]
   while True:
      line = labels_file.readline()
      if not line:
         break
      print line.split(",")
      labels = set([int(s) for s in line.split(",")])
      for l in xrange(num_labels):
         if l in labels:
            binary_label_files[l].write("1\n")
         else:
            binary_label_files[l].write("0\n")
   for f in binary_label_files:
      f.close()

if __name__ == "__main__":
   labels_file = open(sys.argv[1])
   output_dir = sys.argv[2]
   num_labels = int(sys.argv[3])
   transform(labels_file, output_dir, num_labels)
