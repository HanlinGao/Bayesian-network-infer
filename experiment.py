import exact_infer
import approximate_infer

# initialization
bnfile = 'dog-problem.xml'
query_var = 'hear-bark'
evidences = ['light-on', 'true', 'bowel-problem', 'true']

# create dictionary for evidences, the key is the name (represented by capital characters), the value is true or false
evidence_dict = {}
length = len(evidences)
i = 0
while i < length:
    if evidences[i + 1] == 'True' or 'true' or 'TRUE':
        evidence_dict[evidences[i]] = True
    elif evidences[i + 1] == 'False' or 'false' or 'FALSE':
        evidence_dict[evidences[i]] = False
    else:
        print('invalid parameters, please input true or false')
        break
    i += 2

bayes_net = exact_infer.BayesNet(bnfile)
ground_truth = exact_infer.enumeration_ask(query_var, evidence_dict, bayes_net)

# create two lists for evidences, one is evidence_var ['J', 'M'], one is evidence_value [True, False]
evidence_var = []
evidence_value = []
length = len(evidences)
i = 0
while i < length:
    if evidences[i + 1] == 'True' or 'true' or 'TRUE':
        evidence_var.append(evidences[i])
        evidence_value.append(True)
    elif evidences[i + 1] == 'False' or 'false' or 'FALSE':
        evidence_var.append(evidences[i])
        evidence_value.append(False)
    else:
        print('invalid parameters, please input true or false')
        break
    i += 2

# sampling initialization
sample_num = 1000

# create network
variables, properties, parents, tables = approximate_infer.parsing_file(approximate_infer.access_file(bnfile))
network = approximate_infer.network_construction(variables, properties, parents, tables)
for each in network:
    each.set_visited(False)
sorted_nodes = approximate_infer.topological_sort(network)


def rejection_sampling(n, Query_variable, evidence_variables, evidence_values):
    num = 0
    count = [0, 0]
    while num < n:
        consistency = True
        sample = approximate_infer.prior_sampling(sorted_nodes)
        length = len(evidence_variables)
        for j in range(length):
            consistency = (consistency and (sample[evidence_variables[j]] == evidence_values[j]))
        if consistency:
            if sample[Query_variable]:
                count[0] += 1
            else:
                count[1] += 1
            num += 1
    count[0] = count[0] / n
    count[1] = count[1] / n
    return count


# calculate the average error
while True:
    print('test sample num: ', sample_num)
    times = 0
    sum_error_p = 0
    sum_error_n = 0
    while times < 10:
        sampling = rejection_sampling(sample_num, query_var, evidence_var, evidence_value)
        error_p = abs(sampling[0] - ground_truth[0]) / ground_truth[0]
        error_n = abs(sampling[1] - ground_truth[1]) / ground_truth[1]
        print('round ', times, 'error_p: ', error_p)
        sum_error_p += error_p
        sum_error_n += error_n
        times += 1
    mean_error_p = sum_error_p / 10
    mean_error_n = sum_error_n / 10
    print('test sample num: ', sample_num, 'mean_error_p: ', mean_error_p)
    print('test sample num: ', sample_num, 'mean_error_n: ', mean_error_n)

    max_error = max(mean_error_p, mean_error_n)
    if max_error > 0.01:
        if max_error >= 0.02:
            sample_num += 5000
        else:
            sample_num += 3000
    else:
        print(sample_num)
        break
