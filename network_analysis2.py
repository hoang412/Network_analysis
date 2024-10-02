import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('netflix_titles.csv')

# Filter movies featuring Adam Sandler in the cast
adam_sandler_movies = data[data['cast'].str.contains("Adam Sandler", na=False)]

# Create an empty graph
G = nx.Graph()

# Iterate through the filtered data and add nodes/edges based on the common director
for _, row in adam_sandler_movies.iterrows():
    cast_list = row['cast'].split(', ')  # Get cast list
    director = row['director']  # Get director
    
    # Add nodes for each actor in the cast
    for actor in cast_list:
        G.add_node(actor)
    
    # Add edges between actors who share the same director
    for i, actor1 in enumerate(cast_list):
        for actor2 in cast_list[i+1:]:
            if director:  # Only add an edge if there is a director
                # Add an edge with director as an attribute
                if not G.has_edge(actor1, actor2):
                    G.add_edge(actor1, actor2, director=director)
                else:
                    # Append the director if an edge already exists
                    G[actor1][actor2]['director'] += f", {director}"


#nx.write_graphml(G, "adam_sandler_network.graphml")

# Get degrees of all nodes (connections per actor)
actor_degrees = dict(G.degree())

# Sort actors by degree (number of connections) in descending order
top_5_actors = sorted(actor_degrees.items(), key=lambda x: x[1], reverse=True)[:6]

# Display the top 5 actors
for actor, degree in top_5_actors:
    print(f"{actor}: {degree} connections")