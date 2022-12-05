from random import random
from random import randint
from adjacency_matrix_syntaxe import EdgesIdentifierError
from math import sqrt
from copy import deepcopy

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

        """
            On a supprimé le sommet b, il faut donc décrémenter les sommets qui sont > b
            
            x(int) -> valeur de l'élément de la liste
            b(int) -> numéro du sommet supprimé
            
            return(int) -> nouvelle valeur de l'élément
        """
        def decrease(x, b):
            if x > b:
                x -= 1
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
            #on décrémente tous les indices qui sont > à b
            self.adjacency_list[i] = sorted(list(map(lambda x: decrease(x, b), self.adjacency_list[i])))

        #on supprime toutes les arêtes (a, a) pour éviter les cycles
        self.adjacency_list[a] = list(filter(lambda x: x != a, self.adjacency_list[a]))

    """
       Réalise la contraction partielle d'un graphe
           
       g(Graphe) -> Le graphe
       t(int) -> nombre max de sommets du graphe à la sortie de la fonction
       nb_vertex(int) -> nombre de sommets du graphe
       nb_edges(int) -> nombre d'arêtes du graphe
           
       return(int) -> le nombre d'arêtes du graphe
   """
    def partial_contraction(self, t, nb_vertex, nb_edges):
        while nb_vertex > t:
            #tirage aléatoire d'une arête
            id_edges = randint(0, nb_edges - 1)
            e = self.get_edges_from_id(id_edges)
            #contraction de l'arête e dans g
            self.contraction(e)
            #mise à jour du nombre de sommet et d'arête du graphe
            nb_vertex -= 1
            nb_edges = self.get_nb_edges()
        return nb_edges

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
        Renvoie l'arête du graphe qui correspond à un identifiant
        
        id_edges(int) -> identifiant de l'arête
        
        return(int, int) -> l'arête correspondante
    """
    def get_edges_from_id(self, id_edges):
        #controle erreur
        if id_edges >= self.get_nb_edges():
            raise EdgesIdentifierError(id_edges, "get_edges_from_id(liste d'adjacence)")

        #chaque arêtes apparaît 2 fois donc on décide de multiplier l'identifiants recherché par 2
        id_edges *= 2

        for i in range(self.get_nb_edges()):
            if len(self.adjacency_list[i]) == 0:
                continue
            elif (len(self.adjacency_list[i]) - 1) < id_edges:
                id_edges -= len(self.adjacency_list[i])
            else:
                return tuple(sorted((i, self.adjacency_list[i][id_edges])))

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

    FONCTIONS DE KARGER

"""

"""
    Réalise l'algorithme de karger à partir d'un graphe 
    
    g -> Le graphe 
    
    return(list, int) -> tuple (liste des sommets de v1, la valeur de la coupe minimale)
"""
def karger(g):
    #initialisation du nombre de sommets, du nombre d'aretes dans le graphe et d'une liste qui regroupe les sommets qui fusionneront
    nb_vertex = g.get_nb_vertex()
    nb_edges = g.get_nb_edges()
    merged_vertex = [[i] for i in range(nb_vertex)]

    while nb_vertex > 2:
        #contraction
        id_edges = randint(0, nb_edges - 1)
        e = g.get_edges_from_id(id_edges)
        a, b = e
        remove_edges = g.adjacency_list[a].count(b) #nombres d'aretes qui seront supprimés du graphe
        g.contraction(e)

        #fusion de la liste a avec la liste b
        merged_vertex[a] += merged_vertex[b]

        #suppression de la liste b qui correspond au sommet qui a fusionné
        merged_vertex.pop(b)

        #on décrémente le nombre de sommet et le nombre d'arête du graphe
        nb_edges -= remove_edges
        nb_vertex -= 1
    return (merged_vertex[0], nb_edges)

