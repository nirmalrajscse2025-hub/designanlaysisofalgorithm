"""
Ex. No. 8 - Travelling Salesman Problem using Branch and Bound
             for Finding Optimal Path

CS5303 - DAA Lab
Chennai Institute of Technology | Dept. of CSE
"""

import heapq
from itertools import permutations

INF = float('inf')


def reduce_matrix(mat):
    """Reduce a cost matrix (row-wise then column-wise) and return the
    reduced matrix along with the total reduction cost."""
    n = len(mat)
    m = [row[:] for row in mat]
    cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(m[i])
        if row_min and row_min != INF:
            cost += row_min
            m[i] = [x - row_min if x != INF else INF for x in m[i]]

    # Column reduction
    for j in range(n):
        col_min = min(m[i][j] for i in range(n))
        if col_min and col_min != INF:
            cost += col_min
            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


class Node:
    """A node in the branch-and-bound search tree."""

    def __init__(self, level, path, reduced_matrix, cost, visited):
        self.level = level
        self.path = path
        self.reduced_matrix = reduced_matrix
        self.cost = cost
        self.visited = visited

    def __lt__(self, other):
        # heapq needs a comparison; order nodes by their lower bound cost
        return self.cost < other.cost


def tsp_branch_and_bound(cost_matrix, n):
    """Solve TSP using the Branch and Bound technique with matrix
    reduction as the bounding function."""
    root_matrix, root_cost = reduce_matrix(cost_matrix)

    root = Node(
        level=0,
        path=[0],
        reduced_matrix=root_matrix,
        cost=root_cost,
        visited={0},
    )

    pq = [root]
    heapq.heapify(pq)

    best_cost = INF
    best_path = None

    while pq:
        node = heapq.heappop(pq)

        # Prune if this node cannot possibly beat the current best
        if node.cost >= best_cost:
            continue

        # Leaf node: all cities visited. The chain of matrix reductions has
        # already absorbed the cost of the final (forced) return edge, so
        # node.cost is the exact cost of the completed tour.
        if node.level == n - 1:
            if node.cost < best_cost:
                best_cost = node.cost
                best_path = node.path + [0]
            continue

        current_city = node.path[-1]

        for next_city in range(n):
            if next_city in node.visited:
                continue
            if node.reduced_matrix[current_city][next_city] == INF:
                continue

            # Build the child's matrix: block the row/col and the reverse edge
            child_matrix = [row[:] for row in node.reduced_matrix]
            edge_cost = child_matrix[current_city][next_city]

            for k in range(n):
                child_matrix[current_city][k] = INF
                child_matrix[k][next_city] = INF
            child_matrix[next_city][0] = INF

            reduced_child, reduction_cost = reduce_matrix(child_matrix)

            child_cost = node.cost + edge_cost + reduction_cost
            child = Node(
                level=node.level + 1,
                path=node.path + [next_city],
                reduced_matrix=reduced_child,
                cost=child_cost,
                visited=node.visited | {next_city},
            )
            heapq.heappush(pq, child)

    return best_path, best_cost


def tsp_brute_force(cost_matrix, n):
    """Brute force solver, used to verify the branch-and-bound result."""
    cities = list(range(1, n))
    best_cost = INF
    best_path = None

    for perm in permutations(cities):
        path = [0] + list(perm) + [0]
        c = sum(cost_matrix[path[i]][path[i + 1]] for i in range(n))
        if c < best_cost:
            best_cost = c
            best_path = path

    return best_path, best_cost


def print_matrix(cost_matrix, cities):
    print('Cost Matrix:')
    print(f'{"":>4}', ' '.join(f'{c:>5}' for c in cities))
    for i, row in enumerate(cost_matrix):
        r = ['INF' if x == INF else str(x) for x in row]
        print(f'{cities[i]:>4}', ' '.join(f'{v:>5}' for v in r))


def print_tour(path, best_cost, cost_matrix, cities, label):
    print(f'\n{label}')
    print(f'Optimal Tour: {" -> ".join(cities[i] for i in path)}')
    print(f'Minimum Cost: {best_cost}')
    print('Path verification:')
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        print(f'  {cities[u]} -> {cities[v]}: cost = {cost_matrix[u][v]}')


def main():
    # --- 5-city cost matrix ---
    cost = [
        [INF, 10, 8, 9, 7],
        [10, INF, 10, 5, 6],
        [8, 10, INF, 8, 9],
        [9, 5, 8, INF, 6],
        [7, 6, 9, 6, INF],
    ]
    n = 5
    cities = ['A', 'B', 'C', 'D', 'E']

    print('5-City TSP')
    print_matrix(cost, cities)

    # Branch and Bound solution
    bb_path, bb_cost = tsp_branch_and_bound(cost, n)
    print_tour(bb_path, bb_cost, cost, cities, 'Branch and Bound Result')

    # Brute force verification
    bf_path, bf_cost = tsp_brute_force(cost, n)
    print_tour(bf_path, bf_cost, cost, cities, 'Brute Force Verification')

    # Confirm both approaches agree
    print(f'\nMatch: {"YES" if bb_cost == bf_cost else "NO"}')


if __name__ == '__main__':
    main()
