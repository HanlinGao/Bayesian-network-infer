import os
from xml.etree import ElementTree
import math
import random

'''
A node class, used to record any information about the node, like its name, parents and the CPT.
Besides some methods are included, like set visited or bool value, and calculate the probability
of an occurrence of an event.
'''


class Node:
    # taking in these four variables to initialize a node
    def __init__(self, name, table, parents, property):
        self.name = name
        self.table = []
        self.bool = None  # a variable that will be used to store the boolean assignment from the sampling process
        self.parent = parents  # the list parent is the connection between nodes

        # the full table can be redundancy, take only the probability that the even occurs
        for i in range(len(table)):
            if i % 2 == 0:
                self.table.append(table[i])
        if len(property) == 0:
            self.property = None
        else:
            self.property = property

        # a boolean variable that will used to record if the node is visited for topological sort
        self.visited = False

    # a series of get, set method
    def get_table(self):
        return self.table

    def get_bool(self):
        return self.bool

    def set_bool(self, bool):
        self.bool = bool

    def add_parent(self, node):
        self.parent.append(node)

    def set_visited(self, boolean):
        self.visited = boolean

    def get_visited(self):
        return self.visited

    # a method for getting a probability for an event to occur
    def get_probability(self, bool_list_of_parents=[]):
        if len(self.parent) == 0:
            return self.table[0]
        if len(self.parent) == 1:
            if bool_list_of_parents[0]:
                return self.table[0]
            else:
                return self.table[1]
        if len(self.parent) == 2:
            if bool_list_of_parents[0]:
                if bool_list_of_parents[1]:
                    return self.table[0]
                else:
                    return self.table[1]
            if not bool_list_of_parents[0]:
                if bool_list_of_parents[1]:
                    return self.table[2]
                else:
                    return self.table[3]

    # a display method
    def print_out(self):
        print('Name', self.name)
        print('property', self.property)
        print('parents', self.parent)
        print('table', self.table)


# # the global variables
# variables = []  # a list for storing all variables that obtained from the xml file
# properties = []  # a list for storing properties of all variables that obtained from the xml file
# parents = []  # a list for storing all parents of all variables that obtained from the xml file
# tables = []  # a list for storing all tables of all variables that obtained from the xml file
# sorted_nodes = []  # a list for storing nodes that are in a topological order


# get into an xml file
def access_file(file_name):
    # file_name = file_name
    # full_file = os.path.abspath(os.path.join('data', file_name))
    dom = ElementTree.parse(file_name)
    return dom


# obtain information from the file
def parsing_file(dom):
    variables = []  # a list for storing all variables that obtained from the xml file
    properties = []  # a list for storing properties of all variables that obtained from the xml file
    parents = []  # a list for storing all parents of all variables that obtained from the xml file
    tables = []  # a list for storing all tables of all variables that obtained from the xml file

    variable = dom.findall('NETWORK/VARIABLE/NAME')

    for each in variable:
        variables.append(each.text)
        # print(each.text)
        # table = each.find('TABLE')
        # list = table.text.split()

    property = dom.findall('NETWORK/VARIABLE/PROPERTY')
    for each in property:
        properties.append(each.text.split('= ')[-1])

    parent = dom.findall('NETWORK/DEFINITION/GIVEN')
    for each in parent:
        parents.append(each.text)

    table = dom.findall('NETWORK/DEFINITION/TABLE')
    for each in table:
        t = each.text.split()
        float_table = []
        for each_num in t:
            float_table.append(float(each_num))
        tables.append(float_table)

    return variables, properties, parents, tables


# initialize all the nodes with information got from the file, and by adding parents to build connections, then
# store them into a list
def network_construction(variable_list, property_list, parent_list, table_list):
    list = []

    # from the global list variables, create the nodes one by one
    while len(variable_list) != 0:
        variable = variable_list.pop(0)

        if len(property_list) != 0:
            property = property_list.pop(0)
        else:
            property = []

        tab = table_list.pop(0)

        pare = []
        # the number of parents is not corresponding to variables, but by the number of its CPT, we can know how many
        # parents the node has
        num_of_pare = int(math.log2(len(tab))) - 1
        for i in range(num_of_pare):
            pare.append(parent_list.pop(0))

        node = Node(variable, tab, pare, property)  # initial the node
        list.append(node)   # put it into list
    return list


# using its name to find the node object, for accessing it
def find_node_by_name(network, name):
    for each in network:
        if each.name == name:
            return each


# take in a list of parents` names and return a list of parent node objects
def get_parents(parent_list, network):
    list = []
    for each in parent_list:
        list.append(find_node_by_name(network, each))
    return list


# traversal of the network, and put all explored nodes into that global list, sorted_nodes,
# the early the node gets explored, the index of it in the list smaller
def explore(sorted_nodes, node, network):
    node.visited = True
    parent_list = get_parents(node.parent, network)
    for each in parent_list:
        if not each.get_visited():
            explore(sorted_nodes, each, network)
    sorted_nodes.append(node)

# after explore all the nodes in the network, the nodes are topologically sorted,
# in this order, all the probability of a node is always given the truth of its parents
def topological_sort(network):
    sorted_nodes = []
    for each in network:
        if not each.get_visited():
            explore(sorted_nodes, each, network)

    return sorted_nodes


# taking in a topologically sorted network, flip the network, like flipping a coin, according to the probabilities, the
# value of bool(an attribute of a node object) is set and return a dict with keys of node names and values of their bool
def prior_sampling(sorted_list):
    distribution_dic = dict()

    # flip the nodes one by one
    for each in sorted_list:
        parents_value = []
        parent_nodes = get_parents(each.parent, sorted_list)

        if len(each.parent) == 0:
            probability = each.get_probability()
        else:
            for each_parent in parent_nodes:
                parents_value.append(each_parent.get_bool())
            probability = each.get_probability(parents_value)

        random_num = random.random()    # randomly generate a float from 0 to 1

        # if the random number is smaller than the probability, assign it a true value, or a false
        if random_num < probability:
            each.set_bool(True)
        else:
            each.set_bool(False)
        distribution_dic[each.name] = each.get_bool()
    return distribution_dic


def rejection_sampling(n, file_name, Query_variable, evidence_variables, evidence_values):
    variables, properties, parents, tables = parsing_file(access_file(file_name))
    network = network_construction(variables, properties, parents, tables)
    for each in network:
        each.set_visited(False)
    sorted_nodes = topological_sort(network)
    num = 0
    count = [0, 0]
    while num < n:
        consistency = True
        sample = prior_sampling(sorted_nodes)
        for i in range(len(evidence_variables)):
            consistency = (consistency and (sample[evidence_variables[i]] == evidence_values[i]))
        if consistency:
            if sample[Query_variable]:
                count[0] += 1
            else:
                count[1] += 1
            num += 1
    count[0] = count[0] / n
    count[1] = count[1] / n
    return count
