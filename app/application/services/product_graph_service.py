from collections import defaultdict
import networkx as nx
from app.domain.models import Product

class ProductGraphService:
    def __init__(self):
        self.graph = nx.Graph()

    def build_graph(self, products):
        """Builds a aimilarity graph for a given product list"""
        for product in products:
            self.graph.add_node(product.id, name=product.name)

        for i, product_a in enumerate(products):
            for product_b in products[i+1:]:
                if product_a.category == product_b.category:
                    self.graph.add_edge(product_a.id, product_b.id)
        return self.graph

    def find_similar_products(self, product_id):
        """Returns directly connected products"""
        return list(self.graph.neighbors(product_id))