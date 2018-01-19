# coding=utf-8
#   Autore: Matteo Esposito
#   Versione di Python: 3.6.4
#   Seconda Prova in Itinere
#   Implementazione dell'Algoritmo di Brandes per la Betweennes Centrality
#   Tempo di esecuzione stimato O(nm)


from ProjUtilities import generateAcycleGraph, generateCyclicGraph
from graph.mst import kruskal
from brandes import brandes
import time

DEBUG = True

def doTest(V,A,graph,i,d):
    """
    Funzione usata per fare il benchmarking, accetta i valori
    già convertiti V e A, mentre l'oggetto graph ed l'iteratore i
    sono passati per il puro scopo di profiling

    :param V: array contenente l'id di tutti i nodi
    :param A: lista di "adiacenza" leggermente modificata
    :param graph: IncidenceList(Extended)Graph - grafo
    :param i: i-esima iterazione
    :param d: int - Tipologia di Grafo
                    0: Aciclico
                    1: Ciclico

    :return: None
    """
    tempo_iniziale = time.time()

    #
    #   Chiamata all'Algortimo di Brades per il calcolo degli indici della
    #   Betweennes Centrality
    #   l'algoritmo da me adattato alle nostrte esigenze ritonra con una tripla di elementi:
    #   [0]: Indice Massimo di Betweennes Centrality
    #   [1]: Id del nodo associalo all'Indice Massimo
    #   [2]: Dizionario con Chiave: ID del nodo
    #                       Valore: Indice di Betweennes Centrality
    #
    brandes(V, A)[1]
    tempo_finale = time.time()

    type = ""
    if d==0:
        type = "Aciclico"
    else:
        type = "Ciclico"

    print("Test N:", str(i), ",", str(tempo_finale - tempo_iniziale), ", secondi,", "numero di nodi: ", str(graph.numNodes()),", numero di archi: ",str(graph.numEdges()),", |V|*|E| = ",str(graph.numNodes()*graph.numEdges()), ", Tipologia: ", type)#, ", differenza di elementi: ", str(diff), "elementi totali: ", str(eltot), ", albero maggiore: ", d


def prepBenchmark(n,i,d):
    """
    Funzione per la preparazione del Benchmark
    si occupa di generare un grafo e di convertire le informazioni
    in esso contenute nella configurazione di strutture dati per l'algoritmo
    di Brandes
    :param n: int - numero di nodi
    :param i: int - i-esima itreazione
    :param d: int - tiplogia di Grafo
                    0: Aciclico
                    1: Ciclico
    :return: None
    """

    #   Genero un grafo come Lista di Incidenza
    #   usando però la versione modificata ed impementata
    #   in ProjUtilities.py

    #   graph = GraphIncidenceList()

    #   In base al parametro d
    #   scelgo se generare un grafico
    #   ciclico o aciclico
    if d == 0:
        #   Genero un grafo Aciclico
        graph = generateAcycleGraph(n)


        #   Dalla nuova versione, il grafo viene inizializzato con tutti i nodi connessi
        #   a tutti con pesi però randomici, allora ora mi genero una Minimo Albero Ricoprente
        #   sfruttando Kruskal e la sua implementazione che restituisce una lista di archi
        w_kruskal, mst_kruskal = kruskal(graph)

        if DEBUG:
            print("\tWeight:", w_kruskal)
            print("\tMST:", [str(item) for item in mst_kruskal])

        #   Elimino tuti gli archi dal grafo originale
        for edge in graph.getEdges():
            graph.deleteEdge(edge.tail, edge.head)

        #   Ora riconnetto il grafo con gli archi del suo Minimo Albero Ricoprente
        #   secondo l'invocazione precedente dell'algorimto di Kruskal
        for edge in mst_kruskal:
            graph.insertEdge(edge.tail, edge.head, edge.weight)

        if DEBUG:
            print("Num Nodes:", graph.numNodes())
            print("Num Edges:", graph.numEdges())

        #   Ottengo la tupla;
        #   V:= lista dei nodi
        #   A:= lista dei nodi collegati
        V, A = graph.convertToBradesGraphAlgo()  # Conversion Method

        if DEBUG:
            print("V = Nodes List \t A = Dictionary( node:[n1,n2,n3,...] ... )")
            print(V, A)

        doTest(V,A,graph,i,d)

    else:
        #   Genero un grafo ciclico
        graph = generateCyclicGraph(n)

        if DEBUG:
            print("Num Nodes:", graph.numNodes())
            print("Num Edges:", graph.numEdges())

        #   Ottengo la tupla;
        #   V:= lista dei nodi
        #   A:= lista dei nodi collegati
        V, A = graph.convertToBradesGraphAlgo()  # Conversion Method

        if DEBUG:
            print("V = Nodes List \t A = Dictionary( node:[n1,n2,n3,...] ... )")
            print(V, A)

        doTest(V,A,graph,i,d)


def benchmark(n,d):
    """

    :param n: int - numero di iterazioni
    :param d: Tipologia di grafo
              0: Aciclico
              1: Ciclico
    :return: None
    """
    while n > 0:
        nds = 10*n +n//2
        prepBenchmark(nds, n, d)
        n = n-1

def testWithCycle(n):
    """
    Leftover dei test iniziali, lasciato a testimonianza
    :param n: int - numero di nodi
    :return: None
    """
    graph = generateCyclicGraph(n)
    if DEBUG:
        graph.print()
    V, A = graph.convertToBradesGraphAlgo()
    if DEBUG:
        print(V,A)
    print(brandes(V,A))

if __name__ == "__main__":
    DEBUG = False

    #   Scegliere la tipologia di test:
    #       0: Test rapido manuale
    #       1: Benchmark completo ( vedere giù per i settaggi )
    test_type = 0

    if test_type == 0:

        V = [0, 1, 2, 3,4]

        #A = {0: [ 2, 3, 4], 1: [0, 2,  4], 2: [0, 1, 3, ], 3: [0, 1, 2, 4], 4: [0, 1, 2, 3]}
        A = {0: [1], 1: [0, 2,3], 2: [1, 3], 3: [2,4], 4: [3]}
        # V = [1]
        #A = {1:[1]}
        # V = []
        # A = {}

        #   Grafi della Relazione:

        #   Aciclico
        #   V = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        #   A = {0: [1, 8], 1: [0, 12, 13], 2: [7, 18, 8, 6], 3: [4], 4: [8, 14, 5, 3], 5: [4, 10, 11], 6: [2], 7: [27, 2, 9], 8: [2, 4, 0], 9: [7], 10: [5], 11: [5], 12: [1], 13: [1], 14: [4, 15], 15: [14, 16, 17], 16: [15], 17: [15], 18: [20, 19, 2], 19: [18, 21, 23, 25], 20: [26, 22, 24, 18], 21: [19], 22: [20],23: [19], 24: [20], 25: [19], 26: [20], 27: [7]}

        # Ciclico
        #   V = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        #   A = {0:[1, 5], 1: [2, 0, 4, 8], 2: [7, 1, 8, 3], 3: [2, 8, 4, 6], 4: [8, 1, 5, 3], 5: [4, 0], 6: [7, 3], 7:[2,6], 8: [2, 1, 4, 3]}

        print(V,A)
        print("\n")
        print(brandes(V,A))
    else:
        #   Numero di Test
        n = 100

        #   Tiplogia di Grafo:
        #       0: Grafo Aciclico
        #       1: Grafo Ciclico
        d = 0

        #   Inizia Benchmarking dell'algoritmo
        benchmark(n,d)

