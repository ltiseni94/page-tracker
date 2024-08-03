import pytest
import requests


@pytest.mark.timeout(1.5)
def test_should_update_redis(redis_client, flask_url):
    redis_client.set("page_views", 4)
    response = requests.get(flask_url)
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    assert redis_client.get("page_views") == b"5"

