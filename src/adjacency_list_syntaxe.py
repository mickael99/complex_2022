from random import random
from random import randint

"""
    Graphe représenté par sa liste d'adjacence
"""
class Graphe:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    """
        Contracte une arête
        
        e -> arête représenté par un table (a, b) 
    """
    def contraction(self, e):
        """
            Remplace tous les élement de la liste qui vaut b par a (utiliser lors de la fusion des sommets a et b)
            le sommet b est alors supprimé

            x(int) -> valeur de l'élément de la liste
            a(int) -> numéro du sommet
            b(int) -> numéro du sommet à supprimer

            return(int) -> nouvelle valeure de l'élément
        """
        def replace_b_by_a(x, a, b):
            if x == b:
                x = a
            return x

        #on suppose qu'on supprime le sommet 'b' du graphe et qu'on garde le sommet 'a' tel que a < b
        (a, b) = sorted(e)
        length = len(self.adjacency_list)

        #fusionnage des sommets a et b
        self.adjacency_list[a] += self.adjacency_list[b]

        #suppression du sommet b
        self.adjacency_list.pop(b)
        for i in range(length - 1):
            #le sommet 'b' n'existe plus car il a fusionné avec le sommet 'a' donc on remplace tous les sommets 'b' par 'a'
            self.adjacency_list[i] = sorted(list(map(lambda x: replace_b_by_a(x, a, b), self.adjacency_list[i])))

        #on supprime toutes les arêtes (a, a) pour éviter les cycles
        self.adjacency_list[a] = list(filter(lambda x: x != a, self.adjacency_list[a]))

    """
        Renvoie le nombre de sommets dans le graphe
    """
    def get_nb_vertex(self):
        return len(self.adjacency_list)

    """
        renvoie le nombre d'arêtes dans le graphe
    """
    def get_nb_edges(self):
        edges = 0
        for i in range(self.get_nb_vertex()):
            edges += len(self.adjacency_list[i])
        return edges // 2

"""

    CREATION DE GRAPHE
    
"""

"""
    Créer une liste d'adjacence d'un graphe de taille 'length' sans arête
    
    length(int) -> nombre de sommets du graphe
    
    return(list[]) -> La liste d'adjacence du graphe
"""
def create_empty_list(length):
    #Obligatoire de faire cela dans une boucle car [] * length ne fonctionne pas
    adjacency_list = [0] * length
    for i in range(length):
        adjacency_list[i] = []
    return adjacency_list

"""
    Créer un graphe cyclique de taille 'length'
    
    length(int) -> nombre de sommets du graphe
    
    return(Graphe) -> Le graphe résultant
"""
def create_cyclic_graph(length):
    adjacency_list = create_empty_list(length)

    for i in range(length):
        adjacency_list[i] += [(i + 1) % length]
        adjacency_list[i] += [(i - 1) % length]

    return Graphe(adjacency_list)

"""
    Créer un graphe complet de taille 'length'
    
    length(int) -> nombre de sommets du graphe
    
    return(Graphe) -> Le graphe résultant
"""
def create_complete_graph(length):
    adjacency_list = create_empty_list(length)

    for i in range(length):
        for j in range(length):
            if i != j:
                adjacency_list[i] += [j]

    return Graphe(adjacency_list)

"""
    Créer un graphe bipartie complet de taille 'length'
    
    length(int) -> nombre de sommets du graphe
    
    return(Graphe) -> Le graphe résultant
"""
def create_complete_bipartie_graph(length):
    adjacency_list = create_empty_list(length)

    k = length // 2
    for i in range(k):
        for j in range(length - 1, k - 1, -1):
           adjacency_list[i] += [j]
           adjacency_list[j] += [i]

    return Graphe(adjacency_list)

"""
    Créer un graphe de taille 'length' où chaque arête apparaît avec une probabilité 'probability'
    
    length(int) -> nombre de sommets du graphe
    probability(float compris entre 0 et 1) -> probabilité d'apparition de chaque arête
    
    return(Graphe) -> Le graphe résultant
"""
def create_random_graph(length, probability):
    adjacency_list = create_empty_list(length)

    for i in range(length):
        for j in range(i, length):
            if i != j and random() < probability:
                adjacency_list[i] += [j]
                adjacency_list[j] += [i]
    return Graphe(adjacency_list)

"""

    FONCTIONS DE TESTES

"""
def test_contraction():
    cyclic_graph = create_cyclic_graph(5)
    cyclic_graph.contraction((2, 3))

    complete_graph = create_complete_graph(4)
    complete_graph.contraction((1, 2))

    complete_bipartie_graph = create_complete_bipartie_graph(6)
    complete_bipartie_graph.contraction((0, 4))

    try:
        assert cyclic_graph.adjacency_list == [[1, 4], [0, 2], [1, 4], [0, 2]]
        assert complete_graph.adjacency_list == [[1, 1, 3], [0, 0, 3, 3], [0, 1, 1]]
        assert complete_bipartie_graph.adjacency_list == [[1, 2, 3, 5], [0, 3, 5], [0, 3, 5], [0, 1, 2], [0, 1, 2]]
    except AssertionError:
        print("Probleme avec la fonction de contraction")


if __name__ == "__main__":
    test_contraction()
