import networkx as nx
import osmnx as ox
import random
import matplotlib.pyplot as plt
from CHAlgorithmBase import contraction_hierarchy, ch_query

# Testing example graph against CH variations:-------------------------------------------------------------------------

#online variations:

def run_preprocessing_CH_degree_ordering(G):
    order, edges_added, F = contraction_hierarchy(G, order_type="degree", is_online=True)
    print("Contraction order:", order)
    return order, edges_added


def run_preprocessing_CH_edge_diff(G):
    order, edges_added, F = contraction_hierarchy(G, order_type="edge_diff", is_online=True)
    print("Contraction order:", order)
    return order, edges_added


# Offline variations:


def offline_run_preprocessing_CH_degree_ordering(G):
    order, edges_added, F = contraction_hierarchy(G, order_type="degree", is_online=False)
    print("Contraction order:", order)
    return order, edges_added


def offline_run_preprocessing_CH_edge_diff(G):
    order, edges_added, F = contraction_hierarchy(G, order_type="edge_diff", is_online=False)
    print("Contraction order:", order)
    return order, edges_added


#CH query:
def run_query_CH(G, s, t):
    distance, nodes_explored = ch_query(G, s, t)
    return distance, nodes_explored


#Making graph----------------------------------------------------------------------------------------------------------

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

plt.figure()
pos = nx.spring_layout(G, weight='weight', seed=2)  # shell_layout, planar_layout
nx.draw(G, pos,
        with_labels=True)  # fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]}' for u, v, d in G.edges(data=True)})
plt.savefig("test_example_with_shortcuts")


H = G.copy()

#Online testing:-------------------------------------------------------------------------------------------------------


#EDGE DIFFERENCE CH:


edge_diff_node_order, Ep_shortcuts_added = run_preprocessing_CH_edge_diff(G)
print(f"online Edge diff shortcuts actual: {Ep_shortcuts_added}")
# After pre-processing, edge-diff will have:
Ep_shortcuts_added_test = [(2, 4, 6)]

# Test edge-diff CH preprocessing:
if Ep_shortcuts_added != Ep_shortcuts_added_test:
    print("Error! edge-diff CH preprocessing shorcuts added failed!")
    exit(1)

edge_diff_node_order_test_added = [3, 4]

if edge_diff_node_order[0:2] != edge_diff_node_order_test_added:
    print("Error! edge-diff CH preprocessing node order added failed!")
    exit(1)


edge_diff_distance, edge_diff_CH_nodes_explored = run_query_CH(G, 7, 4)
# After querying, edge-diff will have:
edge_diff_CH_nodes_explored_test = [2, 0, 5, 6]  # other nodes can be explored, many permutations possible
edge_diff_CH_nodes_not_explored_test = [3, 8]

# Test edge-diff CH querying:
none_failed = True
for each_node in edge_diff_CH_nodes_explored_test:
    if each_node not in edge_diff_CH_nodes_explored:
        none_failed = False

for each_node in edge_diff_CH_nodes_not_explored_test:
    if each_node in edge_diff_CH_nodes_explored:
        none_failed = False


if not none_failed: # order should be the same also
    print("Error! online edge-diff CH query nodes explored failed!")
    exit(1)

if edge_diff_distance != 8:
    print("Error! online edge-diff CH query distance failed!")
    exit(1)


#DEGREE CH:
G = H.copy()

degree_node_order, Ep_degree_shortcuts_added = run_preprocessing_CH_degree_ordering(G)
print(f"online degree shortcuts actual: {Ep_degree_shortcuts_added}")
# After pre-processing, edge-diff will have:
Ep_degree_shortcuts_added_test = [(4, 5, 2)]  # only this one
# Test degree CH preprocessing:
if (Ep_degree_shortcuts_added != Ep_degree_shortcuts_added_test): # order should be the same also
    print("Error! degree CH preprocessing shortcuts added failed!", flush=True)
    exit(1)

#degree node order test:

if degree_node_order[0:3] != [8, 7, 6]:
    print("Error! degree CH preprocessing node order added failed!", flush=True)
    exit(1)

if 0 in degree_node_order[0:5]:
    print("Error! degree CH preprocessing node order of nodes not expected near beginning failed!", flush=True)
    exit(1)


degree_distance, degree_CH_nodes_explored = run_query_CH(G, 4,7)  # 7, 4
print("degree nodes explored: ", degree_CH_nodes_explored)

