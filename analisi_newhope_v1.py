import networkx as nx
import matplotlib.pyplot as plt
import json
import random

def build_network_from_json(file_path):
    """
    Costruisce un grafo NetworkX da un file JSON di Moviegalaxies.
    Gli archi sono pesati in base al numero di interazioni.
    """
    # Carica i dati dal file JSON
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Crea un grafo non diretto vuoto
    G = nx.Graph()

    # Estrai i dati della rete
    network_data = data['network']

    # Aggiungi i nodi (personaggi) al grafo
    for node_data in network_data['nodes']:
        character_name = node_data['name']
        G.add_node(character_name)

    # Aggiungi gli archi (interazioni) al grafo
    for edge_data in network_data['edges']:
        source_name = edge_data['source']
        target_name = edge_data['target']
        weight = edge_data['weight']

        # Aggiungiamo l'arco con l'attributo 'weight'
        G.add_edge(source_name, target_name, weight=weight)

    return G

# --- Esecuzione Principale ---
if __name__ == "__main__":
    # Percorso del file JSON
    file_path = 'movie-jsons/new-hope.json'

    # Costruisci la rete per "A New Hope"
    G_anh = build_network_from_json(file_path)

    # Stampa alcune informazioni base
    print("Rete di 'Star Wars: A New Hope' costruita con successo!")
    print(f"Numero di personaggi (nodi): {G_anh.number_of_nodes()}")
    print(f"Numero di interazioni (archi): {G_anh.number_of_edges()}")

    # --- Visualizzazione ---
    plt.figure(figsize=(15, 15))
    pos = nx.spring_layout(G_anh, k=0.5, iterations=50)
    nx.draw(G_anh,
            pos,
            with_labels=True,
            node_color='skyblue',
            node_size=500,
            font_size=8,
            edge_color='gray')
    plt.title("Rete dei Personaggi di 'Star Wars: A New Hope'", size=20)
    plt.savefig('star_wars_newhope_network.png')
    print("\nIl grafico della rete è stato salvato come 'star_wars_newhope_network.png'")

    # --- Analisi di Centralità ---
    print("\n--- Analisi di Centralità ---")

    # Calcolo delle diverse misure di centralità
    degree_centrality = nx.degree_centrality(G_anh)
    betweenness_centrality = nx.betweenness_centrality(G_anh, weight='weight')
    closeness_centrality = nx.closeness_centrality(G_anh, distance='weight')
    try:
        eigenvector_centrality = nx.eigenvector_centrality(G_anh, weight='weight', max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        eigenvector_centrality = {node: 0.0 for node in G_anh.nodes()}
        print("\nAvviso: il calcolo dell'Eigenvector Centrality non è convergente.")
    pagerank = nx.pagerank(G_anh, weight='weight')

    def print_top_centrality(centrality_dict, measure_name, top_n=5):
        """Stampa i top N nodi per una data misura di centralità."""
        print(f"\n--- Top {top_n} Personaggi per {measure_name} ---")
        sorted_centrality = sorted(centrality_dict.items(), key=lambda item: item[1], reverse=True)
        for i in range(min(top_n, len(sorted_centrality))):
            character, value = sorted_centrality[i]
            print(f"{i+1}. {character}: {value:.4f}")

    print_top_centrality(degree_centrality, "Degree Centrality")
    print_top_centrality(betweenness_centrality, "Betweenness Centrality")
    print_top_centrality(closeness_centrality, "Closeness Centrality")
    print_top_centrality(eigenvector_centrality, "Eigenvector Centrality")
    print_top_centrality(pagerank, "PageRank")

    # --- Analisi di Community ---
    print("\n--- Analisi di Community (Metodo Louvain) ---")
    communities = nx.community.louvain_communities(G_anh, weight='weight')
    print(f"Trovate {len(communities)} community principali.")
    for i, community in enumerate(communities):
        sorted_community = sorted(list(community))
        print(f"Community {i+1}: {sorted_community}")
    modularity = nx.community.modularity(G_anh, communities, weight='weight')
    print(f"\nModularità della partizione: {modularity:.4f}")
    node_to_community = {}
    for i, community in enumerate(communities):
        for character in community:
            node_to_community[character] = i

    # --- Visualizzazione con Community ---
    plt.figure(figsize=(18, 18))
    pos = nx.spring_layout(G_anh, k=0.6, iterations=100, seed=42)
    node_colors = [node_to_community.get(node) for node in G_anh.nodes()]
    nx.draw(G_anh, pos, with_labels=True, node_color=node_colors, cmap=plt.cm.Set1, node_size=800, font_size=10, font_color='black', edge_color='lightgray')
    plt.title("Rete dei Personaggi di 'Star Wars: A New Hope' con Community (Louvain)", size=20)
    plt.savefig('star_wars_newhope_network_communities.png')
    print("\nIl grafico della rete con le community è stato salvato come 'star_wars_newhope_network_communities.png'")

    # --- Analisi Proprietà Strutturali ---
    print("\n--- Analisi delle Proprietà Strutturali della Rete ---")
    degree_sequence = [d for n, d in G_anh.degree()]
    print(f"Grado minimo: {min(degree_sequence)}")
    print(f"Grado massimo: {max(degree_sequence)}")
    print(f"Grado medio: {sum(degree_sequence) / G_anh.number_of_nodes():.2f}")
    avg_clustering = nx.average_clustering(G_anh)
    print(f"\nCoefficiente di Clustering Medio: {avg_clustering:.4f}")
    if nx.is_connected(G_anh):
        avg_path_length = nx.average_shortest_path_length(G_anh)
        print(f"La rete è connessa.")
        print(f"Cammino Minimo Medio: {avg_path_length:.4f}")
        G_main_component = G_anh
    else:
        print("La rete non è connessa. Calcolo le proprietà sul Componente Gigante (GCC).")
        giant_component_nodes = max(nx.connected_components(G_anh), key=len)
        G_gcc = G_anh.subgraph(giant_component_nodes)
        print(f"Numero di nodi nel GCC: {G_gcc.number_of_nodes()}")
        avg_path_length_gcc = nx.average_shortest_path_length(G_gcc)
        print(f"Cammino Minimo Medio (nel GCC): {avg_path_length_gcc:.4f}")
        G_main_component = G_gcc

    # --- Analisi dei Percorsi ---
    print("\n--- Analisi dei Percorsi Critici ---")
    try:
        diameter = nx.diameter(G_main_component)
        print(f"Diametro della rete (componente principale): {diameter}")
        print("Esempio di percorso che rappresenta il diametro:")
        for source in G_main_component.nodes():
            for target in G_main_component.nodes():
                if source != target:
                    path = nx.shortest_path(G_main_component, source, target)
                    if len(path) - 1 == diameter:
                        print(f"  {' -> '.join(path)}")
                        raise StopIteration
    except StopIteration:
        pass
    except Exception as e:
        print(f"Impossibile calcolare il diametro: {e}")

    # --- Analisi di Robustezza ---
    print("\n--- Analisi di Robustezza della Rete ---")

    def analyze_robustness(G, removal_strategy='degree'):
        """Simula la rimozione di nodi e traccia la dimensione del componente gigante."""
        G_copy = G.copy()
        if removal_strategy == 'degree':
            nodes_to_remove = [n for n, d in sorted(G_copy.degree(), key=lambda x: x[1], reverse=True)]
        elif removal_strategy == 'betweenness':
            centrality = nx.betweenness_centrality(G_copy, weight='weight')
            nodes_to_remove = [n for n, c in sorted(centrality.items(), key=lambda x: x[1], reverse=True)]
        else:  # 'random'
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

    robustness_targeted = analyze_robustness(G_anh, removal_strategy='degree')
    robustness_random = analyze_robustness(G_anh, removal_strategy='random')

    plt.figure(figsize=(12, 7))
    plt.plot(robustness_targeted, marker='o', linestyle='--', label='Attacco Mirato (per Grado)')
    plt.plot(robustness_random, marker='x', linestyle=':', label='Fallimento Casuale')
    plt.xlabel("Numero di Nodi Rimossi")
    plt.ylabel("Dimensione del Componente Gigante")
    plt.title("Analisi di Robustezza della Rete")
    plt.grid(True)
    plt.legend()
    plt.savefig('star_wars_newhoperobustness_analysis.png')
    print("\nIl grafico dell'analisi di robustezza è stato salvato come 'star_wars_newhope_robustness_analysis.png'")