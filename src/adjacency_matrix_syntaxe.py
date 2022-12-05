from random import random
from random import randint
from math import sqrt
from copy import deepcopy

"""
    Exception qui se lance lorsqu'on cherche un identifiant d'une arête qui n'existe pas dans le graphe
"""
class EdgesIdentifierError(Exception):
    """
        Constructeur:
            s -> l'argument passé en paramètre de la fonction
            f -> la fonction dans laquelle l'exception a été levée
    """
    def __init__(self, s, f = ""):
        Exception.__init__(self, s)
        self.s = s
        self.f = f

    """
        Fonction d'affichage
    """
    def __str__(self):
        return "exception \"EdgesIdentifierError\" lancée depuis la fonction \" " + self.f + \
               "\" avec le paramètre " + self.s

"""
    Graphe représenté par sa matrice d'adjacence
"""
class Graphe:
    def __init__(self, matrix):
        self.matrix = matrix

    """
        Contracte une arête
        e -> arête représenté par un table (a, b) 
    """
    def contraction(self, e):
        #on suppose qu'on supprime le sommet 'b' du graphe et qu'on garde le sommet 'a'
        (a, b) = e
        length = len(self.matrix)

        #fusionnage des arrêtes
        for i in range(length):
            self.matrix[a][i] += self.matrix[b][i]
        for i in range(length):
            self.matrix[i][a] += self.matrix[i][b]
        self.matrix[a][a] = 0

        #suppression d'un sommet (b)
        self.matrix.pop(b)
        for  i in range(length - 1):
            self.matrix[i].pop(b)

    """
        Réalise la contraction partielle d'un graphe
            
        g(Graphe) -> Le graphe
        t(int) -> nombre max de sommets du graphe à la sortie de la fonction
        nb_vertex(int) -> nombre de sommets du graphe
        nb_edges(int) -> nombre d'arêtes du graphe
            
        return(int) -> le nombre d'arêtes du graphe
    """
    def partial_contraction(self, t, nb_vertex, nb_edges):
        while(nb_vertex > t):
            #selection d'une arête aléatoire
            id_edges = randint(0, nb_edges - 1)
            e = self.get_edges_from_id(id_edges)
            a, b = e
            #contraction de l'arête
            remove_edges = self.matrix[a][b] #nombres d'aretes qui seront supprimés du graphe
            self.contraction(e)
            #mise à jour du nombre de sommet et du nombre d'arête du graphe
            nb_edges -= remove_edges
            nb_vertex -= 1
        return nb_edges

    """
        Renvoie le nombre de sommets dans le graphe
    """
    def get_nb_vertex(self):
        return len(self.matrix)

    """
        renvoie le nombre d'arêtes dans le graphe
    """
    def get_nb_edges(self):
        edges = 0
        for i in range(self.get_nb_vertex()):
            edges += sum(self.matrix[i])
        return edges // 2

    """
        Renvoie l'arête du graphe qui correspond à un identifiant
        
        id_edges(int) -> identifiant de l'arête
        
        return(int, int) -> l'arête correspondante
    """
    def get_edges_from_id(self, id_edges):
        #controle erreur
        if id_edges >= self.get_nb_edges():
            raise EdgesIdentifierError(id_edges, "get_edges_from_id")

        c = 0 #identifiant de l'arête courante
        for i in range(self.get_nb_vertex()):
            for j in range(i, self.get_nb_vertex()):
                #on incrémente notre identidiant de l'arête courante à chaque fois qu'on visite une arête
                for k in range(self.matrix[i][j]): #attention on est dans le cas d'un multi graphe
                    if c == id_edges:
                        return (i, j)
                    c += 1

"""
    CREATION DE GRAPHE
    
"""

"""
    Créer une matrice d'adjacence d'un graphe de taille 'length' sans arête
    
    length(int) -> nombre de sommets du graphe
    
    return(list[]) -> La matrice d'adjacence du graphe
"""
def create_matrix(length):
    matrix = [0] * length
    for i in range(length):
        matrix[i] = [0] * length
    return matrix

"""
    Créer un graphe cyclique de taille 'length'
    
    length(int) -> nombre de sommets du graphe
    
    return(Graphe) -> Le graphe résultant
"""
def create_cyclic_graph(length):
    matrix = create_matrix(length)

    for i in range(length):
        for j in range(length):
            if i - j == 1 or i - j == -1 or (i == 0 and j == length - 1) or (i == length - 1 and j == 0):
                matrix[i][j] = 1
    return Graphe(matrix)

"""
    Créer un graphe complet de taille 'length'
    
    length(int) -> nombre de sommets du graphe
    
    return(Graphe) -> Le graphe résultant
"""
def create_complete_graph(length):
    matrix = create_matrix(length)

    for i in range(length):
        for j in range(length):
            if i != j:
                matrix[i][j] = 1
    return Graphe(matrix)

"""
    Créer un graphe bipartie complet de taille 'length'
    
    length(int) -> nombre de sommets du graphe
    
    return(Graphe) -> Le graphe résultant
"""
def create_complete_bipartie_graphe(length):
    matrix = create_matrix(length)

    k = length // 2
    for i in range(k):
        for j in range(length - 1, k - 1, -1):
            matrix[i][j] = 1
            matrix[j][i] = 1

    return Graphe(matrix)

"""
    Créer un graphe de taille 'length' où chaque arête apparaît avec une probabilité 'probability'
    
    length(int) -> nombre de sommets du graphe
    probability(float compris entre 0 et 1) -> probabilité d'apparition de chaque arête
    
    return(Graphe) -> Le graphe résultant
"""
def create_random_graph(length, probability):
    matrix = create_matrix(length)

    for i in range(length):
        for j in range(length):
            if i != j and random() < probability:
                matrix[i][j] = 1
    return Graphe(matrix)

"""

    FONCTIONS DE KARGER

"""

"""
    Réalise l'algorithme de karger à partir d'un graphe 
    
    g(Graphe) -> Le graphe 
    
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
        remove_edges = g.matrix[a][b] #nombres d'aretes qui seront supprimés du graphe
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

    complete_bipartie_graphe = create_complete_bipartie_graphe(6)
    complete_bipartie_graphe.contraction((0, 4))

    try:
        assert cyclic_graph.matrix == [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
        assert complete_graph.matrix == [[0, 2, 1], [2, 0, 2], [1, 2, 0]]
        assert complete_bipartie_graphe.matrix == [[0, 1, 1, 1, 1], [1, 0, 0, 1, 1], [1, 0, 0, 1, 1], [1, 1, 1, 0, 0], [1, 1, 1, 0, 0]]
        print("La contraction fonctionne\n")
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
    complete_graphe = create_complete_graph(50)
    l, e = iterated_karger(complete_graphe, 100)
    try:
        assert e == 49
        print("L'algorithme de karger itere fonctionne\n")
    except AssertionError:
        print("Probleme avec la fonction de iterated_karger")

def test_karger_stein():
    complete_graphe = create_complete_graph(200)
    l, e = karger_stein(complete_graphe, complete_graphe.get_nb_vertex(), complete_graphe.get_nb_edges())
    try:
        assert e == 199
        print("L'algorithme de karger stein fonctionne\n")
    except AssertionError:
        print("Probleme avec la fonction de iterated_karger")

if __name__ == "__main__":
    print("\n")
    test_contraction()
    test_karger()
    test_iterated_karger()
    test_karger_stein()
