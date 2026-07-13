import heapq


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path Compression
        return self.parent[x]

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        # Union by Rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.parent[ry] = rx

        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True


def kruskal(n, edges):
    """
    Kruskal's Algorithm
    Time Complexity: O(E log E)
    """
    edges = sorted(edges)

    uf = UnionFind(n)

    mst = []
    total_cost = 0

    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight

            if len(mst) == n - 1:
                break

    return mst, total_cost


def prim(n, adj, start=0):
    """
    Prim's Algorithm
    Time Complexity: O(E log V)
    """

    INF = float("inf")

    key = [INF] * n
    parent = [-1] * n
    in_mst = [False] * n

    key[start] = 0

    pq = [(0, start)]  # (weight, vertex)

    mst = []
    total_cost = 0

    while pq:
        weight, u = heapq.heappop(pq)

        if in_mst[u]:
            continue

        in_mst[u] = True

        if parent[u] != -1:
            mst.append((parent[u], u, weight))
            total_cost += weight

        for v, wt in adj.get(u, []):
            if not in_mst[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, total_cost


# ---------------- MAIN PROGRAM ---------------- #

n = 7

edges = [
    (7, 0, 1),
    (5, 0, 3),
    (8, 1, 2),
    (9, 1, 3),
    (7, 1, 4),
    (5, 2, 4),
    (15, 3, 4),
    (6, 3, 5),
    (8, 4, 5),
    (9, 4, 6),
    (11, 5, 6),
]

# Build adjacency list
adj = {}

for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

# Run Kruskal
k_mst, k_cost = kruskal(n, edges)

# Run Prim
p_mst, p_cost = prim(n, adj)

# Display Results
print("===== Kruskal's MST =====")
for u, v, w in k_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total Cost =", k_cost)

print("\n===== Prim's MST =====")
for u, v, w in p_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total Cost =", p_cost)