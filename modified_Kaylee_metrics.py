import osmnx as ox
import networkx as nx
import time
import tracemalloc  # For detailed memory usage
import pandas as pd
from CHAlgorithmBase import contraction_hierarchy, ch_query
from TNRAlgorithmExtension import TransitNodeRouting

import random

#Original Code from Kaylee who got it from Faezeh
#Modified and final version by Andy Worcester

def main_metrics(G, s_t_pairs):
    # Start measuring overall memory usage
    H = G.copy()

    tracemalloc.start()

    # ✅ Store results for comparison
    results = []

    # ✅ Define the 4 correct ordering criteria
    CH_order_types = ["degree", "edge_diff"]
    CH_is_online = [False, True]


    #This section is for the project deliverables 1 and 2:
    for order_type in CH_order_types:
        for is_online in CH_is_online:
            print()
            print(f"Starting TNR and CH variation with order type: {order_type} and if is online: {is_online}")

            G = H.copy()
            results.append(run_tests_CH(G, s_t_pairs, is_online, order_type))
            G = H.copy()
            results.append(run_tests_TNR(G, s_t_pairs, is_online, order_type))

    #Out of curiosity, this is an extended piece:
    for k in [2, 8, 25, 50, 100, 250]: #Falcon max is over 500 nodes
        print()
        print(f"Starting TNR extended tests with k value: {k}")
        G = H.copy()

        results.append(run_extended_TNR_tests(G, s_t_pairs, k))

    save_results(results)


def run_tests_CH(G, s_t_pairs, is_online, order_type):
    # **Measure Preprocessing Time and Memory Usage**
    tracemalloc.reset_peak()
    start_preprocess = time.perf_counter()

    order, edges_added, F = contraction_hierarchy(G, order_type=order_type, is_online=is_online)

    end_preprocess = time.perf_counter()
    current_mem_pre, peak_mem_pre = tracemalloc.get_traced_memory()

    preprocessing_time = end_preprocess - start_preprocess
    preprocessing_memory = peak_mem_pre / 1024 / 1024

    print(f"✅ Preprocessing Completed in: {preprocessing_time:.4f} sec, Memory: {preprocessing_memory:.2f} MB")

    all_query_times = []
    all_query_mems = []
    all_query_lengths = []

    for source, target in s_t_pairs:
        # **Measure Query Time and Memory Usage**
        tracemalloc.reset_peak()
        start_query = time.perf_counter()

        # ✅ Use bidirectional Dijkstra on the CH Graph
        path_length, shortest_path = ch_query(G, source, target)

        end_query = time.perf_counter()
        current_mem_query, peak_mem_query = tracemalloc.get_traced_memory()
        query_time = end_query - start_query
        query_memory = peak_mem_query / 1024 / 1024
        all_query_times.append(query_time)
        all_query_mems.append(query_memory)
        all_query_lengths.append(path_length)

    avg_query_time = sum(all_query_times) / len(all_query_times)
    avg_query_memory = sum(all_query_mems) / len(all_query_mems)
    avg_query_lengths = sum(all_query_lengths) / len(all_query_lengths)
    print(f"✅ Queries Completed. Avg time: {avg_query_time:.4f} sec, Avg Path Length: {avg_query_lengths:.2f}, Avg Memory: {avg_query_memory:.2f} MB")

    # ✅ Store the results for comparison
    if is_online:
        ordering_name = order_type + "_CH_ordering_ONLINE"
    else:
        ordering_name = order_type + "_CH_ordering_OFFLINE"
    results = [ordering_name, preprocessing_time, preprocessing_memory, avg_query_time, avg_query_lengths, avg_query_memory]

    return results


