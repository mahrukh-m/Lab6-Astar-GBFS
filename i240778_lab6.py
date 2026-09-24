import math
import heapq


locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}


# 2. Hospital weighted graph


hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    # add remaining nodes and their connections as given in the lab task document.
    
    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}


def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def reconstruct_path(parent, goal):
    if goal not in parent:
        return None

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def greedy_best_first_search(start, goal, graph):
    priority_queue = [(heuristic(start, goal), start)]
    parent = {start: None}
    cost_so_far = {start: 0}
    visited = set()
    expansion_order = []

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            break

        for neighbor, edge_cost in graph.get(current, {}).items():
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                cost_so_far[neighbor] = cost_so_far[current] + edge_cost
                heapq.heappush(
                    priority_queue,
                    (heuristic(neighbor, goal), neighbor)
                )

    path = reconstruct_path(parent, goal)
    if path is None:
        return None, math.inf, expansion_order

    return path, cost_so_far[goal], expansion_order


def a_star_search(start, goal, graph):
    priority_queue = [(heuristic(start, goal), start)]
    parent = {start: None}
    g_cost = {start: 0}
    visited = set()
    expansion_order = []

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            break

        for neighbor, edge_cost in graph.get(current, {}).items():
            tentative_cost = g_cost[current] + edge_cost

            if tentative_cost < g_cost.get(neighbor, math.inf):
                g_cost[neighbor] = tentative_cost
                parent[neighbor] = current
                f_cost = tentative_cost + heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (f_cost, neighbor))

    path = reconstruct_path(parent, goal)
    if path is None:
        return None, math.inf, expansion_order

    return path, g_cost[goal], expansion_order