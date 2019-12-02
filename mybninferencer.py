import sys
import exact_infer

bnfile = sys.argv[1]
query_var = sys.argv[2]
evidences = sys.argv[3:]

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
        sys.exit()
    i += 2


bayes_net = exact_infer.BayesNet(bnfile)
print("Method: Exact Inference\n")
print("The distribution of ", query_var, " is: ", exact_infer.enumeration_ask(query_var, evidence_dict, bayes_net))