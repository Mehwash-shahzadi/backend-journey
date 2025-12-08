from decimal import Decimal
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user, get_admin_user
from app.repositories import OrderRepository, ProductRepository 
from app.database.db import get_async_session
from app.dependencies import (
    get_category_service,
    get_product_service,
    get_order_service,
    get_product_repo,
)
from app.models import User
from app.schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    OrderCreate,
    OrderResponse,
)
from app.services import CategoryService, ProductService, OrderService

router = APIRouter(prefix="/v1", tags=["v1"])

# CATEGORY ROUTES

@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category (admin only)",
)
async def create_category(
    category_in: CategoryCreate,
    admin: User = Depends(get_admin_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """
    Create a new product category.

    Only administrators can create categories.

    Args:
        category_in: Category data (name, description).
        admin: Current authenticated admin user.
        service: CategoryService instance.

    Returns:
        Created category with generated ID.

    Raises:
        HTTPException: 403 if user is not admin.
        HTTPException: 400 if category name already exists.
    """
    return await service.create_category(category_in)


@router.get(
    "/categories",
    response_model=list[CategoryResponse],
    summary="Retrieve all categories",
)
async def get_all_categories(
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryResponse]:
    """
    Retrieve all product categories.

    Public endpoint  no authentication required.

    Args:
        service: CategoryService instance.

    Returns:
        List of all categories in the system.
    """
    return await service.get_all_categories()


@router.get(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    summary="Retrieve a single category by ID",
)
async def get_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """
    Retrieve a single category by its ID.

    Public endpoint  no authentication required.

    Args:
        category_id: ID of the category to retrieve.
        service: CategoryService instance.

    Returns:
        Category details including name and description.

    Raises:
        HTTPException: 404 if category not found.
    """
    return await service.get_category_by_id(category_id)


@router.put(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    summary="Update a category (admin only)",
)
async def update_category(
    category_id: int,
    category_in: CategoryUpdate,
    admin: User = Depends(get_admin_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    """
    Update an existing category.

    Only administrators can update categories.

    Args:
        category_id: ID of the category to update.
        category_in: Updated category data.
        admin: Current authenticated admin user.
        service: CategoryService instance.

    Returns:
        Updated category.

    Raises:
        HTTPException: 403 if user is not admin.
        HTTPException: 404 if category not found.
        HTTPException: 400 if new name already exists.
    """
    return await service.update_category(category_id, category_in)


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete a category (admin only)",
)
async def delete_category(
    category_id: int,
    admin: User = Depends(get_admin_user),
    service: CategoryService = Depends(get_category_service),
) -> dict:
    """
    Delete a category by ID.

    Only administrators can delete categories.

    Args:
        category_id: ID of the category to delete.
        admin: Current authenticated admin user.
        service: CategoryService instance.

    Returns:
        Confirmation message.

    Raises:
        HTTPException: 403 if user is not admin.
        HTTPException: 404 if category not found.
    """
    await service.delete_category(category_id)
    return {"detail": "Category deleted successfully"}


#  PRODUCT ROUTES

@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product (admin only)",
)
async def create_product(
    product_in: ProductCreate,
    admin: User = Depends(get_admin_user),
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Create a new product with category associations.

    Only administrators can create products.

    Args:
        product_in: Product data including name, price, stock, and category IDs.
        admin: Current authenticated admin user.
        service: ProductService instance.

    Returns:
        Created product with categories attached.

    Raises:
        HTTPException: 403 if user is not admin.
        HTTPException: 400 if any category_id is invalid.
    """
    return await service.create_product(product_in)


@router.get(
    "/products",
    response_model=list[ProductResponse],
    summary="Retrieve products with filtering and pagination",
)
async def get_all_products(
    search: str | None = Query(None, description="Search by product name"),
    category_id: int | None = Query(None, description="Filter by category ID"),
    min_price: Decimal | None = Query(None, gt=0, description="Minimum price"),
    max_price: Decimal | None = Query(None, gt=0, description="Maximum price"),
    skip: int = Query(0, ge=0, description="Records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    service: ProductService = Depends(get_product_service),
) -> list[ProductResponse]:
    """
    Retrieve products with powerful filtering.

    Public endpoint  no authentication required.

    Supports:
    - Name search
    - Category filtering
    - Price range
    - Pagination

    Args:
        search: Partial product name match.
        category_id: Filter by category.
        min_price: Minimum price filter.
        max_price: Maximum price filter.
        skip: Pagination offset.
        limit: Number of items per page.
        service: ProductService instance.

    Returns:
        Filtered and paginated list of products.
    """
    products = await service.get_all_products()

    if search:
        products = [p for p in products if search.lower() in p.name.lower()]
    if category_id:
        products = [p for p in products if any(c.id == category_id for c in p.categories)]
    if min_price:
        products = [p for p in products if p.price >= min_price]
    if max_price:
        products = [p for p in products if p.price <= max_price]

    return products[skip:skip + limit]


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Retrieve a single product by ID",
)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Retrieve a single product with full category details.

    Public endpoint  no authentication required.

    Args:
        product_id: ID of the product to retrieve.
        service: ProductService instance.

    Returns:
        Product details including categories.

    Raises:
        HTTPException: 404 if product not found.
    """
    return await service.get_product_by_id(product_id)


@router.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Update a product (admin only)",
)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    admin: User = Depends(get_admin_user),
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Update an existing product.

    Only administrators can update products.

    Args:
        product_id: ID of the product to update.
        product_in: Updated product data.
        admin: Current authenticated admin user.
        service: ProductService instance.

    Returns:
        Updated product with new categories.

    Raises:
        HTTPException: 403 if user is not admin.
        HTTPException: 404 if product not found.
        HTTPException: 400 if category_id invalid.
    """
    return await service.update_product(product_id, product_in)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=dict,
    summary="Delete a product (admin only)",
)
async def delete_product(
    product_id: int,
    admin: User = Depends(get_admin_user),
    service: ProductService = Depends(get_product_service),
) -> dict:
    """
    Delete a product by ID.

    Only administrators can delete products.

    Args:
        product_id: ID of the product to delete.
        admin: Current authenticated admin user.
        service: ProductService instance.

    Returns:
        Confirmation message.

    Raises:
        HTTPException: 403 if user is not admin.
        HTTPException: 404 if product not found.
    """
    await service.delete_product(product_id)
    return {"detail": "Product deleted successfully"}

#     ORDER ROUTES
# Keep everything else exactly as you had it – only replace the POST /orders route

@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=201,
    summary="Place a new order  stock reduced atomically (Day 39)",
)
async def place_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    order_service: OrderService = Depends(get_order_service),
    product_repo: ProductRepository = Depends(get_product_repo),  # ← now works!
):
    return await order_service.create_order(
        user=current_user,
        items_data=order_in.items,
        product_repo=product_repo,
        session=session,
    )

@router.get(
    "/users/me/orders",
    response_model=list[OrderResponse],
    summary="Get current user's order history",
)
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    service: OrderService = Depends(get_order_service),
) -> list[OrderResponse]:
    """
    Retrieve order history for the current user.

    Orders include full item details and product snapshots.

    Args:
        current_user: Authenticated user.
        service: OrderService instance.

    Returns:
        List of user's orders, newest first.

    Raises:
        HTTPException: 401 if not authenticated.
    """
    return await service.get_user_orders(current_user.id)