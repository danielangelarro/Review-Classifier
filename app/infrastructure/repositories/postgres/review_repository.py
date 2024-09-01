from sqlalchemy.orm import Session
from app.domain.models import Review

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_reviews_by_product_id(self, product_id: str):
        """
        Retrieve all reviews for a specific product.

        This function queries the database and returns all review objects associated with the given product ID.

        Parameters:
        ----------
        product_id : str
            The unique identifier of the product for which to retrieve reviews.

        Returns:
        -------
        list of Review
            A list of Review objects associated with the specified product ID.
            Returns an empty list if no reviews are found.
        """
        return self.db.query(Review).filter(Review.product_id == product_id).all()

    def create_review(self, product_id: str, user_id: str, title: str, content: str, sentiment: str):
        """
        Create a new review for a product.

        This function creates a new review in the database with the provided information.

        Parameters:
        ----------
        product_id : str
            The unique identifier of the product being reviewed.
        user_id : str
            The unique identifier of the user writing the review.
        title : str
            The title of the review.
        content : str
            The main text content of the review.
        sentiment : str
            The sentiment of the review (e.g., "positive", "negative", "neutral").

        Returns:
        -------
        Review
            The newly created Review object, after it has been added to the database and refreshed.

        Note:
        -----
        This function commits the new review to the database immediately.
        """
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