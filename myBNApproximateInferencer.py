import sys
import approximate_infer

sample_num = int(sys.argv[1])
bnfile = sys.argv[2]
query_var = sys.argv[3]
evidences = sys.argv[4:]

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
        sys.exit()
    i += 2

print("Method: Rejection Sampling Inference\n")
print("The distribution of ", query_var, " is: ", approximate_infer.rejection_sampling(sample_num, bnfile, query_var,
                                                                                       evidence_var, evidence_value))