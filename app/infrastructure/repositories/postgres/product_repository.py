from sqlalchemy.orm import Session
from app.domain.models import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product_by_id(self, product_id: str):
        """
        Retrieve a product from the database by its ID.

        Args:
            product_id (str): The unique identifier of the product.

        Returns:
            Product: The product object if found, None otherwise.
        """
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all_products(self):
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: A list of all product objects in the database.
        """
        return self.db.query(Product).all()

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
        product = Product(name=name, category=category, price=price, description=description)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product