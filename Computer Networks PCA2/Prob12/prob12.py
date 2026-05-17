# ============================================================
# Program: Connected / Disconnected Graph Detection
# Topic   : Graph Connectivity using DFS Traversal
# Graph   : Figure 1 (Uploaded Diagram)
#
# Objective:
# 1. Check whether the graph is CONNECTED or DISCONNECTED
# 2. If disconnected, identify all connected components
# 3. Use proper graph theory algorithms without deviating
#    from standard DFS logic
#
# Weight Rule:
# wij = Random Integer between 2 and 9 if i != j
# wij = 0 if i == j
#
# Algorithm Used:
# -> Depth First Search (DFS)
#
# Time Complexity:
# -> O(V + E)
#
# ============================================================

import random
from collections import defaultdict


class Graph:
    def __init__(self):
        # Adjacency list representation
        self.graph = defaultdict(list)

        # Stores edge weights
        self.weights = {}

    # --------------------------------------------------------
    # Add Edge
    # --------------------------------------------------------
    def add_edge(self, u, v):
        """
        Adds an undirected edge between u and v
        with random weight between 2 and 9.
        """

        # Generate random weight
        weight = random.randint(2, 9)

        # Add edge in adjacency list
        self.graph[u].append(v)
        self.graph[v].append(u)

        # Store weights for both directions
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight

    # --------------------------------------------------------
    # Display Graph
    # --------------------------------------------------------
    def display_graph(self):
        print("\n=========== GRAPH STRUCTURE ===========")

        for node in sorted(self.graph.keys()):
            print(f"\n{node} -->")

            for neighbour in self.graph[node]:
                weight = self.weights[(node, neighbour)]
                print(f"   {neighbour} (weight = {weight})")

    # --------------------------------------------------------
    # DFS Traversal
    # --------------------------------------------------------
    def dfs(self, node, visited, component):
        """
        Standard Recursive DFS Algorithm
        """

        visited.add(node)
        component.append(node)

        for neighbour in self.graph[node]:
            if neighbour not in visited:
                self.dfs(neighbour, visited, component)

    # --------------------------------------------------------
    # Find Connected Components
    # --------------------------------------------------------
    def connected_components(self):
        """
        Finds all connected components in graph
        """

        visited = set()
        components = []

        for node in self.graph.keys():

            if node not in visited:
                component = []

                # Perform DFS
                self.dfs(node, visited, component)

                components.append(component)

        return components

    # --------------------------------------------------------
    # Check Connectivity
    # --------------------------------------------------------
    def check_connectivity(self):

        components = self.connected_components()

        print("\n=======================================")
        print("GRAPH CONNECTIVITY ANALYSIS")
        print("=======================================")

        if len(components) == 1:
            print("\nThe graph is CONNECTED.")
            print("\nAll nodes belong to a single component:")
            print(sorted(components[0]))

        else:
            print("\nThe graph is DISCONNECTED.")
            print(f"\nNumber of Connected Components = {len(components)}")

            for index, component in enumerate(components, start=1):
                print(f"\nComponent {index}:")
                print(sorted(component))


# ============================================================
# MAIN DRIVER PROGRAM
# ============================================================

if __name__ == "__main__":

    # Create graph object
    g = Graph()

    # ========================================================
    # EDGES FROM THE UPLOADED FIGURE
    # ========================================================

    edges = [

        ("x1", "x5"),
        ("x1", "x6"),
        ("x1", "x8"),
        ("x1", "x9"),

        ("x2", "x3"),
        ("x2", "x5"),
        ("x2", "x7"),
        ("x2", "x9"),

        ("x3", "x4"),
        ("x3", "x8"),

        ("x4", "x7"),
        ("x4", "x9"),

        ("x5", "x6"),
        ("x5", "x7"),
        ("x5", "x9"),

        ("x6", "x7"),

        ("x8", "x9")
    ]

    # ========================================================
    # ADD ALL EDGES TO GRAPH
    # ========================================================

    for u, v in edges:
        g.add_edge(u, v)

    # ========================================================
    # DISPLAY GRAPH
    # ========================================================

    g.display_graph()

    # ========================================================
    # CHECK CONNECTIVITY
    # ========================================================

    g.check_connectivity()