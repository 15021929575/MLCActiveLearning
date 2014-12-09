import cPickle, os, hclust

distmat_filenames = os.listdir("distmats")

for distmat_filename in distmat_filenames:
    if distmat_filename != "distmat-alignment.pkl":
        distmat = hclust.load_distmat("distmats/" + distmat_filename)
        cPickle.dump(distmat, open("sdistmats/" + distmat_filename[8:], "w"))
