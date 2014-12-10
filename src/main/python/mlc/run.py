#! /usr/bin/env python
import os, sys, json, subprocess
import numpy as np

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) # Path of this file

DISTMAT_DIR = os.path.join(CURRENT_PATH, "../../resources/sdistmats/")
HCLUST_DIR = os.path.join(CURRENT_PATH, "../../resources/hclusts/")
MAVEN_DIR = os.path.join(CURRENT_PATH, "../../../../")
RESULT_DIR = os.path.join(CURRENT_PATH, "../../resources/result/")
LABELS_FILE_PATH = os.path.join(CURRENT_PATH, "../../resources/hclusts/labels")
NUM_LABELS = 125
OUTPUT_DIR = os.path.join(CURRENT_PATH, "../../../../temp/")
DH_PATH = os.path.join(CURRENT_PATH, "../../cpp/DH/sample.out")
UPDATE_HCLUSTER_PATH = os.path.join(CURRENT_PATH, "../feats/update_hclust.py")
JAVA_HOME = "/usr/lib/jvm/java-7-openjdk-amd64/jre"

def run(reduction_type, distmat_name):
    maven_cmd = ["mvn", "-e", "exec:java", '-Dexec.mainClass=edu.cmu.abr.mlcdh.Main', "-Dexec.classpathScope=runtime"]
    args = [reduction_type, LABELS_FILE_PATH, str(NUM_LABELS), OUTPUT_DIR, DH_PATH] 
    if reduction_type == "BR" or reduction_type == "RAkEL":
        hclust_file_path = os.path.join(HCLUST_DIR, "hclust-" + distmat_name + ".tree")
        args += [hclust_file_path]
    else:
        args += [UPDATE_HCLUSTER_PATH]
        distmat_file_path = os.path.join(DISTMAT_DIR, distmat_name + ".pkl")
        args += [distmat_file_path]
    cmd = " ".join(maven_cmd + ['-Dexec.args="' + " ".join(args) + '" '])
    print "Running: " + cmd
    process = subprocess.Popen(cmd, cwd=MAVEN_DIR, env={"JAVA_HOME" : JAVA_HOME}, shell=True)
    process.wait()
    evaluations = json.load(open(os.path.join(OUTPUT_DIR, "evaluations.json")))
    return evaluations

def multi_run(reduction_type, distmat_name, num_runs):
    all_evaluations = []
    for i in xrange(num_runs):
        all_evaluations += [run(reduction_type, distmat_name)]
    avg = {metric : [] for metric in all_evaluations[0]}
    std = {metric : [] for metric in all_evaluations[0]}
    for metric in avg:
        for queries in xrange(len(all_evaluations[0][metric])):
            values = [all_evaluations[i][metric][queries] for i in xrange(num_runs)]
            avg[metric] += [np.mean(values)]
            std[metric] += [np.std(values)]
    return (avg, std)

def save_result(avg, std, save_dir):
    if not os.path.exists(save_dir) or not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for metric in avg:
        json.dump({"avg" : avg[metric], "std" : std[metric]}, open(os.path.join(save_dir, metric), "wb"));

def main(args):
    distmat_names = ["10mer-seuclidean", "3mer-seuclidean", "4mer-seuclidean", "5mer-seuclidean", "7mer-seuclidean", "9mer-seuclidean", "3mer-cosine", "4mer-cosine", "5,3-gappy-seuclidean", "6,3-gappy-seuclidean", "8,4-gappy-seuclidean", "3mer-mahalanobis", "4mer-mahalanobis", "5mer-cosine", "6mer-seuclidean", "8mer-seuclidean", "random"]
    configs = [["RAkEL", n] for n in distmat_names] + [["BR", n] for n in distmat_names] + [["CC", n] for n in distmat_names if n.endswith("seuclidean") or n == "random"]
    #configs = [["RAkEL", "random"], ["BR", "random"]] + [["CC", n] for n in distmat_names if n.endswith("seuclidean") or n == "random"]
    num_runs = 10
    for config in configs:
        (avg, std) = multi_run(*config, num_runs=num_runs)
        save_result(avg, std, os.path.join(RESULT_DIR, "-".join(config)))

if __name__ == '__main__':
    main(sys.argv)