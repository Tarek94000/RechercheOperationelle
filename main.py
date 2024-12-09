from process import *

def read_graph(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    n = int(lines[0])

    # Initialisation du graphe
    graph = {}
    prixType = False
    for i in range(n):
        graph[i] = {}

    # Création du tableau de capacité
    for i in range(1, 1+n): # Parcours la colonne
        line = lines[i].split() # Lis la ligne et sépare les valeurs

        for j, value in enumerate(line): # Parcours les valeurs
            if value != "0": # Si la valeur est différente de 0 dans la matrice, on l'implémente dans le graphe
                graph[i-1][j] = {"capacité": int(value)}

    # Ajout du prix si existant
    if len(lines) > n+1:
        prixType = True
        for i in range(n + 2, 1+2*n): # Parcours la colonne
            line = lines[i-1].split() # Lis la ligne et sépare les valeurs

            for j, value in enumerate(line): # Parcours les valeurs
                if value != "0": # Si la valeur est différente de 0 dans la matrice, on l'implémente dans le graphe
                    graph[i-n-2][j]["prix"] = int(value)

    return graph, n, prixType

graph, n, prixType = read_graph("figures/fig6.txt")

print(graph)
print(n)
print(prixType)

for task in graph:
    print()
    for task2 in graph[task]:
            print(task, "en", task2, "avec capacité",graph[task][task2]["capacité"], end = " ")
            if prixType:
                print("et prix", graph[task][task2]["prix"])

# Test de find_augmenting_path
path, min_capacity = find_augmenting_path(graph, n)
print("Chemin augmentant :", path)
print("Capacité minimale :", min_capacity)


# Test de ford_fulkerson
"""max_flow, residual_graph = ford_fulkerson(graph, n)
print("Flot maximal :", max_flow)
print("Graphe résiduel :", residual_graph)"""

# bellman_ford_min_cost(graph, n)
