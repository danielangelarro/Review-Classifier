import pandas as pd
from app.domain.models import User

class UserRepository:
    def __init__(self):
        self.df = pd.read_csv('/home/dukagin/Documents/CC/SRI/Review-Classifier/app/data/csv/data.csv')

    def get_user_by_id(self, user_id: str):
        """
        Retrieve a user from the database by their unique identifier.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            User: The user object if found, None otherwise.
        """
        users_id = set([row['reviewerID'] for _, row in self.df.iterrows()])

        users = [User(
            id=user_id,
            username=f'User {user_id}',
            email=f'{user_id}@gmail.com'
        ) for user_id in users_id]
        
        return users

    def get_user_by_username(self, username: str):
        """
        Retrieve a user from the database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The user object if found, None otherwise.
        """
        pass

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
        pass