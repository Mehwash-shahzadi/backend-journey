"""
Routers package initialization.
This file makes the routers directory a Python package.
"""

from app.routers import users, posts, comments

__all__ = ["users", "posts", "comments"]