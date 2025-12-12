import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self._list_rifugi = []
        self.get_all_rifugi()

        self._dict_rifugi = {}
        for r in self._list_rifugi:
            self._dict_rifugi[r.id] = r

        self.G = None
        self.list_weights = None

    def get_all_rifugi(self):
        self._list_rifugi = DAO.readAllRifugi()

    def fattore_difficolta(self, difficolta):
        if difficolta == 'facile':
            return 1
        elif difficolta == 'media':
            return 1.5
        elif difficolta == 'difficile':
            return 2
        else:
            return 0

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """

        self.G = nx.Graph()
        connessioni = DAO.readAllConnessioni(self._dict_rifugi, year)

        for c in connessioni:
            self.G.add_node(c.r1)
            self.G.add_node(c.r2)
            weight = float(c.distanza) * self.fattore_difficolta(c.difficolta)
            self.G.add_edge(c.r1, c.r2, weight=weight)

        #print(self.G)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        self.list_weights = []
        for r1, r2, w in self.G.edges(data=True):
            self.list_weights.append(w['weight'])

        return min(self.list_weights), max(self.list_weights)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        cnt_min = len([w for w in self.list_weights if w < soglia])
        cnt_max = len([w for w in self.list_weights if w > soglia])

        return cnt_min, cnt_max

    """Implementare la parte di ricerca del cammino minimo"""
    def find_shortest_path(self, soglia):
        # filtraggio del grafo secondo il valore del peso
        filtered_graph = nx.Graph()
        min = float('inf')
        r_partenza = None
        r_arrivo = None

        for r1, r2, w in self.G.edges(data=True):
            if w['weight'] > soglia:
                filtered_graph.add_edge(r1, r2, weight=w['weight'])

        fw = nx.floyd_warshall(filtered_graph)
        result = {a: dict(b) for a, b in fw.items()}

        for r1 in result:
            for r2 in result[r1]:
                if r1 == r2 or filtered_graph.has_edge(r1, r2) or result[r1][r2] >= min:
                    pass
                else:
                    min = result[r1][r2]
                    r_partenza = r1
                    r_arrivo = r2

        shortest_path_nodes = nx.shortest_path(filtered_graph, source=r_partenza, target=r_arrivo)
        shortest_path_edges = list(zip(shortest_path_nodes[:-1], shortest_path_nodes[1:]))
        return shortest_path_edges