if degree_distance != 8:
    print(degree_distance)
    print("Error! querying CH degree distance failed!", flush=True)
    exit(1)

# After querying, degree CH will have:
degree_CH_nodes_explored_test = [2, 3, 0]
degree_CH_nodes_not_explored_test = [6, 8]

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


#Offline testing:------------------------------------------------------------------------------------------------------


#Edge diff CH:
G = H.copy()

edge_diff_node_order, Ep_edge_diff_shortcuts_added = offline_run_preprocessing_CH_edge_diff(G)
print(f"Offline edge diff shotcuts actual: {Ep_edge_diff_shortcuts_added}")
# degree node order test:
first_nodes = [3, 4, 0]
last_nodes = [2, 5]
for a_node in edge_diff_node_order[0:3]:
    if a_node not in first_nodes:
        print("Error! offline edge_diff CH preprocessing node order near front failed!", flush=True)
        exit(1)
if edge_diff_node_order[-2:] != last_nodes:
    print("Error! offline edge_diff CH preprocessing node order last failed!", flush=True)
    exit(1)

# After pre-processing, edge-diff will have:
Ep_edge_diff_shortcuts_added_test = [(2, 4, 6), (1, 5, 2), (2, 5, 5)]  # based on first 3 nodes' contractions
# Test edge_diff CH preprocessing:
if (Ep_edge_diff_shortcuts_added != Ep_edge_diff_shortcuts_added_test): # order should be the same also
    print("Error! offline edge_diff CH preprocessing shortcuts added failed!", flush=True)
    exit(1)


edge_diff_distance, edge_diff_CH_nodes_explored = run_query_CH(G, 4,7)  # 7, 4
print("edge_diff offline nodes explored: ", edge_diff_CH_nodes_explored)

if edge_diff_distance != 8:
    print(edge_diff_distance)
    print("Error! querying offline CH edge_diff distance failed!", flush=True)
    exit(1)

# After querying, degree CH will have:
edge_diff_CH_nodes_explored_test = [7, 2, 0, 4]
edge_diff_CH_nodes_not_explored_test = [8, 3]

# Test degree CH querying:
none_failed = True
for each_node in edge_diff_CH_nodes_explored_test:
    if each_node not in edge_diff_CH_nodes_explored:
        none_failed = False

for each_node in edge_diff_CH_nodes_not_explored_test:
    if each_node in edge_diff_CH_nodes_explored:
        none_failed = False

if not none_failed:  # order should be the same also
    print("Error! querying offline CH edge_diff nodes explored failed!", flush=True)
    exit(1)

#Degree CH:
G = H.copy()

degree_node_order, Ep_shortcuts_added = offline_run_preprocessing_CH_degree_ordering(G)
print(f" offline Degree shortcuts actual: {Ep_shortcuts_added}")
# After pre-processing, edge-diff will have:
Ep_shortcuts_added_test = [(4, 5, 2), (2, 4, 6), (0, 2, 4)]

# Test edge-diff CH preprocessing:
if Ep_shortcuts_added != Ep_shortcuts_added_test:
    print("Error! offline degree CH preprocessing shortcuts added failed!")
    exit(1)

offline_CH_degree_node_order_expected = [[8], [7, 6], [1, 3], [2, 5, 4], [0]]
total_length = 0
previous_node_length = 0
for ix, node_set in enumerate(offline_CH_degree_node_order_expected):
    previous_node_length = total_length
    total_length += len(node_set)
    found_each_node = True
    for a_node in node_set:
        if a_node not in degree_node_order[previous_node_length: total_length]:
            found_each_node = False

if not found_each_node:
    print("Error! offline degree CH preprocessing node order added failed!")
    exit(1)


degree_distance, degree_CH_nodes_explored = run_query_CH(G, 7, 4)
# After querying, edge-diff will have:
degree_CH_nodes_explored_test = [7, 4, 2, 0]  # other nodes can be explored, many permutations possible
degree_CH_nodes_not_explored_test = [3, 8, 6, 1]  # striclty

# Test edge-diff CH querying:
none_failed = True
for each_node in degree_CH_nodes_explored_test:
    if each_node not in degree_CH_nodes_explored:
        none_failed = False

for each_node in degree_CH_nodes_not_explored_test:
    if each_node in degree_CH_nodes_explored:
        none_failed = False

if not none_failed: # order should be the same also
    print("Error! offline online degree CH query nodes explored failed!")
    exit(1)

if degree_distance != 8:
    print("Error! offline online degree CH query distance failed!")
    exit(1)



