from collections import deque

def bfs(residual, source, sink, parent):
    n = len(residual)
    visited = [False] * n  # Liste pour suivre les sommets visités
    queue = deque([source])  # File d'attente pour BFS, initialisée avec la source
    visited[source] = True  # Marquer la source comme visitée

    while queue:
        u = queue.popleft()  # Extraire un sommet de la file d'attente
        for v in range(n):
            # Si le sommet v n'a pas été visité et qu'il y a une capacité résiduelle
            if not visited[v] and residual[u][v] > 0:
                parent[v] = u  # Enregistrer le parent de v
                visited[v] = True  # Marquer v comme visité
                queue.append(v)  # Ajouter v à la file d'attente
                if v == sink:
                    return True  # Si le puits est atteint, retourner True
    return False  # Si aucun chemin n'est trouvé, retourner False


def ford_fulkerson(graph):
    source = 0
    sink = graph.n - 1
    parent = [-1] * graph.n
    max_flow = 0

    # Tant qu'il y a un chemin augmentant du source au puits
    while bfs(graph.residual, source, sink, parent):
        path_flow = float('Inf')
        v = sink

        # Trouver le flot maximum à travers le chemin trouvé par BFS
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph.residual[u][v])
            v = u

        # Mettre à jour les capacités résiduelles des arêtes et des arêtes inverses le long du chemin
        v = sink
        while v != source:
            u = parent[v]
            graph.residual[u][v] -= path_flow
            graph.residual[v][u] += path_flow
            graph.flow[u][v] += path_flow
            graph.flow[v][u] -= path_flow
            v = u

        max_flow += path_flow

        graph.display_residual()
        # Afficher le chemin trouvé
        augmenting_path = []
        v = sink
        while v != source:
            augmenting_path.append(v)
            v = parent[v]
        augmenting_path.append(source)
        augmenting_path.reverse()

        print("Chemin trouvé : ", end="")
        
        for i in range(len(augmenting_path)):
            if i == 0:
                print(f"s -> ", end="")
            elif augmenting_path[i] == sink:
                print("t")
            else:
                print(chr(augmenting_path[i]+96), "-> ", end="")

    return max_flow

def push_relabel(graph):
    n = graph.n
    source = 0
    sink = n - 1
    
    height = [0] * n       # Hauteur des sommets
    excess = [0] * n       # Flot excédentaire aux sommets
    seen = [0] * n         # Suivi des voisins vus pour la décharge
    
    # Initialiser le pré-flot
    height[source] = n
    for v in range(n):
        if graph.capacity[source][v] > 0:
            graph.flow[source][v] = graph.capacity[source][v]
            graph.flow[v][source] = -graph.flow[source][v]
            excess[v] = graph.capacity[source][v]
            excess[source] -= graph.capacity[source][v]
    
    def push(u, v):
        # Pousser le flot de u à v
        delta = min(excess[u], graph.capacity[u][v] - graph.flow[u][v])
        graph.flow[u][v] += delta
        graph.flow[v][u] -= delta
        excess[u] -= delta
        excess[v] += delta
        print(f"Poussé {delta} de {u} vers {v}")

    def relabel(u):
        # Réétiqueter le sommet u
        min_height = float('Inf')
        for v in range(n):
            if graph.capacity[u][v] > graph.flow[u][v]:
                min_height = min(min_height, height[v])
        height[u] = min_height + 1
        print(f"Réétiquetage de {u} à la hauteur {height[u]}")

    def discharge(u):
        # Décharger le sommet u
        while excess[u] > 0:
            if seen[u] < n:  # Vérifier le prochain voisin
                v = seen[u]
                if graph.capacity[u][v] > graph.flow[u][v] and height[u] > height[v]:
                    push(u, v)
                else:
                    seen[u] += 1
            else:
                relabel(u)
                seen[u] = 0

    # Ensemble des sommets excluant la source et le puits
    active = [i for i in range(n) if i != source and i != sink]

    # Décharger les sommets actifs
    while any(excess[i] > 0 for i in active):
        for u in active:
            if excess[u] > 0:
                print(f"Décharge de {u} avec {excess[u]}")
                discharge(u)

    # Retourner le flot maximum, qui est le flot total entrant dans le puits
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
