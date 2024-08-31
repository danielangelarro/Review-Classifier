import networkx as nx
from datetime import datetime
from app.domain.models import Review

class RankingService:

    def calculate_relevance(self, review: Review, user_history, product, product_graph: nx.Graph):
        relevance_score = 0

        # Verificar si el producto fue comprado o visitado por el usuario
        purchased_product_ids = [purchase.product_id for purchase in user_history.purchased_products]
        browsing_product_ids = [browse.product_id for browse in user_history.browsing_history]

        if product.id in purchased_product_ids:
            relevance_score += 20
        elif product.id in browsing_product_ids:
            relevance_score += 10

        # Calcular relevancia basada en el grafo de productos
        for purchased_product_id in purchased_product_ids:
            if nx.has_path(product_graph, purchased_product_id, product.id):
                path_length = nx.shortest_path_length(product_graph, source=purchased_product_id, target=product.id)
                relevance_score += (1 / (path_length + 1)) * 15

        # Agregar relevancia basada en votos y antigüedad de la reseña
        relevance_score += review.votes * 0.1
        relevance_score += (datetime.now() - review.date).days * 0.01

        # Ajustar relevancia según el sentimiento
        if review.sentiment.lower() == 'positive':
            relevance_score += 5
        else:
            relevance_score -= 5

        return relevance_score

    def rank_reviews(self, reviews, user_history, product, product_graph: nx.Graph, top_n=5):
        ranked_reviews = sorted(
            reviews,
            key=lambda review: self.calculate_relevance(review, user_history, product, product_graph),
            reverse=True
        )
        return ranked_reviews[:top_n]