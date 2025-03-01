import networkx as nx
import osmnx as ox
import random
import matplotlib.pyplot as plt
from CHAlgorithmBase import contraction_hierarchy, ch_query

# Create a MultiDiGraph
G = nx.MultiDiGraph()
G = G.to_undirected()
# Add 10 nodes to the graph
for i in range(9):
    G.add_node(i)

# A big difference between rank by degree and edge difference is shown by a graph that has a node with a lot of edges, but each of the nodes it connects to are already connected via shortest-path
G.add_edge(0, 1, weight=1)
G.add_edge(0, 2, weight=5)
G.add_edge(0, 3, weight=5)
G.add_edge(0, 4, weight=5)
G.add_edge(0, 5, weight=1)

G.add_edge(1, 2, weight=3)
G.add_edge(2, 3, weight=3)
G.add_edge(3, 4, weight=3)
G.add_edge(4, 5, weight=3)
G.add_edge(5, 1, weight=3)

G.add_edge(4, 6, weight=1)
G.add_edge(5, 6, weight=1)

G.add_edge(2, 7, weight=2)
G.add_edge(7, 8, weight=1)

num_edges = G.number_of_edges()

# save example graph used for testing:
pos = nx.spring_layout(G, weight='weight', seed=1) #shell_layout, planar_layout
nx.draw(G, pos, with_labels=True) #fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]}' for u, v, d in G.edges(data=True)})
plt.savefig("example Graph")




# Testing example graph against algorithms:



def run_preprocessing_CH_degree_ordering(G):
    order, edges_added, F = contraction_hierarchy(G)
    print("Contraction order:", order)

    return order, edges_added


def run_query_CH_degree_ordering(G, s, t):
    print("pre ordering")
    distance, nodes_explored = ch_query(G, s, t)
    print("post ordering")
    return distance, nodes_explored

def run_preprocessing_CH_edge_diff(G):
    edges_added = []
    return edges_added

def run_query_CH_edge_diff(G, Ep_shortcuts_added):
    nodes_explored = []
    return nodes_explored


"""
Ep_shortcuts_added = run_preprocessing_CH_edge_diff(G)
# After pre-processing, edge-diff will have:
Ep_shortcuts_added_test = [(1, 5, 2)]  # (4, 5, 2) is optional (S, T, weight)
choose_one_Ep_shortcuts_added_test = [(2, 5, 5), (1, 3, 6), (2, 4, 6)]
# Test edge-diff CH preprocessing:
if (4, 5, 2) in Ep_shortcuts_added:
    Ep_shortcuts_added.remove((4, 5, 2))


one_is_true = False
for edge in choose_one_Ep_shortcuts_added_test:
    possible_result = []
    possible_result.append(Ep_shortcuts_added_test[0])
    possible_result.append(edge)
    edges_match = True
    for test_edge in possible_result:
        if test_edge not in Ep_shortcuts_added:
            edges_match = False
    if (len(possible_result) == len(Ep_shortcuts_added) and edges_match): # order should be the same also
        one_is_true = True

if not one_is_true:
    print("Error! edge-diff CH preprocessing failed!")
    exit(1)

edge_diff_CH_nodes_explored = run_query_CH_edge_diff(G, Ep_shortcuts_added)
# After querying, edge-diff will have:
edge_diff_CH_nodes_explored_test = [2, 3]  # other nodes can be explored, many permutations possible
edge_diff_CH_nodes_not_explored_test = [0]  # striclty

# Test edge-diff CH querying:
none_failed = True
for each_node in edge_diff_CH_nodes_explored_test:
    if each_node not in edge_diff_CH_nodes_explored:
        none_failed = False

for each_node in edge_diff_CH_nodes_not_explored_test:
    if each_node in edge_diff_CH_nodes_explored:
        none_failed = False


if not none_failed: # order should be the same also
    print("Error! edge-diff CH preprocessing failed!")
    exit(1)

"""

# Now degree testing:
degree_node_order, Ep_degree_shortcuts_added = run_preprocessing_CH_degree_ordering(G)
# After pre-processing, edge-diff will have:
Ep_degree_shortcuts_added_test = [(4, 5, 2)]  # always only this one
# Test degree CH preprocessing:
print("hello: ", Ep_degree_shortcuts_added)
if (Ep_degree_shortcuts_added != Ep_degree_shortcuts_added_test): # order should be the same also
    print("Error! degree CH preprocessing shortcuts added failed!", flush=True)
    exit(1)

degree_distance, degree_CH_nodes_explored = run_query_CH_degree_ordering(G, 4,7)  # 7, 4
print("degree nodes explored: ", degree_CH_nodes_explored)

if degree_distance != 8:
    print(degree_distance)
    print("Error! querying CH degree distance failed!", flush=True)
    exit(1)

# After querying, degree CH will have:
degree_CH_nodes_explored_test = [2, 3, 0]
degree_CH_nodes_not_explored_test = [6]

# Test degree CH querying:
none_failed = True
for each_node in degree_CH_nodes_explored_test:
    if each_node not in degree_CH_nodes_explored:
        none_failed = False

for each_node in degree_CH_nodes_not_explored_test:
    if each_node in degree_CH_nodes_explored:
        none_failed = False

if not none_failed:  # order should be the same also
    print("Error! querying CH degree nodes explored failed!", flush=True)
    exit(1)


all_edges = list(G.edges(4, data=True))
print("Edges associated with node 4:")
for edge in all_edges:
    print(edge)

plt.figure()
pos = nx.spring_layout(G, weight='weight', seed=2)  # shell_layout, planar_layout
nx.draw(G, pos,
        with_labels=True)  # fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]}' for u, v, d in G.edges(data=True)})
plt.savefig("test_example_with_shortcuts")
