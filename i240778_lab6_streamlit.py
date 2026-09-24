import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
# import the necessary functions and variables from searchAlgos.py
from i240778_lab6 import (
    hospital_graph,
    locations,
    greedy_best_first_search,
    a_star_search
)

# Streamlit GUI
#*******************#

# Set Page Config
st.set_page_config(
    page_title="Hospital Navigation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# write meaningful title and description for the app
st.title("Hospital Navigation System")
st.write("hospital navigation system that uses search algorithms to find the shortest path between two points.")

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node", nodes, index=nodes.index("Pharmacy")
    #pass the list of nodes to the selectbox
    # set the default value to "Pharmacy"
)

goal = st.selectbox(
    "Select Goal Node", nodes, index=nodes.index("Emergency_Ward")
    #pass the list of nodes to the selectbox
    # set the default value to "Emergency_Ward"
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"],
    index=1
)

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost, expansion_order = greedy_best_first_search(start, goal, hospital_graph, locations )

        # run the GBFS algorithm with the selected start and goal nodes
        
    else:
        
        path, cost, expansion_order = a_star_search(start, goal, hospital_graph, locations )

        # run the A* algorithm with the selected start and goal nodes
        

    if path is None:
       st.error("No path found")
       # display a error message indicating that no path was found
       

    else:
       
        # Display result
        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Solution Path:** {' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** {cost:.2f}"
        )


        
        # Visualize NetworkX graph
        
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)
        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10, font_weight='bold', arrows=True, edge_labels=nx.get_edge_attributes(G, 'weight'))   
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)