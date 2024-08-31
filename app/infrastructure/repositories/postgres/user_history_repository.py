from sqlalchemy.orm import Session
from app.domain.models import UserHistory, UserPurchase, UserBrowsing

class UserHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_history(self, user_id: str):
        return self.db.query(UserHistory).filter(UserHistory.user_id == user_id).first()

    def add_purchase(self, user_id: str, product_id: str):
        purchase = UserPurchase(user_id=user_id, product_id=product_id)
        self.db.add(purchase)
        self.db.commit()
        self.db.refresh(purchase)
        return purchase

    def add_browsing(self, user_id: str, product_id: str):
        browsing = UserBrowsing(user_id=user_id, product_id=product_id)
        self.db.add(browsing)
        self.db.commit()
        self.db.refresh(browsing)
        return browsing