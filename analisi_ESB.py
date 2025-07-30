import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import json
import random
import matplotlib.patches as mpatches
from networkx.algorithms.community import louvain_communities

MOVIE_TITLE = "Star Wars: The Empire Strikes Back"
JSON_FILE_PATH = "movie-jsons/empire.json"

def build_network_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = nx.Graph()
    network_data = data['network']
    for node_data in network_data['nodes']:
        G.add_node(node_data['name'])
    for edge_data in network_data['edges']:
        G.add_edge(edge_data['source'], edge_data['target'], weight=edge_data['weight'])
    return G

def print_top_centrality(centrality_dict, measure_name, top_n=5):
    print(f"\n--- Top {top_n} Personaggi per {measure_name} ---")
    sorted_centrality = sorted(centrality_dict.items(), key=lambda item: item[1], reverse=True)
    for i in range(min(top_n, len(sorted_centrality))):
        character, value = sorted_centrality[i]
        print(f"{i+1}. {character}: {value:.4f}")
    mean_value = sum(centrality_dict.values()) / len(centrality_dict)
    print(f"Valore medio di {measure_name}: {mean_value:.4f}")

def analyze_robustness(G, removal_strategy='degree'):
    G_copy = G.copy()
    if removal_strategy == 'degree':
        nodes_to_remove = [n for n, d in sorted(G_copy.degree(), key=lambda x: x[1], reverse=True)]
    elif removal_strategy == 'betweenness':
        centrality = nx.betweenness_centrality(G_copy, weight='weight')
        nodes_to_remove = [n for n, c in sorted(centrality.items(), key=lambda x: x[1], reverse=True)]
    else:
        nodes_to_remove = list(G_copy.nodes())
        random.shuffle(nodes_to_remove)

    gcc_sizes = []
    if nx.is_connected(G_copy):
        gcc_sizes.append(G_copy.number_of_nodes())
    else:
        gcc_sizes.append(len(max(nx.connected_components(G_copy), key=len)))

    for node in nodes_to_remove[:-1]:
        G_copy.remove_node(node)
        if G_copy.number_of_nodes() > 0:
            if nx.is_connected(G_copy):
                gcc_sizes.append(G_copy.number_of_nodes())
            else:
                gcc_sizes.append(len(max(nx.connected_components(G_copy), key=len)))
        else:
            gcc_sizes.append(0)
    return gcc_sizes