"""
   Réalise l'algorithme de karger T fois
   
   g(Graphe) -> Le graphe 
   T(int) -> Le nombre d'itération
   
   return(list, int) -> tuple (liste des sommets de v1, la valeur de la coupe minimale)
"""
def iterated_karger(g, t):
    total_min_cut_size = -1
    min_cut_size = []

    for i in range(t):
        tmp_min_cut_size, nb_edges = karger(deepcopy(g))
        if total_min_cut_size == -1 or (nb_edges < total_min_cut_size):
            total_min_cut_size = nb_edges
            min_cut_size = tmp_min_cut_size

    return(min_cut_size,total_min_cut_size)

"""
   Réalise l'algorithme de karger Stein
   
   g(Graphe) -> Le graphe 
   nb_vertex(int) -> le nombre de sommet du graphe
   nb_edges(int) -> le nombre d'arête du graphe
   
   return(list, int) -> tuple (liste des sommets de v1, la valeur de la coupe minimale)
"""
def karger_stein(g,nb_vertex,nb_edges):
    if(nb_vertex <= 6):
        merged_vertex, min_cut_size = karger(g)
        return (merged_vertex, min_cut_size)

    # t = 1+ #V/sqrt(2)
    t = int((1 + nb_vertex / sqrt(2)) + 0.99)

    #création de g1
    g1 = deepcopy(g)
    nb_vertex_g1 = nb_vertex
    nb_edges_g1 = nb_edges

    #g1 = contraction_partielle(g, t)
    g1.partial_contraction(t, nb_vertex_g1, nb_edges_g1)
    nb_vertex_g1 = g1.get_nb_vertex()
    nb_edges_g1 = g1.get_nb_edges()

    #s1, m1 = kargerStein(g1)
    s1, m1 = karger_stein(g1, nb_vertex_g1, nb_edges_g1)

    #création de g2
    g2 = deepcopy(g)
    nb_vertex_g2 = nb_vertex
    nb_edges_g2 = nb_edges

    #g2 = contraction_partielle(g, t)
    g2.partial_contraction(t, nb_vertex_g2, nb_edges_g2)
    nb_vertex_g2 = g2.get_nb_vertex()
    nb_edges_g2 = g2.get_nb_edges()

    #s2, m2 = kargerStein(g2)
    s2, m2 = karger_stein(g2, nb_vertex_g2, nb_edges_g2)

    #test sur les valeurs de m1 et m2
    if m1 < m2:
        return (s1, m1)
    else:
        return (s2, m2)
    

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
        assert cyclic_graph.adjacency_list == [[1, 3], [0, 2], [1, 3], [0, 2]]
        assert complete_graph.adjacency_list == [[1, 1, 2], [0, 0, 2, 2], [0, 1, 1]]
        assert complete_bipartie_graph.adjacency_list == [[1, 2, 3, 4], [0, 3, 4], [0, 3, 4], [0, 1, 2], [0, 1, 2]]
        print("L'algorithme de contraction fonctionne\n")
    except AssertionError:
        print("Probleme avec la fonction de contraction")

def test_karger():
    #On teste uniquement les graphes cycliques car la valeur d'une coupe minimale est toujours 2 peu importe les arêtes choisies
    cyclic_graph = create_cyclic_graph(5)

    l, e = karger(cyclic_graph)
    try:
        assert e == 2
        print("L'algorithme de karger fonctionne\n")
    except AssertionError:
        print("Probleme avec la fonction de karger")

def test_iterated_karger():
    complete_graphe = create_complete_graph(30)
    l, e = iterated_karger(complete_graphe, 100)
    try:
        assert e == 29
        print("L'algorithme de karger itere fonctionne\n")
    except AssertionError:
        print("Probleme avec la fonction de iterated_karger")

def test_karger_stein():
    complete_graphe = create_complete_graph(20)
    l, e = karger_stein(complete_graphe, complete_graphe.get_nb_vertex(), complete_graphe.get_nb_edges())
    try:
        assert e == 19
        print("L'algorithme de karger stein fonctionne\n")
    except AssertionError:
        print("Probleme avec la fonction de iterated_karger")

if __name__ == "__main__":
    print("\n")
    test_contraction()
    test_karger()
    test_iterated_karger()
    test_karger_stein()
