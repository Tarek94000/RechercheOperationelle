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


def ford_fulkerson(graph):
    source = 0
    sink = graph.n - 1
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


def push_relabel(graph):
    n = graph.n
    source = 0
    sink = n - 1
    
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
        delta = min(excess[u], graph.capacity[u][v] - graph.flow[u][v])
        graph.flow[u][v] += delta
        graph.flow[v][u] -= delta
        excess[u] -= delta
        excess[v] += delta
    
    def relabel(u):
        min_height = float('Inf')
        for v in range(n):
            if graph.capacity[u][v] > graph.flow[u][v]:
                min_height = min(min_height, height[v])
        height[u] = min_height + 1

    def discharge(u):
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

def min_cost_flow(graph, target_flow):
    n = graph.n
    source = 0
    sink = n - 1
    total_cost = 0
    flow = 0

    while flow < target_flow:
        # Trouver les plus courts chemins dans le graphe résiduel
        dist, pred = bellman_ford(graph.residual, graph.cost, source, n)

        # Vérifier si un cycle négatif est présent
        for u in range(n):
            for v in range(n):
                if graph.residual[u][v] > 0 and dist[u] + graph.cost[u][v] < dist[v]:
                    raise ValueError("Cycle négatif détecté dans le graphe.")

        # Vérifier si un chemin est trouvable
        if dist[sink] == float('Inf'):
            print("Aucun chemin disponible pour atteindre le flot cible.")
            break

        # Trouver le flot maximum possible à pousser dans ce chemin
        path_flow = float('Inf')
        v = sink
        while v != source:
            u = pred[v]
            if u == -1:
                raise ValueError("Erreur dans les prédécesseurs : chemin invalide.")
            path_flow = min(path_flow, graph.residual[u][v])
            v = u

        # Limiter le flot pour ne pas dépasser le flot cible restant
        path_flow = min(path_flow, target_flow - flow)

        # Pousser le flot le long du chemin augmentant
        v = sink
        while v != source:
            u = pred[v]
            # Mise à jour du graphe résiduel
            graph.residual[u][v] -= path_flow
            graph.residual[v][u] += path_flow

            # Mise à jour de la matrice de flot
            graph.flow[u][v] += path_flow
            graph.flow[v][u] -= path_flow

            # Mise à jour du coût total
            total_cost += path_flow * graph.cost[u][v]
            v = u

        # Mettre à jour le flot total
        flow += path_flow
        print(f"Flot ajouté : {path_flow}, Flot total : {flow}, Coût total : {total_cost}")

    # Vérifier si le flot cible a été atteint
    if flow < target_flow:
        print("Impossible d'atteindre le flot cible avec les capacités actuelles.")
        return None

    return total_cost
