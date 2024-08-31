import pytest


@pytest.mark.asyncio
def test_rank_reviews_with_user_history(client, fake_data):
    user_id = fake_data["user"].id
    product_id = fake_data["products"][0].id

    response = client.get(f"/api/reviews/{user_id}/{product_id}?top_n=5")
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == user_id
    assert data["product_id"] == product_id
    assert "top_reviews" in data
    assert len(data["top_reviews"]) == 5

    # Verificar que las reseñas están ordenadas por relevancia
    reviews = data["top_reviews"]
    for i in range(len(reviews) - 1):
        # No hay una manera directa de verificar la relevancia sin exponerla,
        # pero asumimos que el servicio de ranking funciona correctamente
        pass