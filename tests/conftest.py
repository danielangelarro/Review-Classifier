import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.domain.models import Product
from app.domain.models import Review
from app.domain.models import User
from app.database import get_db
from app.main import app
from fastapi.testclient import TestClient
from faker import Faker
import uuid
import pandas as pd
from datetime import datetime


DATABASE_URL_TEST = "postgresql://postgres:postgres@localhost:5434/app_db"

engine = create_engine(DATABASE_URL_TEST)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionTesting()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def fake_data(db):
    df = pd.read_csv('tests/data/csv/data.csv')

    fake = Faker()
    # Crear un producto
    product = Product(
        id='B000006OVE',
        name=fake.word(),
        category='Game',
        price=fake.random_number(digits=2),
        description=fake.text(max_nb_chars=300)
    )

    db.add(product)
    db.commit()

    # Inserta los usuarios
    users_id = set([row['reviewerID'] for _, row in df.iterrows()])

    users = [User(
        id=user_id,
        username=f'User {user_id}',
        email=f'{user_id}@gmail.com'
    ) for user_id in users_id]

    db.add_all(users)
    db.commit()

    # Crear reseñas
    reviews = [Review(
        product_id=row['asin'],
        user_id=row['reviewerID'],
        title=row['summary'],
        content=row['reviewText'],
        sentiment=row['sentiments'],
        votes=row['overall'],
        helpful=row['helpful'],
        date=datetime.strptime(row['reviewTime'], '%m %d, %Y')
    ) for _, row in df.iterrows() if row['asin'] == product.id]

    db.add_all(reviews)
    db.commit()

    return {"user": users, "product": product, "reviews": reviews}
