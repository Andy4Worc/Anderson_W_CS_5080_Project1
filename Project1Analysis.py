import osmnx as ox
import networkx as nx
import scipy as sp
import matplotlib.pyplot as plt
from CHAlgorithmBase import contraction_hierarchy, ch_query
import random
from TNRAlgorithmExtension import TransitNodeRouting
from modified_Kaylee_metrics import main_metrics

def pick_random_node(G):
    return random.choice(list(G.nodes))

def get_random_source_and_targets(G, seed=42):
    source_target_pairs = []
    random.seed(seed)
    for _ in range(100):
        source = pick_random_node(G)
        target = pick_random_node(G)
        source_target_pairs.append( (source, target) )
    return source_target_pairs

def get_graph_from_city():
    # Define the city name and the type of network
    city_name = "Falcon, Colorado, USA"
    network_type = "drive"  # Other options: "walk", "bike", "all"

    # Download the road network for the specified city
    G = ox.graph_from_place(city_name, network_type=network_type)

    # Get the number of nodes in the graph
    num_nodes = len(G.nodes)
    # Print the number of nodes and edges
    print(f"The graph has {num_nodes} nodes and {len(G.edges)} edges.")

    # Plot the graph

    #Another style of a plot:
    #fig, ax = ox.plot_graph(G, node_size=[10] * len(list(G.nodes)), edge_linewidth=1, bgcolor='k')
    #plt.savefig("no_shortcuts_Falcon_osmnx")

    G = G.to_undirected()
    self_loops = list(nx.selfloop_edges(G))
    G.remove_edges_from(self_loops)


    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    # Draw the graph preserving the geographic layout
    fig, ax = plt.subplots(figsize=(12, 12),)
    nx.draw(G, pos=pos, node_size=10, edge_color='lightgray') # with_labels=True

    # If you want to add edge labels:
    #edge_labels = {}
    #for u, v, data in G.edges(data=True): #key, data
    #    edge_labels[(u, v)] = int(data.get("travel_time", data.get("length", 1))/5) + 1
    # nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, font_size=5)

    plt.title("Falcon without shortcuts")
    plt.axis("equal")  # This helps preserve the aspect ratio
    plt.savefig("no_shortcuts_Falcon", bbox_inches="tight", dpi=1200)
    plt.close()

    # Change weights to be "travel_time" based:
    for u, v, data in G.edges(data=True):
        data["weight"] = int(data.get("travel_time", data.get("length", 1))/5) + 1

    return G



def no_metrics_correctness_analysis(H):
    CH_order_types = ["degree", "edge_diff"]
    CH_is_online = [False, True]


    # start of metric analysis:

    for order_type in CH_order_types:
        for is_online in CH_is_online:
            print(f"Starting CH variation with order type: {order_type} and if is online: {is_online}")
            print()

            G = H.copy()

            print(f"Num of edges pre contraction: {G.number_of_edges()}")
            print("Starting CH pre-processing...")
            print()
            order, edges_added, F = contraction_hierarchy(G, order_type=order_type, is_online=is_online)
            print(f"Num of edges post contraction: {G.number_of_edges()}")
            print("Contraction order:", order)
            print()
            # At this point, G has been contracted and contains any shortcut edges added.

            # Run the CH query.
            for _ in range(100):
                source = pick_random_node(G)  # 10848375497
                target = pick_random_node(G) # 10848375497
                distance, explored_nodes = ch_query(G, source, target)
                # print(f"Shortest distance from {source} to {target}: {distance}")
                # print("Explored nodes: ", explored_nodes)
                verification = nx.shortest_path_length(G, source=source, target=target, weight='weight')
                if verification != distance:
                    print(f"ERROR! ch query returned: {distance}, but built-in shortest path was: {verification}")
                    print(f"For: source: {source}, target: {target}")
                    print()
                    exit(1)

            print()
            print()
            print("TNR pre-processing:")

            k = 20  # for example
            tnr = TransitNodeRouting(F, k)
            tnr.setup_transit_nodes_and_D()   # Select transit nodes and compute table D.

            # Compute candidate access nodes (forward and backward) and record search spaces.
            tnr.compute_access_nodes_forward()
            # tnr.compute_access_nodes_backward()

            # Prune the candidate access nodes.
            tnr.prune_access_nodes()

            # Run a query:
            for _ in range(100):
                source = pick_random_node(F)  # 10848375497
                target = pick_random_node(F) # 10848375497
                distance = tnr.query(source, target)
                distance_check, _ = nx.bidirectional_dijkstra(F, source, target)
                if distance != distance_check:
                    print(f"ERROR on TNR! Dist: {distance}, check {distance_check}")
                    exit(1)

            plt.figure()
            pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

            # Draw the graph preserving the geographic layout
            fig, ax = plt.subplots(figsize=(12, 12), )
            nx.draw(G, pos=pos, node_size=10, edge_color='lightgray')  # with_labels=True

            plt.title("Falcon without shortcuts")
            plt.axis("equal")  # This helps preserve the aspect ratio
            plt.savefig("Falcon_shortcuts_CH_" + order_type + "_is_online_" + str(is_online), bbox_inches="tight", dpi=1200)
            plt.close()



G = get_graph_from_city()
H = G.copy()
source_target_pairs = get_random_source_and_targets(G)
print(source_target_pairs)
no_metrics_correctness_analysis(H) # can comment out to just go to metrics
print()
print("Finished testing CH and TNR algorithms for ensuring they are error-free")
print()
print("Now running proper metrics")
G = H.copy()
main_metrics(G, source_target_pairs)

