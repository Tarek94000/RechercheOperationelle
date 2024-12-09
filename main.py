from graph import Graphique
from algorithms import *
from utils import *

def main():
    print("Bienvenue dans le programme de résolution de flots !")
    print("Veuillez choisir un numéro de fichier entre 1 et 10 pour sélectionner un problème.")
    
    # Prompt the user to choose a file
    while True:
        try:
            choix_fichier = int(input("Entrez un numéro entre 1 et 10: "))
            if 1 <= choix_fichier <= 10:
                break
            else:
                print("Veuillez entrer un nombre entre 1 et 10.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entre 1 et 10.")
    
    # Construct the file path
    fichier = f"fig/fig{choix_fichier}.txt"
    print(f"Fichier sélectionné : {fichier}")
    
    # Load the graph
    try:
        graph = Graphique.read_graph(fichier)
        graph.display()
    except FileNotFoundError:
        print("Le fichier spécifié est introuvable. Assurez-vous que le fichier existe.")
        return

    source, sink = 0, graph.n - 1  # Default source and sink nodes
    
    # Prompt the user to choose an algorithm
    print("\nChoisissez un algorithme pour résoudre le problème :")
    print("1. Ford-Fulkerson")
    print("2. Push-Relabel")
    if graph.has_costs():
        print("3. Flot à coût minimal (Bellman-Ford)")
    
    while True:
        try:
            choix_algo = int(input("Entrez le numéro de l'algorithme: "))
                
            if not graph.has_costs() and choix_algo in [1, 2]:
                break
            elif graph.has_costs() and choix_algo in [1, 2, 3]:
                break
            else:
                print("Veuillez entrer un numéro valide.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro valide (1-3).")

    # Execute the chosen algorithm
    if choix_algo == 1:
        max_flow = ford_fulkerson(graph, source, sink)
        print(f"\nFlot maximal avec l'algorithme Ford-Fulkerson : {max_flow}")
        graph.display_flow()
    elif choix_algo == 2:
        max_flow = push_relabel(graph, source, sink)
        print(f"\nFlot maximal avec l'algorithme Push-Relabel : {max_flow}")
        graph.display_flow()
    elif choix_algo == 3:
        while True:
            try:
                target_flow = int(input("Entrez la valeur de flot cible : "))
                if target_flow > 0:
                    break
                else:
                    print("Veuillez entrer une valeur positive.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer une valeur entière positive.")
        
        total_cost = min_cost_flow(graph, source, sink, target_flow)
        print(f"\nCoût total du flot : {total_cost}")
        graph.display_flow()

if __name__ == "__main__":
    main()
