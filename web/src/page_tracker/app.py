"""App code for page_views application"""

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """App entry point"""
    try:
        page_views = get_redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong \N{thinking face}", 500
    return f"This page has been seen {page_views} times."


@cache
def get_redis():
    """Get Redis client"""
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
