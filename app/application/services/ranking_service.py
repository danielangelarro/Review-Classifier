import networkx as nx
import numpy as np
import networkx as nx

from app.domain.models import Review

from collections import defaultdict


class RankingService:
    def create_graph(self, reviews):
        G = nx.Graph()

        # Crear nodos para usuarios y juegos
        for row in reviews:
            G.add_node(row.user_id, bipartite=0)
            G.add_node(row.product_id, bipartite=1)

            # Añadir arista con peso basado en sentiment y overall
            weight = (row.sentiment + 1) / 2 * (row.votes / 5)  # Normalizar a [0, 1]
            G.add_edge(row.user_id, row.product_id, weight=weight)

        return G

    def get_similar_users(self, G, user_id, game_id):
        # Obtener usuarios que han revisado el mismo juego
        similar_users = set(G.neighbors(game_id)) - {user_id}
        return similar_users

    def personalized_pagerank(self, G, user_id, game_id):
        similar_users = self.get_similar_users(G, user_id, game_id)

        # Crear vector personalizado
        personalization = defaultdict(float)
        for user in similar_users:
            personalization[user] = 1.0

        # Ejecutar PageRank personalizado
        pagerank = nx.pagerank(G, personalization=personalization)
        return pagerank

    def rank_reviews(self, reviews, user_id, game_id, top_n=10):
        G = self.create_graph(reviews)
        pagerank = self.personalized_pagerank(G, user_id, game_id)

        # Calcular score para cada review
        scored_reviews = []
        for review in reviews:
            reviewer_rank = pagerank.get(review.user_id, 0)
            sentiment_score = (review.sentiment + 1) / 2  # Normalizar a [0, 1]
            helpful = [int(x) for x in review.helpful[1:-1].split(', ')]
            helpfulness = helpful[0] / max(helpful[1], 1)

            score = (reviewer_rank + sentiment_score + helpfulness) / 3
            scored_reviews.append((score, review))

        # Ordenar reviews por score
        scored_reviews.sort(reverse=True, key=lambda x: x[0])

        return scored_reviews[:top_n]