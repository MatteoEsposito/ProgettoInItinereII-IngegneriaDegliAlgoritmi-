# coding=utf-8
#   Autore dell'Implementazione: Matteo Esposito ( riscrittura dallo Pseudo Codice )
#   Autore Originale dell'ALgoritmo: Ulrik Brandes ( Univeristy of Konstanz )
#   Modifiche: Matteo Esposito

from collections import deque

def brandes(V, A):
    """
    Calcola la Betweennes Centrality per Grafi non pesati Ciclici ed Aciclici.

    :param V: Array - Contentente tutti gli id dei nodi
    :param A: Dizionari - Dizionario contenente:
                            Chiave: Id Nodo
                            Valore: Nodi Incidenti con il nodo in questione
    :time O(|V|*|E|) ~ O(nm) ~= O(n^2)
    :return:

    int - max_node_value: Valore Massimo di Betweennes Centrality
    set - result: insieme degli id dei nodi che posseggono il massimo come loro indice di Betweennes Centrality
    dictionary - C: Dizionario contente:                    <---- Unico Output originale dell'Algoritmo
                    Chiave: ID Nodo
                    Valore: Indice di Betweennes Cenrtrality
    """

    #   L'algoritmo fa alcuni brevi test per poter fornire una rispota coerente e veloce in casi particolari
    if not V:
        return None, {}, {}

    if len(V) == 1: # O(1), https://wiki.python.org/moin/TimeComplexity
        return 0, {V[0]}, {V[0]:[0]}

    #   Inizializzo alcune variabili utili per il return finale ( aggiunta rispetto all'algoritmo originale )
    max_node_value = 0
    max_node_id = 0
    result = set([max_node_id])

    # Inizializzo il Dizionario C con gli id dei nodi come sue chiavi
    R = dict((v, 0) for v in V)

    # Eseguo tutte le seguneti operazioni per ogni singolo vertice del grafo
    for s in V:
        #   Nome della Variabile nell'implementazione   Nome della Variabile nel Paper di Brandes
        S = []                                          #   Pila -> Pila contenente i nodi del grafo in ordine
                                                        #           non crescente di distanza(sorgente, nodo)
        P = dict((w, []) for w in V)                    #   P[w] -> Dizionario di predecessori sui cammini minimi dalla
                                                        #           sorgente

        σ = dict((t, 0) for t in V)                     #   σ[t] -> Numero di cammini minimi σ[s,v]
        σ[s] = 1
        d = dict((t, -1) for t in V)                    #   d[t] -> Dipendenza della sorgente verso ogni nodo del grafo
        d[s] = 0

        Q = deque([])                                   #   Coda
        Q.append(s)

        #   L'algoritmo necessita di avere informazioni su tutti i possibili
        #   cammini minimi legati a ciascun nodo, essenzialmente implementiamo
        #   una simil-BFS
        #   Time Complexity per grafi non pesati O(m)
        while Q:
            v = Q.popleft()
            S.append(v)

            # Ora comincio ad iterare su tutti i vicini di A[v]
            for w in A[v]:

                #   Se trovo per la prima volta il nodo d[w]
                #   allora lo appendo alla coda Q ed
                #   incremento il valora di dipendenza della
                #   sorgente dal nodo in esame

                if d[w] < 0:
                    Q.append(w)
                    d[w] = d[v] + 1

                #   Ora mi chiedo se effettivamente
                #   l'arco in esame si trova su un cammino minimo
                #   in caso affermativo aggiungo tale nodo alla lista dei predecessori
                if d[w] == d[v] + 1:
                    σ[w] = σ[w] + σ[v]
                    P[w].append(v)

        δ = dict((v, 0) for v in V)

        #   Passiamo ora alla "propagazione" della "dependency" dei nodi
        #   nella pila S per poi concludere con il computo
        #   della somma di tutti i valori di dipendenza
        #   Time Complexity per grafi non pesati: O(m)
        while S:

            #   La pila S restituisce i vertici in ordine di distanza non-crescente dal nodo s
            w = S.pop()

            #   Calcolo la "dependency" tra s ed ogni vertice w presente in P
            for v in P[w]:
                δ[v] = δ[v] + (σ[v]/σ[w]) * (1 + δ[w])

                if w != s:
                    R[w] = R[w] + δ[w]

                #   Modifiche all'algoritmo originale:
                #   -> aggiunta del check sul valore massimo
                #   -> aggiunta del'insieme dei nodi di valore massimo
                #   -> modificata quindi la tipologia di struttra dati del return

                if max_node_value == R[w] and max_node_value != 0:
                    result.update([w])
                    #   L'algoritmo, ovviamente, risente di questa oeprazione in quanto
                    #   la complessità di questa operazione è O(len(result))
                    #   ma il "caso peggiore" cioè N non potrà mai verificarsi
                    #   poichè nel caso peggiore, grafo completamente connesso
                    #   l'algoritmo non esegue alcuna di queste operazioni.


                if max_node_value < R[w]:
                    max_node_value = R[w]
                    max_node_id = w
                    result = set([max_node_id])

    return max_node_value, result, R
