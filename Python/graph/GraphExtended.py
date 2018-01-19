from graph.Graph import GraphBase


class GraphExtended(GraphBase):
    def __init__(self):
        super(GraphExtended, self).__init__()

    def convertToBradesGraphAlgo(self):
        """
        Funzione per la generazione di una tipologia diversa di lista
        Questa funzione è essenzialmente un "convertitore" di lista di incidenza

        :return: Dizionario di liste
                 lista di Incidenza modificata per l'Algoritmo di Brandes
                 dal Nodo: [al nodo1, n2,n3,...]
        """
        A = {}
        for inc_item in self.inc.items():
            edg = []
            for edges in inc_item[1]:
                edg.append(edges.head)
            A[inc_item[0]] = edg

        V = []
        for i in self.getNodes():
            V.append(i.id)
        return V, A