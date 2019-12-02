from xml.etree import ElementTree as ET
import copy


# Initial parse to get the network root in xml file
def xml_parse_net(file):
    tree = ET.parse(file)
    root = tree.getroot()
    net = root[0]
    return net  # Return the network in xml form


# A Basic Bayesian net node
class BayesNode(object):
    def __init__(self, nd):
        self.label = None  # Name of the node
        self.given = []    # Given Variable
        self.parent = []   # Connected Based on parent nodes
        self.table = []    # Get the probability table
        self.bool = None   # Record the boolean value for children to use (used in determine the probability)
        self.set_all(nd)   # When instantiate, set all attributes of a node

    # To add parent node for the current node
    def add_parent(self, new_node):
        self.parent.append(new_node)

    # Set label and values based on FOR element in xml
    def set_label(self, nd):
        temp = nd.find("FOR")
        self.label = temp.text

    # Set given variables based on GIVEN elements in xml
    def set_given(self, nd):
        given = nd.findall("GIVEN")
        for e in given:
            self.given.append(e.text)

    # Set the table based on TABLE element in xml
    def set_table(self, nd):
        temp = nd.find("TABLE")
        table = temp.text.split()
        for i in range(len(table)):
            if i % 2 == 0:
                self.table.append(float(table[i]))

    # Set all attributes
    def set_all(self, nd):
        self.set_label(nd)
        self.set_given(nd)
        self.set_table(nd)


# connect all the Bayesian nodes in a network
class BayesNet(object):
    def __init__(self, file):
        self.root = xml_parse_net(file)  # the root in xml form
        self.nodes = self.get_all_node()  # Nodes are objects of BayesNode
        self.build_network()  # When instantiate, form the Bayesian network graph
        self.variable = self.get_all_variable()

    # Get all nodes in xml (return a list of BayesNode objects)
    def get_all_node(self):
        nodes = []
        defines = self.root.findall("DEFINITION")
        for d in defines:
            nd = BayesNode(d)
            nodes.append(nd)
        return nodes

    # Build the network (nodes connect with each other with parent attribute)
    def build_network(self):
        for n in self.nodes:
            if n.given:
                for nd in self.nodes:
                    # if the given variable match a node's name, you find the parent node
                    if nd.label in n.given:
                        n.add_parent(nd)

    # Find all variables in xml and make them topological sorted
    def get_all_variable(self):
        var = []
        net = self.nodes
        sorted_net = topological_sort(net)
        for v in sorted_net:
            var.append(v.label)
        return var


# topological sorting method
def topological_sort(net):
    visited = []
    sorted_list = []
    for each in net:
        if each not in visited:
            explore(each, net, visited, sorted_list)
    return sorted_list


# DFS for topological sorting
def explore(v, net, visited, sorted_list):
    visited.append(v)
    u = v.parent
    for each in u:
        if each not in visited:
            explore(each, net, visited, sorted_list)
    sorted_list.append(v)


# Normalize the distribution
def normalize(db):
    total = 0
    new_db = []
    for num in db:
        total += num
    for num in db:
        new_db.append((num * 1.0) / total)
    return new_db


# The enumeration algorithm for answering queries on Bayesian networks
def enumeration_ask(query, e, bn):
    ex = e                      # Dictionary for recording the evidence and values
    queue = []                  # A distribution over query variable, initial empty
    query_tf = [True, False]    # query boolean values
    for x in query_tf:
        # extend e with query = true or false
        ex[query] = x
        queue.append(enumeration_all(bn.variable, ex, bn))
    return normalize(queue)     # Return the distribution


# Enumeration all the values given query variable's value
def enumeration_all(variables, e, net):
    # Initialize the nodes' bool value for following operation (For probability using)
    keys = e.keys()
    for key in keys:
        key_node = find_node(key, net)
        key_node.bool = e[key]

    # Main code
    if not variables:
        return 1.0      # float
    variables_copy = copy.deepcopy(variables)
    y = variables_copy.pop(0)

    # if current variable is in evidence
    if y in keys:
        # Get the probability of current variable
        return probability(y, e, net) * enumeration_all(variables_copy, e, net)
    else:
        ey1 = copy.deepcopy(e)
        ey2 = copy.deepcopy(e)
        ey1[y] = True
        ey2[y] = False
        # Get the summation probability of current and posterior variable
        return (probability(y, ey1, net) * enumeration_all(variables_copy, ey1, net)) \
               + (probability(y, ey2, net) * enumeration_all(variables_copy, ey2, net))


# Find a node based on its name
def find_node(label, net):
    for nod in net.nodes:
        if nod.label == label:
            return nod


# Get the probability of the variable given evidence
def probability(variable, e, net):
    # Initial probability
    pb = None
    # Get the boolean value of current variable
    tf = e[variable]
    nod = find_node(variable, net)

    # Different methods for different parents number
    if not nod.parent:
        pb = nod.table[0]
    elif len(nod.parent) == 1:
        if nod.parent[0].bool is True:
            pb = nod.table[0]
        else:
            pb = nod.table[1]
    elif len(nod.parent) == 2:
        if nod.parent[0].bool is True:
            if nod.parent[1].bool is True:
                pb = nod.table[0]
            else:
                pb = nod.table[1]
        elif nod.parent[0].bool is False:
            if nod.parent[1].bool is True:
                pb = nod.table[2]
            else:
                pb = nod.table[3]

    # Return the value based on the value of current variable
    if tf is True:
        return pb
    else:
        return 1.0 - pb


# bayes_net = BayesNet("aima-alarm.xml")
# print(enumeration_ask("B", {"J": True, "M": True}, bayes_net))
