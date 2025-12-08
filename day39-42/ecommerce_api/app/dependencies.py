from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from app.core.security import get_current_user, get_admin_user
from app.models import User
from app.repositories import (
    UserRepository,
    CategoryRepository,
    ProductRepository,
    OrderRepository,
    OrderItemRepository,
)
from app.services import (
    UserService,
    CategoryService,
    ProductService,
    OrderService,
)


# ===== Authentication & Authorization =====

__all_auth__ = [
    "get_current_user",
    "get_admin_user",
]


# ===== Database Session =====

__all_db__ = [
    "get_async_session",
]


# ===== Repository Dependencies =====


async def get_user_repo(
    session: AsyncSession = Depends(get_async_session),) -> UserRepository:
    """
    Get UserRepository instance.

    Args:
        session: AsyncSession from dependency injection.

    Returns:
        UserRepository instance.
    """
    return UserRepository(session)


async def get_category_repo(
    session: AsyncSession = Depends(get_async_session),) -> CategoryRepository:
    """
    Get CategoryRepository instance.

    Args:
        session: AsyncSession from dependency injection.

    Returns:
        CategoryRepository instance.
    """
    return CategoryRepository(session)


async def get_product_repo(
    session: AsyncSession = Depends(get_async_session),) -> ProductRepository:
    """
    Get ProductRepository instance.

    Args:
        session: AsyncSession from dependency injection.

    Returns:
        ProductRepository instance.
    """
    return ProductRepository(session)


async def get_order_repo(
    session: AsyncSession = Depends(get_async_session),) -> OrderRepository:
    """
    Get OrderRepository instance.

    Args:
        session: AsyncSession from dependency injection.

    Returns:
        OrderRepository instance.
    """
    return OrderRepository(session)


async def get_order_item_repo(
    session: AsyncSession = Depends(get_async_session),) -> OrderItemRepository:
    """
    Get OrderItemRepository instance.

    Args:
        session: AsyncSession from dependency injection.

    Returns:
        OrderItemRepository instance.
    """
    return OrderItemRepository(session)


# ===== Service Dependencies =====


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repo),) -> UserService:
    """
    Get UserService instance.

    Args:
        user_repo: UserRepository from dependency injection.

    Returns:
        UserService instance.
    """
    return UserService(user_repo)


async def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repo),) -> CategoryService:
    """
    Get CategoryService instance.

    Args:
        category_repo: CategoryRepository from dependency injection.

    Returns:
        CategoryService instance.
    """
    return CategoryService(category_repo)


async def get_product_service(
    product_repo: ProductRepository = Depends(get_product_repo),
    category_repo: CategoryRepository = Depends(get_category_repo),) -> ProductService:
    """
    Get ProductService instance.

    Args:
        product_repo: ProductRepository from dependency injection.
        category_repo: CategoryRepository from dependency injection.

    Returns:
        ProductService instance.
    """
    return ProductService(product_repo, category_repo)


async def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repo),) -> OrderService:
    """
    Get OrderService instance.

    Args:
        order_repo: OrderRepository from dependency injection.

    Returns:
        OrderService instance.
    """
    return OrderService(order_repo)


__all__ = [
    "get_async_session",
    "get_current_user",
    "get_admin_user",
    "get_user_repo",
    "get_category_repo",
    "get_product_repo",
    "get_order_repo",
    "get_order_item_repo",
    "get_user_service",
    "get_category_service",
    "get_product_service",
    "get_order_service",
]