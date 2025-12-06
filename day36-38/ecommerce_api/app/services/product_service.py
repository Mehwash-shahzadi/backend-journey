"""
Product service for product-related business logic.

Handles CRUD operations for products with category association.
"""

from fastapi import HTTPException, status

from app.models import Product
from app.repositories import ProductRepository, CategoryRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductService:
    """
    Service layer for product operations.

    Handles product CRUD operations, category associations, and validation.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository,
    ):
        """
        Initialize ProductService.

        Args:
            product_repo: ProductRepository instance for product data access.
            category_repo: CategoryRepository instance for category data access.
        """
        self.product_repo = product_repo
        self.category_repo = category_repo

    async def get_all_products(self) -> list[Product]:
        """Retrieve all products with categories preloaded."""
        return await self.product_repo.get_all_with_categories()

    async def get_product_by_id(self, product_id: int) -> Product:
        """Retrieve a product by id with categories preloaded."""
        product = await self.product_repo.get_by_id_with_categories(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )
        return product

    async def create_product(self, product_in: ProductCreate) -> Product:
        """
        Create a new product with associated categories.

        Args:
            product_in: ProductCreate schema with product data and category_ids.

        Returns:
            Created Product with categories preloaded (safe for Pydantic serialization).

        Raises:
            HTTPException: 400 if any category_id is invalid.
        """
        # Validate categories exist
        categories = []
        if product_in.category_ids:
            for cat_id in product_in.category_ids:
                category = await self.category_repo.get_by_id(cat_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Category with id {cat_id} not found",
                    )
                categories.append(category)

        # Create product
        product = Product(
            name=product_in.name,
            price=product_in.price,
            stock=product_in.stock,
        )
        product.categories = categories

        # Save to DB
        created = await self.product_repo.create(product)

        # Reload with joinedload so categories are available
        return await self.product_repo.get_by_id_with_categories(created.id)

    async def update_product(
        self, product_id: int, product_in: ProductUpdate
    ) -> Product:
        """
        Update an existing product.

        Category associations are completely replaced.
        """
        product = await self.get_product_by_id(product_id)

        # Update categories if provided
        if product_in.category_ids is not None:
            categories = []
            for cat_id in product_in.category_ids:
                category = await self.category_repo.get_by_id(cat_id)
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Category with id {cat_id} not found",
                    )
                categories.append(category)
            product.categories = categories

        # Update other fields
        update_data = product_in.model_dump(exclude={"category_ids"}, exclude_unset=True)
        if update_data:
            await self.product_repo.update(product_id, update_data)

        # Always return preloaded version
        return await self.product_repo.get_by_id_with_categories(product_id)

    async def delete_product(self, product_id: int) -> bool:
        """Delete a product by id."""
        await self.get_product_by_id(product_id)
        return await self.product_repo.delete(product_id)