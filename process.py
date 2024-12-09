from collections import deque

def find_augmenting_path(graph, n):
    """
    Trouve un chemin augmentant dans un graphe résiduel en utilisant un parcours en largeur (BFS).

    Arguments :
        graph (dict): Graphe résiduel sous forme de dictionnaire {nœud: {voisin: {"capacité": valeur}}}.
        n (int): Nombre total de nœuds.

    Retourne :
        tuple: (chemin, min_capacity) où :
            - chemin (list): Liste des nœuds constituant le chemin augmentant.
            - min_capacity (int): Capacité minimale sur le chemin.
    """
    source = 0
    sink = n - 1

    # Initialisation
    visited = set()
    parent = {source: None}  # Pour reconstruire le chemin
    queue = deque([source])

    while queue:
        current = queue.popleft()
        visited.add(current)

        # Parcourir les voisins du nœud actuel
        for neighbor, data in graph[current].items():
            capacity = data.get("capacité", 0)
            if neighbor not in visited and capacity > 0:  # Chemin possible
                parent[neighbor] = current
                if neighbor == sink:  # Si on atteint le puits
                    # Reconstruire le chemin
                    path = []
                    min_capacity = float('inf')
                    node = sink
                    while node is not None:
                        path.insert(0, node)
                        if parent[node] is not None:
                            min_capacity = min(min_capacity, graph[parent[node]][node]["capacité"])
                        node = parent[node]
                    return path, min_capacity
                queue.append(neighbor)

    return [], 0  # Aucun chemin trouvé


def find_min_cost_path(graph, n):
    """
    Trouve un chemin augmentant avec le coût minimal dans un graphe résiduel à l'aide de Bellman-Ford.

    Arguments :
        graph (dict): Graphe résiduel sous forme de dictionnaire {nœud: {voisin: {"capacité": valeur, "prix": valeur}}}.
        n (int): Nombre total de nœuds.

    Retourne :
        tuple: (chemin, min_capacity, path_cost) où :
            - chemin (list): Liste des nœuds constituant le chemin.
            - min_capacity (int): Capacité minimale sur le chemin.
            - path_cost (int): Coût total du chemin.
    """
    source = 0
    sink = n - 1

    # Initialisation des distances et parents
    dist = {i: float('inf') for i in range(n)}
    parent = {i: None for i in range(n)}
    dist[source] = 0

    # Bellman-Ford : Relaxation des arêtes
    for _ in range(n - 1):  # Maximum n-1 itérations
        for u in graph:
            for v, data in graph[u].items():
                capacity = data.get("capacité", 0)
                cost = data.get("prix", 0)
                if capacity > 0 and dist[u] + cost < dist[v]:  # Relaxation
                    dist[v] = dist[u] + cost
                    parent[v] = u

    # Vérifier si le puits est accessible
    if dist[sink] == float('inf'):
        return [], 0, 0  # Aucun chemin trouvé

    # Reconstruire le chemin et calculer la capacité minimale
    path = []
    min_capacity = float('inf')
    node = sink
    while node is not None:
        path.insert(0, node)
        if parent[node] is not None:
            min_capacity = min(min_capacity, graph[parent[node]][node]["capacité"])
        node = parent[node]

    # Retourner le chemin, la capacité minimale et le coût total
    return path, min_capacity, dist[sink]


def ford_fulkerson(graph, n):
    """
    Implémente l'algorithme Ford-Fulkerson pour trouver le flot maximal.

    Arguments :
        graph (dict): Le graphe avec les capacités et prix.
        n (int): Nombre de nœuds.

    Retourne :
        tuple: (flot_maximal, graphe_résiduel)
    """
    max_flow = 0

    while True:
        # Trouver un chemin augmentant et sa capacité minimale
        path, min_capacity = find_augmenting_path(graph, n)

        if not path:  # Aucun chemin augmentant trouvé
            break

        # Ajouter la capacité minimale au flot total
        max_flow += min_capacity

        # Mettre à jour les capacités dans le graphe résiduel
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]

            # Réduire la capacité de l'arête u -> v
            graph[u][v]["capacité"] -= min_capacity

            # Ajouter ou mettre à jour l'arête inverse v -> u
            if v not in graph:
                graph[v] = {}
            if u in graph[v]:
                graph[v][u]["capacité"] += min_capacity
            else:
                graph[v][u] = {"capacité": min_capacity}

    return max_flow, graph


def bellman_ford_min_cost(graph, n):
    """
    Implémente l'algorithme pour trouver le flot à coût minimal.

    Arguments :
        graph (dict): Le graphe avec les capacités et prix.
        n (int): Nombre de nœuds.

    Retourne :
        tuple: (flot_total, coût_total, graphe_résiduel)
    """
    max_flow = 0
    total_cost = 0

    while True:
        # Trouver un chemin augmentant avec Bellman-Ford
        path, min_capacity, path_cost = find_min_cost_path(graph, n)

        if not path:  # Aucun chemin augmentant trouvé
            break

        # Ajouter la capacité minimale au flot total
        max_flow += min_capacity
        total_cost += min_capacity * path_cost

        # Mettre à jour les capacités et les coûts dans le graphe résiduel
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]

            # Réduire la capacité de l'arête u -> v
            graph[u][v]["capacité"] -= min_capacity

            # Ajouter ou mettre à jour l'arête inverse v -> u
            if v not in graph:
                graph[v] = {}
            if u in graph[v]:
                graph[v][u]["capacité"] += min_capacity
            else:
                graph[v][u] = {"capacité": min_capacity}

    return max_flow, total_cost, graph
