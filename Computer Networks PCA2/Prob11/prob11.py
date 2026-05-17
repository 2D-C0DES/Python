"""
===============================================================================
DISTANCE VECTOR ROUTING SIMULATION
-------------------------------------------------------------------------------
Problem:
1. Simulate Distance Vector Routing Algorithm
2. Find shortest path from x6 to x3
3. Find all possible paths from x5 to x3

Graph weights:
w_ij = random integer between 2 and 9 if i != j
w_ii = 0

This program follows the actual Distance Vector Routing logic:
- Each router maintains a routing table
- Routers exchange routing information with neighbors
- Bellman-Ford Equation is used:
      D_x(y) = min [ c(x,v) + D_v(y) ]

Author: Debanjan Das
===============================================================================
"""

import random
from collections import defaultdict
from copy import deepcopy

# =============================================================================
# STEP 1: CREATE GRAPH
# =============================================================================

class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, weight):
        """
        Add undirected edge between u and v
        """
        self.graph[u][v] = weight
        self.graph[v][u] = weight

    def get_nodes(self):
        return list(self.graph.keys())

    def display_graph(self):
        print("\n================ GRAPH EDGES ================\n")

        visited = set()

        for u in self.graph:
            for v in self.graph[u]:

                if (v, u) not in visited:
                    print(f"{u} ----({self.graph[u][v]})---- {v}")
                    visited.add((u, v))

        print()


# =============================================================================
# STEP 2: DISTANCE VECTOR ROUTING IMPLEMENTATION
# =============================================================================

class DistanceVectorRouting:

    def __init__(self, graph):
        self.graph = graph.graph
        self.nodes = list(self.graph.keys())

        # Distance table
        self.distance_table = {}

        # Next hop table
        self.next_hop = {}

        self.initialize_tables()

    # -------------------------------------------------------------------------
    # INITIALIZATION
    # -------------------------------------------------------------------------

    def initialize_tables(self):

        for node in self.nodes:

            self.distance_table[node] = {}
            self.next_hop[node] = {}

            for destination in self.nodes:

                # Distance to itself is 0
                if node == destination:
                    self.distance_table[node][destination] = 0
                    self.next_hop[node][destination] = node

                # Direct neighbor distance
                elif destination in self.graph[node]:
                    self.distance_table[node][destination] = self.graph[node][destination]
                    self.next_hop[node][destination] = destination

                # Unknown path initially
                else:
                    self.distance_table[node][destination] = float('inf')
                    self.next_hop[node][destination] = None

    # -------------------------------------------------------------------------
    # DISPLAY ROUTING TABLE
    # -------------------------------------------------------------------------

    def display_tables(self):

        print("\n================ ROUTING TABLES ================\n")

        for node in self.nodes:

            print(f"\nRouting Table for Router {node}")
            print("-" * 50)

            print(f"{'Destination':<15}{'Cost':<10}{'Next Hop'}")
            print("-" * 50)

            for destination in self.nodes:

                cost = self.distance_table[node][destination]

                if cost == float('inf'):
                    cost = "INF"

                print(f"{destination:<15}{str(cost):<10}{self.next_hop[node][destination]}")

    # -------------------------------------------------------------------------
    # DISTANCE VECTOR ALGORITHM
    # -------------------------------------------------------------------------

    def run_distance_vector(self):

        print("\n================================================")
        print("STARTING DISTANCE VECTOR ROUTING ALGORITHM")
        print("================================================")

        iteration = 0

        while True:

            iteration += 1

            print(f"\nIteration {iteration}")

            updated = False

            # Copy previous table
            old_table = deepcopy(self.distance_table)

            # For every router
            for source in self.nodes:

                # Check every neighbor
                for neighbor in self.graph[source]:

                    # Check every destination
                    for destination in self.nodes:

                        # Bellman-Ford Equation
                        new_distance = (
                            self.graph[source][neighbor]
                            + old_table[neighbor][destination]
                        )

                        # Update if shorter path found
                        if new_distance < self.distance_table[source][destination]:

                            old_cost = self.distance_table[source][destination]

                            self.distance_table[source][destination] = new_distance
                            self.next_hop[source][destination] = neighbor

                            updated = True

                            print(
                                f"Router {source}: "
                                f"Updated route to {destination} "
                                f"from {old_cost} to {new_distance} "
                                f"via {neighbor}"
                            )

            # Stop if no changes
            if not updated:
                print("\nNetwork has converged.")
                break

        print("\nDistance Vector Routing Completed Successfully.\n")

    # -------------------------------------------------------------------------
    # GET SHORTEST PATH
    # -------------------------------------------------------------------------

    def get_shortest_path(self, source, destination):

        path = [source]

        current = source

        # Build path using next hop table
        while current != destination:

            current = self.next_hop[current][destination]

            if current is None:
                return None, float('inf')

            path.append(current)

        cost = self.distance_table[source][destination]

        return path, cost


