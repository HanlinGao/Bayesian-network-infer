# Bayesian-network-infer
## Introduction
Python implementation of uncertain inference based on Bayesian networks, which is a good start point for AI uncertain knowledge.

Program for creating Bayesian network from given .xml file is included.

Algorithms implemented:
* Inference by enumeration
* Approximate Inference based on Rejection sampling
## Usage
* For inference by enumeration:
  
  Run in the command line in the form of:

        Python <program_name.py> <network_file.xml> <Query_Var> <Evidence1, true/false> <Evidence2, true/false>...

  for example, run mybninferencer.py in the command line as:
  
        Python mybninferencer.py aima-alarm.xml B J true M true
* For Rejection sampling:
  
  Run in the command line in the form of:

        Python <program_name.py> <sample_number> <network.xml> <Query_var> <Evidence1, true/false> <Evidence2, true/false>...
    for example, run in the commadn line as:

        Python myBNApproximateInferencer.py 1000 aima-alarm.xml B J true M true

  
## Author
Hanlin Gao(ishenrygao@gmail.com)

Jinhao Zhang(ggbuliton@gmail.com)

Yue Shang(shangyue9417@hotmail.com)