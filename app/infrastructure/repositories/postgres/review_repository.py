from sqlalchemy.orm import Session
from app.domain.models import Review

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_reviews_by_product_id(self, product_id: str):
        return self.db.query(Review).filter(Review.product_id == product_id).all()

    def create_review(self, product_id: str, user_id: str, title: str, content: str, sentiment: str):
        review = Review(
            product_id=product_id,
            user_id=user_id,
            title=title,
            content=content,
            sentiment=sentiment
        )
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review