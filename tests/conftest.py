# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.domain.models import Product
from app.domain.models import Review
from app.domain.models import User, UserHistory, UserPurchase, UserBrowsing
from app.database import get_db
from app.main import app
from fastapi.testclient import TestClient
from faker import Faker
import uuid

DATABASE_URL_TEST = "postgresql://postgres:postgres@localhost:5434/test_app_db"

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
    fake = Faker()
    # Crear productos
    products = [Product(
        id=str(uuid.uuid4()),
        name=fake.word(),
        category=fake.random_element(elements=('Electronics', 'Books', 'Clothing', 'Home')),
        price=fake.random_number(digits=2),
        description=fake.text(max_nb_chars=300)
    ) for _ in range(10)]

    db.add_all(products)
    db.commit()

    # Crear un usuario
    user = User(
        id=str(uuid.uuid4()),
        username=fake.user_name(),
        email=fake.email()
    )
    db.add(user)
    db.commit()

    # Crear historial de usuario
    user_history = UserHistory(user_id=user.id)
    db.add(user_history)
    db.commit()

    # Agregar compras y navegaciones
    purchases = [UserPurchase(
        id=str(uuid.uuid4()),
        user_id=user.id,
        product_id=products[0].id,
        purchase_date=fake.date_time_this_year()
    )]

    browsings = [UserBrowsing(
        id=str(uuid.uuid4()),
        user_id=user.id,
        product_id=products[0].id,
        browse_date=fake.date_time_this_year()
    )]

    db.add_all(purchases + browsings)
    db.commit()

    # Crear reseñas
    reviews = [Review(
        product_id=products[0].id,
        user_id=user.id,
        title=fake.sentence(),
        content=fake.text(max_nb_chars=200),
        sentiment=fake.random_element(elements=('Positive', 'Negative')),
        votes=fake.random_int(min=0, max=100),
        date=fake.date_time_this_year()
    ) for _ in range(50)]

    db.add_all(reviews)
    db.commit()

    return {"user": user, "products": products, "reviews": reviews}
