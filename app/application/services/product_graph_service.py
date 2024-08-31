from collections import defaultdict
import networkx as nx
from app.domain.models import Product

class ProductGraphService:
    def __init__(self):
        self.graph = nx.Graph()

    # def calculate_tfidf_similarity(products):
    #     descriptions = [p.description for p in products]
    #     vectorizer = TfidfVectorizer(stop_words='english')
    #     tfidf_matrix = vectorizer.fit_transform(descriptions)
    #     similarity_matrix = cosine_similarity(tfidf_matrix)
    #     return similarity_matrix
    #
    #
    # def build_graph(products, similarity_matrix):
    #     G = nx.Graph()
    #     for i, product in enumerate(products):
    #         G.add_node(product.product_id, description=product.description)
    #         for j in range(i+1, len(products)):
    #             if similarity_matrix[i, j] > 0.2:
    #                 G.add_edge(product.product_id, products[j].product_id, weight=similarity_matrix[i, j])
    #     return G

    def build_graph(self, products):
        # Construir el grafo considerando similitudes en nombres y compras comunes
        # Por simplicidad, conectamos productos que comparten al menos una categoría
        for product in products:
            self.graph.add_node(product.id, name=product.name)

        for i, product_a in enumerate(products):
            for product_b in products[i+1:]:
                if product_a.category == product_b.category:
                    self.graph.add_edge(product_a.id, product_b.id)
        return self.graph

    def find_similar_products(self, product_id):
        # Retorna productos conectados directamente
        return list(self.graph.neighbors(product_id))