class Graphique:
    def __init__(self, n):
        self.n = n
        self.capacity = [[0] * n for _ in range(n)]
        self.cost = [[0] * n for _ in range(n)]      # Cost matrix (optional)
        self.residual = [[0] * n for _ in range(n)]
        self.flow = [[0] * n for _ in range(n)]

    # Vérifie si le graphe a des coûts
    def has_costs(self):
        if self.cost is None:
            return False
        else:
            return True
    
    def add_edge(self, u, v, capacity):
        self.capacity[u][v] = capacity
        self.residual[u][v] = capacity

    @classmethod
    def read_graph(cls, filename):
        with open(filename, 'r') as file:
            # Read number of vertices
            n = int(file.readline().strip())
            
            # Create a FlowNetwork instance
            graph = cls(n)
            
            # Read capacity matrix
            for i in range(n):
                row = list(map(int, file.readline().strip().split()))
                graph.capacity[i] = row
            
            # Read optional cost matrix
            remaining_lines = file.readlines()
            if len(remaining_lines) == n:
                for i in range(n):
                    row = list(map(int, remaining_lines[i].strip().split()))
                    graph.cost[i] = row
            else:
                graph.cost = None  # No cost matrix provided

        # Initialize the residual matrix to match capacity initially
        graph.residual = [row[:] for row in graph.capacity]
        return graph

    def display_flow(self):
        
        flow = self.flow
        print("\n\n* Matrice des flots:\n")
        # Affiche l'en-tête de la matrice
        print("  ", end="")
        for i in range(len(flow)):
            if i < 10:
                print(" ", end="")
            if i == 0:
                print(f"  s", end="")
            elif i == len(flow)-1:
                print(f"  t", end="")
            else:
                print(f"  {chr(i+96)}", end="")
        print()
        
        # Parcourt chaque tâche pour créer les lignes de la matrice
        for i in range(len(flow)):
            # Si la tâche fait plus de 9, on ajuste l'espacement pour l'affichage
            if i == 0:
                print(f"s ", end="")
            elif i == len(flow)-1:
                print(f"t ", end="")
            else:
                print(f"{chr(i+96)} ", end="")
            
            # Vérifie si la tâche actuelle est un prédécesseur de task2
            for j in range(len(flow)):
                # Si la tâche fait plus de 9, on ajuste l'espacement pour l'affichage
                if flow[i][j] != 0:
                    if flow[i][j] < 10 and flow[i][j] > 0:
                        print(f"   {flow[i][j]}", end="")
                    else:
                        print(f"  {flow[i][j]}", end="")
                else:
                    print("   *", end="")
            print()

    def display(self):
        
        capacity = self.capacity
        print("\n* Matrice des capacités:\n")
        # Affiche l'en-tête de la matrice
        print("  ", end="")
        for i in range(len(capacity)):
            if i < 10:
                print(" ", end="")
            if i == 0:
                print(f"  s", end="")
            elif i == len(capacity)-1:
                print(f"  t", end="")
            else:
                print(f"  {chr(i+96)}", end="")
        print()
        
        # Parcourt chaque tâche pour créer les lignes de la matrice
        for i in range(len(capacity)):
            # Si la tâche fait plus de 9, on ajuste l'espacement pour l'affichage
            if i == 0:
                print(f"s ", end="")
            elif i == len(capacity)-1:
                print(f"t ", end="")
            else:
                print(chr(i+96), "", end="")
            
            # Vérifie si la tâche actuelle est un prédécesseur de task2
            for j in range(len(capacity)):
                # Si la tâche fait plus de 9, on ajuste l'espacement pour l'affichage
                if capacity[i][j] != 0:
                    if capacity[i][j] < 10:
                        print(f"   {capacity[i][j]}", end="")
                    else:
                        print(f"  {capacity[i][j]}", end="")
                else:
                    print("   *", end="")
            print()
            
        if self.cost:
            cost = self.cost
            print("\n\n* Matrice des prix:\n")
            # Affiche l'en-tête de la matrice
            print("  ", end="")
            for i in range(len(cost)):
                if i < 10:
                    print(" ", end="")
                if i == 0:
                    print(f"  s", end="")
                elif i == len(cost)-1:
                    print(f"  t", end="")
                else:
                    print(f"  {chr(i+96)}", end="")
            print()
            
            # Parcourt chaque tâche pour créer les lignes de la matrice
            for i in range(len(cost)):
                # Si la tâche fait plus de 9, on ajuste l'espacement pour l'affichage
                if i == 0:
                    print(f"s ", end="")
                elif i == len(cost)-1:
                    print(f"t ", end="")
                else:
                    print(f"{chr(i+96)} ", end="")
                
                # Vérifie si la tâche actuelle est un prédécesseur de task2
                for j in range(len(cost)):
                    # Si la tâche fait plus de 9, on ajuste l'espacement pour l'affichage
                    if cost[i][j] != 0:
                        if cost[i][j] < 10:
                            print(f"   {cost[i][j]}", end="")
                        else:
                            print(f"  {cost[i][j]}", end="")
                    else:
                        print("   *", end="")
                print()