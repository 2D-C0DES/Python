import networkx as nx
import random
import math
from itertools import islice

# ----------------------------------------------------------
# STEP 1 : CREATE GRAPH
# ----------------------------------------------------------

G = nx.Graph()

nodes = [f"x{i}" for i in range(1, 10)]

G.add_nodes_from(nodes)

# Graph edges from the figure
edges = [
    ("x6", "x7"),
    ("x7", "x4"),
    ("x4", "x3"),
    ("x7", "x5"),
    ("x6", "x5"),
    ("x6", "x1"),
    ("x5", "x1"),
    ("x1", "x8"),
    ("x8", "x3"),
    ("x5", "x2"),
    ("x2", "x3"),
    ("x2", "x9"),
    ("x9", "x8"),
    ("x5", "x9"),
    ("x1", "x9"),
    ("x2", "x7"),
    ("x4", "x9")
]

# Assign random weights between 2 and 9
for u, v in edges:
    weight = random.randint(2, 9)
    G.add_edge(u, v, weight=weight)

# ----------------------------------------------------------
# STEP 2 : INITIAL NODE POSITIONS
# ----------------------------------------------------------

positions_t1 = {}

for node in nodes:
    positions_t1[node] = (
        random.randint(0, 100),
        random.randint(0, 100)
    )

# ----------------------------------------------------------
# STEP 3 : UPDATED POSITIONS AFTER MOVEMENT
# ----------------------------------------------------------

positions_t2 = {}

for node in nodes:

    old_x, old_y = positions_t1[node]

    # Random movement
    new_x = old_x + random.randint(-10, 10)
    new_y = old_y + random.randint(-10, 10)

    positions_t2[node] = (new_x, new_y)

# ----------------------------------------------------------
# STEP 4 : DISTANCE FUNCTION
# ----------------------------------------------------------

def euclidean_distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )

# ----------------------------------------------------------
# STEP 5 : CALCULATE LINK STABILITY
# ----------------------------------------------------------

link_stability = {}

for u, v in G.edges():

    d1 = euclidean_distance(
        positions_t1[u],
        positions_t1[v]
    )

    d2 = euclidean_distance(
        positions_t2[u],
        positions_t2[v]
    )

    delta_d = abs(d2 - d1)

    weight = G[u][v]['weight']

    # Stability Formula
    stability = weight / (1 + delta_d)

    link_stability[(u, v)] = stability

# ----------------------------------------------------------
# STEP 6 : FIND ALL PATHS
# ----------------------------------------------------------

source = "x6"
destination = "x3"

all_paths = list(
    nx.all_simple_paths(
        G,
        source=source,
        target=destination
    )
)

# ----------------------------------------------------------
# STEP 7 : CALCULATE PATH STABILITY
# ----------------------------------------------------------

best_path = None
best_stability = -1

print("\nALL POSSIBLE PATHS\n")

for path in all_paths:

    total_stability = 0

    for i in range(len(path) - 1):

        u = path[i]
        v = path[i + 1]

        if (u, v) in link_stability:
            total_stability += link_stability[(u, v)]
        else:
            total_stability += link_stability[(v, u)]

    print(f"Path: {path}")
    print(f"Stability Score: {total_stability:.4f}\n")

    if total_stability > best_stability:
        best_stability = total_stability
        best_path = path

# ----------------------------------------------------------
# STEP 8 : OUTPUT MOST STABLE PATH
# ----------------------------------------------------------

print("=" * 60)
print("MOST STABLE PATH")
print("=" * 60)

print(f"Source Node      : {source}")
print(f"Destination Node : {destination}")

print(f"\nMost Stable Path : {best_path}")

print(f"Path Stability   : {best_stability:.4f}")

# ----------------------------------------------------------
# STEP 9 : DISPLAY EDGE WEIGHTS
# ----------------------------------------------------------

print("\nEDGE WEIGHTS\n")

for u, v in G.edges():
    print(f"{u} -- {v} : Weight = {G[u][v]['weight']}")