# =============================================================================
# STEP 3: FIND ALL POSSIBLE PATHS
# =============================================================================

def find_all_paths(graph, start, end, path=None):

    if path is None:
        path = []

    path = path + [start]

    # Destination reached
    if start == end:
        return [path]

    paths = []

    # Visit neighbors
    for neighbor in graph[start]:

        if neighbor not in path:

            new_paths = find_all_paths(
                graph,
                neighbor,
                end,
                path
            )

            for p in new_paths:
                paths.append(p)

    return paths


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():

    random.seed()  # Random weights every execution

    g = Graph()

    # -------------------------------------------------------------------------
    # GRAPH CONNECTIONS FROM THE GIVEN FIGURE
    # -------------------------------------------------------------------------

    edges = [

        ("x6", "x7"),
        ("x6", "x5"),
        ("x6", "x1"),

        ("x7", "x5"),
        ("x7", "x4"),

        ("x5", "x2"),
        ("x5", "x9"),
        ("x5", "x1"),

        ("x2", "x3"),
        ("x2", "x9"),

        ("x4", "x3"),
        ("x4", "x9"),

        ("x9", "x8"),
        ("x9", "x1"),

        ("x3", "x8")
    ]

    # -------------------------------------------------------------------------
    # ASSIGN RANDOM WEIGHTS BETWEEN 2 AND 9
    # -------------------------------------------------------------------------

    print("\n================================================")
    print("GENERATING RANDOM EDGE WEIGHTS")
    print("================================================")

    for u, v in edges:

        weight = random.randint(2, 9)

        g.add_edge(u, v, weight)

    # Display graph
    g.display_graph()

    # -------------------------------------------------------------------------
    # RUN DISTANCE VECTOR ROUTING
    # -------------------------------------------------------------------------

    dvr = DistanceVectorRouting(g)

    print("\nINITIAL ROUTING TABLES")
    dvr.display_tables()

    dvr.run_distance_vector()

    print("\nFINAL ROUTING TABLES")
    dvr.display_tables()

    # -------------------------------------------------------------------------
    # SHORTEST PATH FROM x6 TO x3
    # -------------------------------------------------------------------------

    print("\n================================================")
    print("SHORTEST PATH FROM x6 TO x3")
    print("================================================")

    shortest_path, total_cost = dvr.get_shortest_path("x6", "x3")

    print("\nShortest Path:")
    print(" -> ".join(shortest_path))

    print(f"\nTotal Cost = {total_cost}")

    # -------------------------------------------------------------------------
    # FIND ALL POSSIBLE PATHS FROM x5 TO x3
    # -------------------------------------------------------------------------

    print("\n================================================")
    print("ALL POSSIBLE PATHS FROM x5 TO x3")
    print("================================================")

    all_paths = find_all_paths(g.graph, "x5", "x3")

    for index, path in enumerate(all_paths, start=1):

        print(f"\nPath {index}: {' -> '.join(path)}")

        # Calculate path cost
        cost = 0

        for i in range(len(path) - 1):
            cost += g.graph[path[i]][path[i + 1]]

        print(f"Cost = {cost}")

    print("\n================================================")
    print("PROGRAM EXECUTION COMPLETED")
    print("================================================")


# =============================================================================
# DRIVER CODE
# =============================================================================

if __name__ == "__main__":
    main()