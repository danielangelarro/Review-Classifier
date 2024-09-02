from sqlalchemy.orm import Session
from app.domain.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: str):
        """
        Retrieve a user from the database by their unique identifier.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            User: The user object if found, None otherwise.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str):
        """
        Retrieve a user from the database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, username: str, email: str):
        """
        Create a new user in the database.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.

        Returns:
            User: The newly created user object.

        Note:
            This function commits the new user to the database and refreshes the object
            to ensure all database-generated fields (like id) are populated.
        """
        new_user = User(username=username, email=email)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user