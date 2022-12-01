from random import random
from random import randint

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
        a = e[0]
        b = e[1]
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
    except AssertionError:
        print("Probleme avec la fonction de contraction")

def test_karger():
    #On teste uniquement les graphes cycliques car la valeur d'une coupe minimale est toujours 2 peu importe les arêtes choisies
    cyclic_graph = create_cyclic_graph(5)

    l, e = karger(cyclic_graph)
    try:
        assert e == 2
    except AssertionError:
        print("Probleme avec la fonction de karger")

if __name__ == "__main__":
    test_contraction()
    test_karger()