def run_tests_TNR(G, s_t_pairs, is_online, order_type):
    # **Measure Preprocessing Time and Memory Usage**
    tracemalloc.reset_peak()
    start_preprocess = time.perf_counter()

    order, edges_added, F = contraction_hierarchy(G, order_type=order_type, is_online=is_online)

    k = 30  # for example
    tnr = TransitNodeRouting(F, k)
    tnr.setup_transit_nodes_and_D()  # Select transit nodes and compute table D.

    # Compute candidate access nodes (forward and backward) and record search spaces.
    tnr.compute_access_nodes_forward()

    # Prune the candidate access nodes.
    tnr.prune_access_nodes()

    end_preprocess = time.perf_counter()
    current_mem_pre, peak_mem_pre = tracemalloc.get_traced_memory()

    preprocessing_time = end_preprocess - start_preprocess
    preprocessing_memory = peak_mem_pre / 1024 / 1024

    print(f"✅ Preprocessing Completed in: {preprocessing_time:.4f} sec, Memory: {preprocessing_memory:.2f} MB")

    all_query_times = []
    all_query_mems = []
    all_query_lengths = []

    for source, target in s_t_pairs:
        # **Measure Query Time and Memory Usage**
        tracemalloc.reset_peak()
        start_query = time.perf_counter()

        # ✅ do query on the graph:
        path_length = tnr.query(source, target)

        end_query = time.perf_counter()
        current_mem_query, peak_mem_query = tracemalloc.get_traced_memory()
        query_time = end_query - start_query
        query_memory = peak_mem_query / 1024 / 1024
        all_query_times.append(query_time)
        all_query_mems.append(query_memory)
        all_query_lengths.append(path_length)

    avg_query_time = sum(all_query_times) / len(all_query_times)
    avg_query_memory = sum(all_query_mems) / len(all_query_mems)
    avg_query_lengths = sum(all_query_lengths) / len(all_query_lengths)
    print(f"✅ Queries Completed. Avg time: {avg_query_time:.4f} sec, Avg Path Length: {avg_query_lengths:.2f}, Avg Memory: {avg_query_memory:.2f} MB")

    # ✅ Store the results for comparison
    if is_online:
        ordering_name = order_type + "_TNR_ordering_ONLINE"
    else:
        ordering_name = order_type + "_TNR_ordering_OFFLINE"
    results = [ordering_name, preprocessing_time, preprocessing_memory, avg_query_time, avg_query_lengths, avg_query_memory]

    return results


def run_extended_TNR_tests(G, s_t_pairs, k):
    # **Measure Preprocessing Time and Memory Usage**
    tracemalloc.reset_peak()
    start_preprocess = time.perf_counter()

    order, edges_added, F = contraction_hierarchy(G, order_type="edge_diff", is_online=False)

    tnr = TransitNodeRouting(F, k)
    tnr.setup_transit_nodes_and_D()  # Select transit nodes and compute table D.

    # Compute candidate access nodes (forward and backward) and record search spaces.
    tnr.compute_access_nodes_forward()

    # Prune the candidate access nodes.
    tnr.prune_access_nodes()

    end_preprocess = time.perf_counter()
    current_mem_pre, peak_mem_pre = tracemalloc.get_traced_memory()

    preprocessing_time = end_preprocess - start_preprocess
    preprocessing_memory = peak_mem_pre / 1024 / 1024

    print(f"✅ Preprocessing Completed in: {preprocessing_time:.4f} sec, Memory: {preprocessing_memory:.2f} MB")

    all_query_times = []
    all_query_mems = []
    all_query_lengths = []

    for source, target in s_t_pairs:
        # **Measure Query Time and Memory Usage**
        tracemalloc.reset_peak()
        start_query = time.perf_counter()

        # ✅ do query on the graph:
        path_length = tnr.query(source, target)

        end_query = time.perf_counter()
        current_mem_query, peak_mem_query = tracemalloc.get_traced_memory()
        query_time = end_query - start_query
        query_memory = peak_mem_query / 1024 / 1024
        all_query_times.append(query_time)
        all_query_mems.append(query_memory)
        all_query_lengths.append(path_length)

    avg_query_time = sum(all_query_times) / len(all_query_times)
    avg_query_memory = sum(all_query_mems) / len(all_query_mems)
    avg_query_lengths = sum(all_query_lengths) / len(all_query_lengths)
    print(f"✅ Queries Completed. Avg time: {avg_query_time:.5f} sec, Avg Path Length: {avg_query_lengths:.2f}, Avg Memory: {avg_query_memory:.2f} MB")

    # ✅ Store the results for comparison

    ordering_name = "TNR_extended_tests_k=" + str(k)

    results = [ordering_name, preprocessing_time, preprocessing_memory, avg_query_time, avg_query_lengths, avg_query_memory]

    return results


def save_results(results):
    # **Measure Total Memory Usage**
    current_mem_total, peak_mem_total = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"\n**Total Peak Memory Usage:** {peak_mem_total / 1024 / 1024:.2f} MB")

    # ✅ Display Results as a Table
    df_results = pd.DataFrame(results, columns=["Ordering Method", "Preprocessing Time (s)", "Preprocessing Memory (MB)",
                                       "Query Time (s)", "Path Length", "Query Memory (MB)"])

    # ✅ Print Full Table Without Truncation
    print("\n🔹 CH and TNR Ordering Comparison Results:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 800)
    print(df_results)

    # ✅ Save Results to a CSV File
    df_results.to_csv("CH_TNR_results.csv", index=False)
    print("\n✅ Results saved as 'CH_TNR_results.csv'. Open it to view all columns.")