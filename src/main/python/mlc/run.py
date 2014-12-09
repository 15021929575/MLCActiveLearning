#! /usr/bin/env python

DISTMAT_DIR = ""
HCLUST_DIR = ""
MAVEN_DIR = ""
RESULT_DIR = ""
labels_file_path = ""
num_labels = 0
output_dir = ""
dh_path = ""
update_hcluster_path = ""

def run(reduction_type, distmat_name):
    maven_cmd = ["mvn", "-e", "exec:java", '-Dexec.mainClass="edu.cmu.abr.mlcdh.Main"', "-Dexec.classpathScope=runtime"]
    args = [reduction_type, labels_file_path, str(num_labels), output_dir, dh_path] 
    if reduction_type == "BR" or reduction_type == "RAkEL":
        hclust_file_path = os.path.join(HCLUST_DIR, ["hclust-" + distmat_name + ".tree"])
        args += [hclust_file_path]
    else:
        args += [update_hcluster_path]
        distmat_file_path = os.path.qoin(DISTMAT_DIR, [distmat_name + ".pkl"])
        args += [distmat_file_path]
    cmd = maven_cmd + ['-Dexec.args="' + " ".join(args) + '"']
    print "Running: " + " ".join(cmd)
    process = subprocess.Popen(args, cwd=MAVEN_DIR)
    process.wait()
    evaluations = json.load(open(os.path.join(output_dir, "evaluations.json")))
    return evaluations

def multi_run(reduction_type, distmat_name, num_runs):
    all_evaluations = []
    for i in xrange(num_runs):
        all_evaluations += run(reduction_type, distmat_name)
    avg = {metric : [] for metric in all_evaluations[0]}
    std = {metric : [] for metric in all_evaluations[0]}
    for metric in avg:
        for queries in xrange(len(all_evaluations[0][metric])):
            values = [all_evaluations[i][metric][queries] for i in xrange(num_runs)]
            avg[metric] += [np.mean(values)]
            std[metric] += [np.std(values)]
    return (avg, std)

def save_result(avg, std, save_dir):
    if not os.path.exists(save_dir) || not os.path.isdir(save_dir):
        os.path.mkdir(save_dir)
    for metric in avg:
        json.dump({"avg" : avg[metric], "std" : std[metric]}, open(os.path.join(dir, metric)));

def main(args):
    distmat_names = ["10mer-seuclidean", "3mer-seuclidean", "4mer-seuclidean", "5mer-seuclidean", "7mer-seuclidean", "9mer-seuclidean", "3mer-cosine", "4mer-cosine", "5,3-gappy-seuclidean", "6,3-gappy-seuclidean", "8,4-gappy-seuclidean", "3mer-mahalanobis", "4mer-mahalanobis", "5mer-cosine", "6mer-seuclidean", "8mer-seuclidean"]
    configs = [["BR", n] for n in distmat_names] + [["RAkEL", n] for n in distmat_names] + [["BR", n] for n in distmat_names if n.endswith("seuclidean")]
    num_runs = 10
    for config in configs:
        (avg, std) = multi_run(*config, num_runs)
        save_result(avg, std, os.path.join(RESULT_DIR, "-".join(config)))