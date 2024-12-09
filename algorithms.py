from collections import deque

def bfs(residual, source, sink, parent):
    n = len(residual)
    visited = [False] * n
    queue = deque([source])
    visited[source] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and residual[u][v] > 0:
                parent[v] = u
                visited[v] = True
                queue.append(v)
                if v == sink:
                    return True
    return False


def ford_fulkerson(graph, source, sink):
    parent = [-1] * graph.n
    max_flow = 0

    while bfs(graph.residual, source, sink, parent):
        path_flow = float('Inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph.residual[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            graph.residual[u][v] -= path_flow
            graph.residual[v][u] += path_flow
            graph.flow[u][v] += path_flow
            graph.flow[v][u] -= path_flow
            v = u

        max_flow += path_flow

    return max_flow


def push_relabel(graph, source, sink):
    """
    Push-Relabel algorithm for Maximum Flow problem.
    
    Args:
        graph (FlowNetwork): The graph object.
        source (int): Source vertex index.
        sink (int): Sink vertex index.
    
    Returns:
        int: Maximum flow from source to sink.
    """
    n = graph.n
    height = [0] * n       # Height of vertices
    excess = [0] * n       # Excess flow at vertices
    seen = [0] * n         # Tracks neighbors seen for discharge
    
    # Initialize preflow
    height[source] = n
    for v in range(n):
        if graph.capacity[source][v] > 0:
            graph.flow[source][v] = graph.capacity[source][v]
            graph.flow[v][source] = -graph.flow[source][v]
            excess[v] = graph.capacity[source][v]
            excess[source] -= graph.capacity[source][v]
    
    def push(u, v):
        """
        Push flow from vertex u to vertex v.
        """
        delta = min(excess[u], graph.capacity[u][v] - graph.flow[u][v])
        graph.flow[u][v] += delta
        graph.flow[v][u] -= delta
        excess[u] -= delta
        excess[v] += delta
    
    def relabel(u):
        """
        Relabel vertex u to allow pushing.
        """
        min_height = float('Inf')
        for v in range(n):
            if graph.capacity[u][v] > graph.flow[u][v]:
                min_height = min(min_height, height[v])
        height[u] = min_height + 1

    def discharge(u):
        """
        Discharge excess flow from vertex u.
        """
        while excess[u] > 0:
            if seen[u] < n:  # Check next neighbor
                v = seen[u]
                if graph.capacity[u][v] > graph.flow[u][v] and height[u] > height[v]:
                    push(u, v)
                else:
                    seen[u] += 1
            else:
                relabel(u)
                seen[u] = 0

    # Set of vertices excluding source and sink
    active = [i for i in range(n) if i != source and i != sink]

    # Discharge active vertices
    while any(excess[i] > 0 for i in active):
        for u in active:
            if excess[u] > 0:
                discharge(u)

    # Return the maximum flow, which is the total flow into the sink
    return sum(graph.flow[v][sink] for v in range(n))


def bellman_ford(residual, cost, source, n):
    """
    Bellman-Ford algorithm to find shortest paths in a graph.
    
    Args:
        residual (list[list[int]]): Residual graph capacities.
        cost (list[list[int]]): Edge costs for the graph.
        source (int): Source vertex index.
        n (int): Number of vertices.
    
    Returns:
        tuple: (distances, predecessors) where:
            distances (list[int]): Shortest path distances from the source.
            predecessors (list[int]): Predecessor for each vertex on the shortest path.
    """
    dist = [float('Inf')] * n
    pred = [-1] * n
    dist[source] = 0

    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if residual[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                    dist[v] = dist[u] + cost[u][v]
                    pred[v] = u

    # Check for negative cycles (optional, not required here)
    return dist, pred


def min_cost_flow(graph, source, sink, target_flow):
    """
    Minimum Cost Flow algorithm using Bellman-Ford to find augmenting paths.
    
    Args:
        graph (FlowNetwork): The graph object.
        source (int): Source vertex index.
        sink (int): Sink vertex index.
        target_flow (int): Target flow value.
    
    Returns:
        int: Total cost of the flow.
    """
    n = graph.n
    total_cost = 0
    flow = 0

    while flow < target_flow:
        # Find shortest paths in the residual graph
        dist, pred = bellman_ford(graph.residual, graph.cost, source, n)

        # If no path exists, break
        if dist[sink] == float('Inf'):
            break

        # Find the maximum flow we can push through the augmenting path
        path_flow = float('Inf')
        v = sink
        while v != source:
            u = pred[v]
            path_flow = min(path_flow, graph.residual[u][v])
            v = u

        # Push flow along the augmenting path
        v = sink
        while v != source:
            u = pred[v]
            graph.residual[u][v] -= path_flow
            graph.residual[v][u] += path_flow
            total_cost += path_flow * graph.cost[u][v]
            v = u

        flow += path_flow

    return total_cost
