# Star Wars Network Analysis

This repository contains Python scripts to analyze the character interaction networks of the original Star Wars trilogy. Each script focuses on one movie, performs a series of network analyses, and saves the results as graphs and data files.

## Scripts

- `analisi_newhope_v2.py`: Analyzes the character interaction network of *Star Wars: Episode IV – A New Hope*.
- `analisi_empire_v1.py`: Analyzes the character interaction network of *Star Wars: Episode V – The Empire Strikes Back*.
- `analisi_jedi_v1.py`: Analyzes the character interaction network of *Star Wars: Episode VI – Return of the Jedi*.

## Features

Each script performs the following analyses:

- **Network Construction**: Builds a NetworkX graph from a JSON file containing character interactions.
- **Centrality Analysis**: Calculates and prints the top 5 characters for the following centrality measures:
    - Degree Centrality
    - Betweenness Centrality
    - Closeness Centrality
    - Eigenvector Centrality
    - PageRank
- **Community Detection**: Identifies communities using the Louvain method and calculates the modularity of the partition.
- **Structural Properties**: Analyzes the network's structural properties, including:
    - Degree distribution (min, max, and average degree)
    - Average clustering coefficient
    - Average shortest path length (calculated on the giant component if the network is not connected)
- **Path Analysis**: Calculates the diameter of the network and provides an example of a path that represents the diameter.
- **Robustness Analysis**: Simulates targeted attacks (based on degree) and random failures to analyze the network's robustness.

## How to Run

1. **Install dependencies**: `pip install networkx matplotlib pandas scipy`
2. **Run a script**: `python3 analisi_newhope_v2.py`

## Output

Each script generates the following output files:

- `star_wars_[movie]_network.png`: A simple visualization of the network.
- `star_wars_[movie]_network_communities.png`: A visualization of the network with nodes colored by community.
- `star_wars_[movie]_robustness_analysis.png`: A plot showing the results of the robustness analysis.
- `centralities_[movie].csv`: A CSV file containing the centrality scores for each character (only for *A New Hope* in the current version).
