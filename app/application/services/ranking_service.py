import networkx as nx
import numpy as np
import networkx as nx

from app.domain.models import Review

from collections import defaultdict


class RankingService:
    def create_graph(self, reviews):
        """
        Crea un grafo bipartito a partir de las reseñas de usuarios.

        Este grafo representa las relaciones entre usuarios y productos (juegos).
        Los nodos representan usuarios y productos, y las aristas representan las reseñas.

        Args:
        reviews (list): Una lista de objetos de reseña, cada uno con atributos user_id, product_id, sentiment, y votes.

        Returns:
        networkx.Graph: Un grafo bipartito donde los nodos son usuarios y productos, y las aristas son reseñas ponderadas.

        Note:
        El peso de cada arista se calcula basado en el sentimiento y los votos de la reseña.
        """
        G = nx.Graph()

        for row in reviews:
            G.add_node(row.user_id, bipartite=0)
            G.add_node(row.product_id, bipartite=1)

            weight = (row.sentiment + 1) / 2 * (row.votes / 5)
            G.add_edge(row.user_id, row.product_id, weight=weight)

        return G

    def get_similar_users(self, G, user_id, game_id):
        """
        Encuentra usuarios similares que han revisado el mismo juego.

        Args:
        G (networkx.Graph): El grafo bipartito de usuarios y productos.
        user_id (str): El ID del usuario actual.
        game_id (str): El ID del juego actual.

        Returns:
        set: Un conjunto de IDs de usuarios que han revisado el mismo juego, excluyendo al usuario actual.
        """
        similar_users = set(G.neighbors(game_id)) - {user_id}
        return similar_users

    def personalized_pagerank(self, G, user_id, game_id):
        """
        Ejecuta un PageRank personalizado en el grafo.

        Este método da más importancia a los usuarios similares que han revisado el mismo juego.

        Args:
        G (networkx.Graph): El grafo bipartito de usuarios y productos.
        user_id (str): El ID del usuario actual.
        game_id (str): El ID del juego actual.

        Returns:
        dict: Un diccionario donde las claves son los IDs de los nodos y los valores son sus puntuaciones de PageRank.
        """
        similar_users = self.get_similar_users(G, user_id, game_id)

        personalization = defaultdict(float)
        for user in similar_users:
            personalization[user] = 1.0

        pagerank = nx.pagerank(G, personalization=personalization)
        return pagerank

    def rank_reviews(self, reviews, user_id, game_id, top_n=10):
        """
        Clasifica las reseñas para un juego específico basándose en su relevancia para un usuario dado.

        Este método utiliza un PageRank personalizado y otros factores para calcular un puntaje
        de relevancia para cada reseña.

        Args:
        reviews (list): Una lista de objetos de reseña.
        user_id (str): El ID del usuario para el que se están clasificando las reseñas.
        game_id (str): El ID del juego para el que se están clasificando las reseñas.
        top_n (int, optional): El número de reseñas top a devolver. Por defecto es 10.

        Returns:
        list: Una lista de tuplas (score, review) de las top_n reseñas más relevantes, ordenadas por puntuación descendente.

        Note:
        La puntuación de cada reseña se calcula basándose en el rank del revisor (del PageRank personalizado),
        el sentimiento de la reseña y su utilidad (basada en el campo 'helpful').
        """
        G = self.create_graph(reviews)
        pagerank = self.personalized_pagerank(G, user_id, game_id)

        scored_reviews = []
        for review in reviews:
            reviewer_rank = pagerank.get(review.user_id, 0)
            sentiment_score = (review.sentiment + 1) / 2
            helpful = [int(x) for x in review.helpful[1:-1].split(', ')]
            helpfulness = helpful[0] / max(helpful[1], 1)

            score = (reviewer_rank + sentiment_score + helpfulness) / 3
            scored_reviews.append((score, review))

        scored_reviews.sort(reverse=True, key=lambda x: x[0])

        return scored_reviews[:top_n]