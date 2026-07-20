import heapq


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using a Min-Heap (Priority Queue)

    Time Complexity : O((V + E) log V)
    Space Complexity: O(V)

    graph : {vertex: [(neighbor, weight), ...]}
    source: Starting vertex
    """
    n = len(graph)

    dist = [float('inf')] * n
    prev = [None] * n

    dist[source] = 0

    # Priority Queue: (distance, vertex)
    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        # Ignore outdated entries
        if current_dist > dist[u]:
            continue

        # Relax all adjacent edges
        for v, weight in graph.get(u, []):
            new_dist = current_dist + weight

            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, prev


def reconstruct_path(prev, source, target):
    """Reconstruct the shortest path from source to target."""
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path
    return []


# ---------------- Graph Definition ---------------- #

graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

source = 0

dist, prev = dijkstra(graph, source)

# ---------------- Output ---------------- #

print(f"Shortest Paths from Source Vertex {source}\n")

print(f"{'Vertex':<10}{'Distance':<12}{'Shortest Path'}")
print("-" * 50)

for v in range(len(graph)):
    path = reconstruct_path(prev, source, v)
    path_str = " -> ".join(map(str, path)) if path else "No Path"
    distance = dist[v] if dist[v] != float("inf") else "INF"

    print(f"{v:<10}{str(distance):<12}{path_str}")