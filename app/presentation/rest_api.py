from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.infrastructure.repositories.postgres.review_repository import ReviewRepository
from app.infrastructure.repositories.postgres.product_repository import ProductRepository
from app.infrastructure.repositories.postgres.user_repository import UserRepository
from app.infrastructure.repositories.postgres.user_history_repository import UserHistoryRepository
from app.application.services.ranking_service import RankingService
from app.application.services.product_graph_service import ProductGraphService

router = APIRouter()


@router.get("/reviews/{user_id}/{product_id}")
def get_top_reviews(
        user_id: str,
        product_id: str,
        top_n: int = 5,
        db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    user_history_repo = UserHistoryRepository(db)
    product_repo = ProductRepository(db)
    review_repo = ReviewRepository(db)
    ranking_service = RankingService()
    product_graph_service = ProductGraphService()

    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = product_repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = review_repo.get_reviews_by_product_id(product_id)

    user_history = user_history_repo.get_user_history(user_id)
    if not user_history:
        raise HTTPException(status_code=404, detail="User history not found")

    product_graph = product_graph_service.build_graph(product_repo.get_all_products())

    top_reviews = ranking_service.rank_reviews(reviews, user_history, product, product_graph, top_n=top_n)
    return {"user_id": user_id, "product_id": product_id, "top_reviews": top_reviews}