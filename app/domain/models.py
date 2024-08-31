from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    title = Column(String)
    content = Column(String)
    sentiment = Column(String)
    votes = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="reviews")
    product = relationship("Product", backref="reviews")


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    description = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    history = relationship("UserHistory", back_populates="user", uselist=False)


class UserHistory(Base):
    __tablename__ = "user_histories"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="history")
    purchased_products = relationship("UserPurchase", back_populates="user_history")
    browsing_history = relationship("UserBrowsing", back_populates="user_history")


class UserPurchase(Base):
    __tablename__ = "user_purchases"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user_histories.user_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    purchase_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    user_history = relationship("UserHistory", back_populates="purchased_products")


class UserBrowsing(Base):
    __tablename__ = "user_browsings"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user_histories.user_id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    browse_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    user_history = relationship("UserHistory", back_populates="browsing_history")
