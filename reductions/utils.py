def read_multilabels_file(labels_file_path):
   multilabels = []
   with open(labels_file_path, "r") as labels_file:
      while True:
         line = labels_file.readline()
         labels = set([int(s) for s in line.split(",")])
         multilabels.append(labels)
      return multilabels

def write_singlelabels_file(labels, labels_file_path):
   with open(labels_file_path, "w") as labels_file:
      for label in labels:
         labels_file.write(str(label) + "\n")

def sort(labels_file, output_file):
   """Sorts the output label file of DH into a the same format DH takes in
   """
    lines = labels_file.readlines()
    labels = [None] * len(lines)
    for line in lines:
        split_line = line.split(" ")
        labels[int(split_line[0])] = split_line[1]
    for label in labels:
        output_file.write(label)