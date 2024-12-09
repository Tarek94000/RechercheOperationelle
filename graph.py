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
        print("Flow matrix:")
        for row in self.flow:
            print(row)
    
    def display(self):
        """
        Displays the graph's capacity and cost matrices.
        """
        print("Capacity matrix:")
        for row in self.capacity:
            print(row)
        if self.cost:
            print("\nCost matrix:")
            for row in self.cost:
                print(row)
        else:
            print("\nNo cost matrix.")
