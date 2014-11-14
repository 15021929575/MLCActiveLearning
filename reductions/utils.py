import os, glob, yaml

def read_multilabels_file(labels_file_path):
    multilabels = []
    with open(labels_file_path, "r") as labels_file:
        while True:
            line = labels_file.readline()
            if not line:
                break
            labels = set([int(s) for s in line.split(",")])
            multilabels.append(labels)
        return multilabels

def write_multilabels_file(multilabels, labels_file_path):
    with open(labels_file_path, "w") as labels_file:
        for multilabel in multilabels:
            labels_file.write(str(",".join([str(l) for l in multilabel]) + "\n"))

def read_singlelabels_file(labels_file_path):
    singlelabels = []
    with open(labels_file_path, "r") as labels_file:
        while True:
            line = labels_file.readline()
            if not line:
                break
            singlelabels.append(int(line))
        return singlelabels

def write_singlelabels_file(labels, labels_file_path):
    with open(labels_file_path, "w") as labels_file:
        for label in labels:
            labels_file.write(str(label) + "\n")

def read_and_sort_shuffled_singlelabels_file(labels_file_path):
    """Sorts the output single label file of DH into a the single labels
    """
    with open(labels_file_path, "r") as labels_file:
        lines = labels_file.readlines()
        labels = [None] * len(lines)
        for line in lines:
            split_line = line.split(" ")
            labels[int(split_line[0])] = int(split_line[1])
        return labels

def dump(obj, output_file_path):
    with open(output_file_path + ".yaml", "w") as output_file:
        yaml.dump(obj, output_file)

def get_default_paths(directory_path):
    """Get default paths for the labels file and the tree file in a directory    
    """
    return (os.path.join(directory_path, "labels"),
            os.path.join(directory_path, "tree"))

def dh(num_labels, tree_file_path, labels, output_path,
       seed=42, select_type=1, period=100):
    labels_file_path = os.path.join(output_path, "labels")
    write_singlelabels_file(labels, labels_file_path)
    current_path = os.path.dirname(os.path.realpath(__file__)) # Path of this file
    dh_path = os.path.join(current_path, "../DH/sample.out")
    dh_output_filename_prefix = "predictions_at_iteration_"
    dh_output_prefix = os.path.join(output_path, dh_output_filename_prefix)
    command = [dh_path,
               "--seed", str(seed),
               "--sel_type", str(select_type),
               "--period", str(period),
               str(num_labels), tree_file_path, labels_file_path,
               dh_output_prefix]
    os.system(" ".join(command))
    all_predictions = {}
    for predictions_file_path in glob.iglob(dh_output_prefix + "*"):
        # Iterating over all prediction files DH output
        predictions_file_name = os.path.basename(predictions_file_path)
        # Output from DH are named PREFIX.ITERATION
        iteration = int(predictions_file_name[len(dh_output_filename_prefix) + 1:])
        all_predictions[iteration] = \
            read_and_sort_shuffled_singlelabels_file(predictions_file_path)
    return all_predictions