# --- Esecuzione Principale ---
if __name__ == "__main__":
    G_anh = build_network_from_json(JSON_FILE_PATH)

    print(f"Rete di '{MOVIE_TITLE}' costruita con successo!")
    print(f"Numero di personaggi (nodi): {G_anh.number_of_nodes()}")
    print(f"Numero di interazioni (archi): {G_anh.number_of_edges()}")

    # --- Visualizzazione semplice ---
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G_anh, k=0.5, iterations=50, seed=42)
    nx.draw(G_anh, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=8, edge_color='gray')
    plt.title(f"Rete dei Personaggi di '{MOVIE_TITLE}'", size=20)
    file_name = f"{MOVIE_TITLE}_network.png"
    plt.savefig(file_name)
    print(f"\nGrafico salvato in {file_name}")

    # --- Centralità ---
    print("\n--- Analisi di Centralità ---")
    degree_centrality = nx.degree_centrality(G_anh)
    betweenness_centrality = nx.betweenness_centrality(G_anh, weight='weight')
    closeness_centrality = nx.closeness_centrality(G_anh, distance='weight')
    try:
        eigenvector_centrality = nx.eigenvector_centrality(G_anh, weight='weight', max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        eigenvector_centrality = {node: 0.0 for node in G_anh.nodes()}
        print("Avviso: il calcolo dell'Eigenvector Centrality non è convergente.")
    pagerank = nx.pagerank(G_anh, weight='weight')

    print_top_centrality(degree_centrality, "Degree Centrality")
    print_top_centrality(betweenness_centrality, "Betweenness Centrality")
    print_top_centrality(closeness_centrality, "Closeness Centrality")
    print_top_centrality(eigenvector_centrality, "Eigenvector Centrality")
    print_top_centrality(pagerank, "PageRank")

    # Salva le centralità in CSV
    centralities_df = pd.DataFrame({
        'Character': list(G_anh.nodes()),
        'Degree': [degree_centrality.get(n, 0) for n in G_anh.nodes()],
        'Betweenness': [betweenness_centrality.get(n, 0) for n in G_anh.nodes()],
        'Closeness': [closeness_centrality.get(n, 0) for n in G_anh.nodes()],
        'Eigenvector': [eigenvector_centrality.get(n, 0) for n in G_anh.nodes()],
        'PageRank': [pagerank.get(n, 0) for n in G_anh.nodes()],
    })
    file_name_csv = f"centralities_{MOVIE_TITLE}.csv"
    centralities_df.to_csv(file_name_csv, index=False)
    print(f"\nDati di centralità salvati in {file_name_csv}")

    # --- Community (Louvain) ---
    print("\n--- Analisi di Community (Metodo Louvain) ---")
    communities = louvain_communities(G_anh, weight='weight')
    print(f"Trovate {len(communities)} community.")
    for i, community in enumerate(communities):
        print(f"Community {i+1}: {sorted(list(community))}")
    modularity = nx.community.modularity(G_anh, communities, weight='weight')
    print(f"Modularità della partizione: {modularity:.4f}")

    node_to_community = {}
    for i, community in enumerate(communities):
        for character in community:
            node_to_community[character] = i

    # --- Visualizzazione con community ---
    plt.figure(figsize=(18, 18))
    pos = nx.spring_layout(G_anh, k=0.6, iterations=100, seed=42)
    node_colors = [node_to_community.get(node) for node in G_anh.nodes()]
    nx.draw(G_anh, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Set1,
            node_size=800, font_size=10, edge_color='lightgray')
    plt.title("Rete con Community (Louvain)", size=20)

    handles = [mpatches.Patch(color=plt.cm.Set1(i / len(communities)), label=f"Community {i+1}") for i in range(len(communities))]
    plt.legend(handles=handles, loc='best')
    file_name_comm = f"{MOVIE_TITLE}_network_communities.png"
    plt.savefig(file_name_comm)
    print(f"\nGrafico salvato in {file_name_comm}")

    # --- Proprietà strutturali ---
    print("\n--- Analisi delle Proprietà Strutturali ---")
    degree_sequence = [d for _, d in G_anh.degree()]
    print(f"Grado minimo: {min(degree_sequence)}")
    print(f"Grado massimo: {max(degree_sequence)}")
    print(f"Grado medio: {sum(degree_sequence) / len(degree_sequence):.2f}")
    avg_clustering = nx.average_clustering(G_anh)
    print(f"Clustering medio: {avg_clustering:.4f}")

    if nx.is_connected(G_anh):
        avg_path_length = nx.average_shortest_path_length(G_anh)
        print("La rete è connessa.")
        print(f"Cammino minimo medio: {avg_path_length:.4f}")
        G_main_component = G_anh
    else:
        print("Rete non connessa. Calcolo sul GCC.")
        giant_nodes = max(nx.connected_components(G_anh), key=len)
        G_main_component = G_anh.subgraph(giant_nodes)
        avg_path_length = nx.average_shortest_path_length(G_main_component)
        print(f"Cammino minimo medio (GCC): {avg_path_length:.4f}")

    # --- Diametro e percorso massimo ---
    print("\n--- Analisi Diametro ---")
    try:
        diameter = nx.diameter(G_main_component)
        print(f"Diametro: {diameter}")
        for source in G_main_component.nodes():
            for target in G_main_component.nodes():
                if source != target:
                    path = nx.shortest_path(G_main_component, source, target)
                    if len(path) - 1 == diameter:
                        print(f"Esempio di percorso massimo: {' -> '.join(path)}")
                        raise StopIteration
    except StopIteration:
        pass

    # --- Robustezza ---
    print("\n--- Analisi di Robustezza ---")
    robustness_targeted = analyze_robustness(G_anh, removal_strategy='degree')
    robustness_random = analyze_robustness(G_anh, removal_strategy='random')

    plt.figure(figsize=(12, 7))
    plt.plot(robustness_targeted, marker='o', linestyle='--', label='Attacco Mirato (Grado)')
    plt.plot(robustness_random, marker='x', linestyle=':', label='Errore Casuale')
    plt.xlabel("Nodi Rimossi")
    plt.ylabel("Dimensione GCC")
    plt.title("Robustezza della Rete")
    plt.grid(True)
    plt.legend()
    file_name_robust = f"{MOVIE_TITLE}_robustness_analysis.png"
    plt.savefig(file_name_robust)
    print(f"Grafico salvato in {file_name_robust}")

    print("\nAnalisi terminata.")
