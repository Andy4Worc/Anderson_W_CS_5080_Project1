import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from CHAlgorithmBase import contraction_hierarchy, ch_query
import random

def pick_random_node(G):
    return random.choice(list(G.nodes))

# Define the city name and the type of network
city_name = "Falcon, Colorado, USA"
network_type = "drive"  # Other options: "walk", "bike", "all"

# Download the road network for the specified city
G = ox.graph_from_place(city_name, network_type=network_type)

# Simplify the graph to remove self-loops and parallel edges
# G = ox.simplify_graph(G)

# Get the number of nodes in the graph
num_nodes = len(G.nodes)
print(type(G))
# Print the number of nodes and edges
print(f"The graph has {num_nodes} nodes and {len(G.edges)} edges.")

# Plot the graph
interesting_node_1 = 2002513654 #6408309267
interesting_node_2 = 10848375497 #6408309256
#shortest path should be 10, but ch query found 11: 55787600, 10848375491) and pair (557698839, 10848387314)
#and pair: (1024562158, 10848375497)
node_1_data = interesting_node_1
node_2_data = interesting_node_2

node_colors = []
for node in G.nodes:
    #print(node)
    if node == node_1_data:
        print("Something red")
        node_colors.append('red')  # Color the highlighted node in red
    elif node == node_2_data:
        node_colors.append('orange')
    else:
        node_colors.append('blue')
node_sizes = [100 if (node == node_1_data) or (node == node_2_data) else 10 for node in G.nodes]

#fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')

fig, ax = ox.plot_graph(G, node_color=node_colors, node_size=node_sizes, edge_linewidth=1, bgcolor='k')  # show=False)
#ax.scatter(*G.nodes[highlight_node]['x'], *G.nodes[highlight_node]['y'], s=200, c='red', zorder=5)

# Show the plot
plt.show()

# Check if the graph has around 10,000 nodes
print(f"Num of nodes: {num_nodes}")


G = G.to_undirected()
self_loops = list(nx.selfloop_edges(G))
print(self_loops)
G.remove_edges_from(self_loops)
"""
plt.figure()
pos = nx.spring_layout(G, weight='weight', seed=2)  # shell_layout, planar_layout
nx.draw(G, pos,
        with_labels=True)  # fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]}' for u, v, d in G.edges(data=True)})
plt.savefig("no_shortcuts_Falcon")
"""
print(f"Num of edges pre contraction: {G.number_of_edges()}")
order, edges_added = contraction_hierarchy(G)
print(f"Num of edges pre contraction: {G.number_of_edges()}")
print("Contraction order:", order)

# At this point, G has been contracted and contains any shortcut edges added.

#55740867, 55741498

# fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')
fig, ax = ox.plot_graph(G, node_color=node_colors, node_size=node_sizes, edge_linewidth=1, bgcolor='k')
# Run the CH query.

for _ in range(40):
    source = pick_random_node(G)  # 10848375497
    target = 10848375497
    distance, explored_nodes = ch_query(G, source, target)
    # print(f"Shortest distance from {source} to {target}: {distance}")
    # print("Explored nodes: ", explored_nodes)
    verification = nx.shortest_path_length(G, source=source, target=target, weight='weight')
    if verification != distance:
        print(f"ch query returned: {distance}, but built-in shortest path was: {verification}")
        print(f"For: source: {source}, target: {target}")
        print()

"""
plt.figure()
pos = nx.spring_layout(G, weight='weight', seed=2)  # shell_layout, planar_layout
nx.draw(G, pos,
        with_labels=True)  # fig, ax = ox.plot_graph(G, node_size=10, edge_linewidth=1, bgcolor='k', node_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{d["weight"]}' for u, v, d in G.edges(data=True)})
plt.savefig("Falcon_with_shortcuts")
"""


