from graph import Graphique
from algorithms import *
import copy

def main():
    print("Bienvenue dans le programme de résolution de flots !")
    
    while True:
        # Demander à l'utilisateur de choisir un fichier
        while True:
            try:
                choix_fichier = int(input("\nEntrez un numéro entre 1 et 10: "))
                if 1 <= choix_fichier <= 10:
                    break
                else:
                    print("Veuillez entrer un nombre entre 1 et 10.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un nombre entre 1 et 10.")
        
        # Construire le chemin du fichier
        fichier = f"Propositions/Proposition {choix_fichier}.txt"
        print(f"Fichier sélectionné : {fichier}")
        
        # Charger le graphe
        try:
            graph = Graphique.read_graph(fichier)
            graph.display()
        except FileNotFoundError:
            print("Le fichier spécifié est introuvable. Assurez-vous que le fichier existe.")
            return
        
        # Demander à l'utilisateur de choisir un algorithme
        print("\nChoisissez un algorithme pour résoudre le problème :")
        print("1. Ford-Fulkerson")
        print("2. Push-Relabel")
        if graph.has_costs():
            print("3. Flot à coût minimal (Bellman-Ford)")
        
        while True:
            try:
                choix_algo = int(input("\nEntrez le numéro de l'algorithme: "))
                    
                if not graph.has_costs() and choix_algo in [1, 2]:
                    break
                elif graph.has_costs() and choix_algo in [1, 2, 3]:
                    break
                else:
                    print("Veuillez entrer un numéro valide.")
            except ValueError:
                print("Entrée invalide. Veuillez entrer un numéro valide.")

        # Exécuter l'algorithme choisi
        if choix_algo == 1:
            max_flow = ford_fulkerson(graph)
            graph.display_flow()
            print(f"\nFlot maximal avec l'algorithme Ford-Fulkerson : {max_flow}")
        elif choix_algo == 2:
            max_flow = push_relabel(graph)
            graph.display_flow()
            print(f"\nFlot maximal avec l'algorithme Push-Relabel : {max_flow}")
        elif choix_algo == 3:
            copy_graph = copy.deepcopy(graph)
            max_flow = ford_fulkerson(copy_graph)
            while True:
                try:
                    print(f"\nLe flot maximal est de {max_flow}.", end=" ")
                    target_flow = int(input("Entrez la valeur de flot cible : "))
                    if target_flow > 0 and target_flow <= max_flow:
                        break
                    else:
                        print("Veuillez entrer une valeur valide.")
                except ValueError:
                    print("Entrée invalide. Veuillez entrer une valeur entière valide.")
            
            total_cost = min_cost_flow(graph, target_flow)
            graph.display_flow()
            print(f"\nCoût total du flot : {total_cost}")

if __name__ == "__main__":
    main()
