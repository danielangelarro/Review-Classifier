from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.infrastructure.repositories.postgres.review_repository import ReviewRepository
from app.infrastructure.repositories.postgres.product_repository import ProductRepository
from app.infrastructure.repositories.postgres.user_repository import UserRepository
from app.application.services.ranking_service import RankingService


router = APIRouter()


@router.get("/reviews/{user_id}/{product_id}")
def get_top_reviews(
        user_id: str,
        product_id: str,
        top_n: int = 5,
        db: Session = Depends(get_db)
):
    """
    Retrieve and rank the top reviews for a specific product and user.

    This endpoint fetches the top-ranked reviews for a given product, tailored to a specific user's preferences. It uses a ranking service to determine the most relevant reviews.

    Parameters:
    - user_id (str): The unique identifier of the user.
    - product_id (str): The unique identifier of the product.
    - top_n (int, optional): The number of top reviews to return. Defaults to 5.
    - db (Session): The database session, injected by FastAPI's dependency system.

    Returns:
    A dictionary containing:
    - user_id (str): The ID of the user.
    - product_id (str): The ID of the product.
    - top_reviews (list): A list of the top-ranked reviews, ordered by relevance.

    Raises:
    - HTTPException (404): If the user or product is not found in the database.

    Dependencies:
    - UserRepository: For fetching user data.
    - ProductRepository: For fetching product data.
    - ReviewRepository: For fetching review data.
    - RankingService: For ranking the reviews.

    Note:
    This function assumes the existence of a ranking algorithm that can determine 
    the relevance of reviews based on user preferences and product characteristics.
    """
    user_repo = UserRepository(db)
    product_repo = ProductRepository(db)
    review_repo = ReviewRepository(db)
    ranking_service = RankingService()

    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = product_repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = review_repo.get_reviews_by_product_id(product_id)

    top_reviews = ranking_service.rank_reviews(reviews, user_id, product_id, top_n=top_n)
    return {"user_id": user_id, "product_id": product_id, "top_reviews": top_reviews}