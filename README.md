# Star Wars Network Analysis

This repository contains Python scripts to analyze the character interaction networks of the original Star Wars trilogy. Each script focuses on one movie, performs a series of network analyses, and saves the results as graphs and data files.

## Scripts

- **`analisi_ANH.py`**: Analyzes the character interaction network of a *Star Wars: Episode IV – A New Hope*.
- **`analisi_ESB.py`**: Analyzes the character interaction network of *Star Wars: Episode V – The Empire Strikes Back*.
- **`analisi_RJ.py`**: Analyzes the character interaction network of *Star Wars: Episode VI – Return of the Jedi*.

## Configuration

To analyze a different movie, you can change the following constants at the top of any of the scripts:

- `MOVIE_TITLE`: The title of the movie (e.g., "Star Wars: The Empire Strikes Back"). This is used for titles and output filenames.
- `JSON_FILE_PATH`: The path to the JSON file containing the network data (e.g., "movie-jsons/empire.json").

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

1.  **Install dependencies**: `pip install networkx matplotlib pandas scipy`
2.  **Run a script**: `python3 analisi_ANH.py`

## Output

The script generates the following output files, using the `MOVIE_TITLE` for naming:

- `[MOVIE_TITLE]_network.png`: A simple visualization of the network.
- `[MOVIE_TITLE]_network_communities.png`: A visualization of the network with nodes colored by community.
- `[MOVIE_TITLE]_robustness_analysis.png`: A plot showing the results of the robustness analysis.
- `centralities_[MOVIE_TITLE].csv`: A CSV file containing the centrality scores for each character.

## Project Structure

- **`.gitignore`**: This file is configured to ignore generated image (`.png`) and data (`.csv`) files.
- **`movie-jsons/`**: This directory contains the JSON data files for each movie, which are used as input for the analysis scripts.
