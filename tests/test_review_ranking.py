import pytest


@pytest.mark.asyncio
def test_rank_reviews_with_user_history(client, fake_data):
    user_id = 'A2HD75EMZR8QLN'
    product_id = 'B000006OVE'

    response = client.get(f"/api/reviews/{user_id}/{product_id}?top_n=5")
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == user_id
    assert data["product_id"] == product_id
    assert "top_reviews" in data
    assert len(data["top_reviews"]) == 5
