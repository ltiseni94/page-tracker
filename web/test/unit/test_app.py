import unittest.mock
import pytest
from page_tracker.app import app
from redis import ConnectionError


@unittest.mock.patch("page_tracker.app.get_redis")
def test_should_call_redis_incr(mock_redis, http_client):
    mock_redis.return_value.incr.return_value = 5
    response = http_client.get("/")
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    mock_redis.return_value.incr.assert_called_once_with("page_views")


@unittest.mock.patch("page_tracker.app.get_redis")
def test_should_handle_redis_connection_error(mock_redis, http_client):
    mock_redis.return_value.incr.side_effect = ConnectionError
    response = http_client.get("/")
    assert response.status_code == 500
    assert response.text == "Sorry, something went wrong \N{thinking face}"

