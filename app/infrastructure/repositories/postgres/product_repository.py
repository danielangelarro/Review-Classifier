from sqlalchemy.orm import Session
from app.domain.models import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product_by_id(self, product_id: str):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all_products(self):
        return self.db.query(Product).all()

    def create_product(self, name: str, category: str, price: float, description: str):
        product = Product(name=name, category=category, price=price, description=description)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product