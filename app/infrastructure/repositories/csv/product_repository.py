import pandas as pd
from app.domain.models import Product


class ProductRepository:
    def __init__(self):
        self.df = pd.read_csv('/home/dukagin/Documents/CC/SRI/Review-Classifier/app/data/csv/data.csv')

    def get_product_by_id(self, product_id: str):
        """
        Retrieve a product from the database by its ID.

        Args:
            product_id (str): The unique identifier of the product.

        Returns:
            Product: The product object if found, None otherwise.
        """
        
        product_ids = [row['asin'] for _, row in self.df.iterrows() if row['asin'] == product_id]
    
        products = [Product(
            id=id,
            name=fake.word(),
            category='Game',
            price=fake.random_number(digits=2),
            description=fake.text(max_nb_chars=300)
        ) for id in product_ids]
        
        return  products

    def get_all_products(self):
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: A list of all product objects in the database.
        """
        
        product_ids = set([row['asin'] for _, row in self.df.iterrows()])
    
        products = [Product(
            id=id,
            name=fake.word(),
            category='Game',
            price=fake.random_number(digits=2),
            description=fake.text(max_nb_chars=300)
        ) for id in product_ids]
        
        return  products
        

    def create_product(self, name: str, category: str, price: float, description: str):
        """
        Create a new product and add it to the database.

        Args:
            name (str): The name of the product.
            category (str): The category of the product.
            price (float): The price of the product.
            description (str): A description of the product.

        Returns:
            Product: The newly created product object.
        """
        pass