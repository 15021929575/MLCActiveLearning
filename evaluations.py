def hamming_loss(predicted_multilabels, actual_multilabels, num_labels):
    HL = 0.0
    data_size = len(predicted_multilabels)
    for data in xrange(data_size):
        predicted_labels = predicted_multilabels[data]
        actual_labels = actual_multilabels[data]
        HL += len(predicted_labels.symmetric_difference(actual_labels))
    return HL / data_size / num_labels

def accuracy(predicted_multilabels, actual_multilabels):
    A = 0.0
    data_size = len(predicted_multilabels)
    for data in xrange(data_size):
        predicted_labels = predicted_multilabels[data]
        actual_labels = actual_multilabels[data]
        A += float(len(predicted_labels.intersection(actual_labels))) / \
             len(predicted_labels.union(actual_labels))
    return A / data_size

def precision(predicted_multilabels, actual_multilabels):
    P = 0.0
    data_size = len(predicted_multilabels)
    for data in xrange(data_size):
        predicted_labels = predicted_multilabels[data]
        actual_labels = actual_multilabels[data]
        P += float(len(predicted_labels.intersection(actual_labels))) / \
             len(predicted_labels)
    return P / data_size

def recall(predicted_multilabels, actual_multilabels):
    R = 0.0
    data_size = len(predicted_multilabels)
    for data in xrange(data_size):
        predicted_labels = predicted_multilabels[data]
        actual_labels = actual_multilabels[data]
        R += float(len(predicted_labels.intersection(actual_labels))) / \
             len(actual_labels)
    return R / data_size

def evaluate(all_predicted_multilabels, actual_multilabels, num_labels):
    evaluations = {}
    methods = [("Hamming Loss", lambda p, a: hamming_loss(p, a, num_labels)),
               ("Accuracy", accuracy),
               ("Precision", precision),
               ("Recall", recall)]
    for (name, method) in methods:
        evaluations[name] = {}
        for iteration in all_predicted_multilabels:
            evaluations[name][iteration] = method(all_predicted_multilabels[iteration],
                actual_multilabels)
    return evaluations
