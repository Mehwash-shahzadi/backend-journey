from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.users.models import Permission, RolePermission
from typing import List

async def create_permission(db: AsyncSession, name: str, description: str | None = None) -> Permission:
    """Create a new permission"""
    permission = Permission(name=name, description=description)
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission

async def get_permission_by_name(db: AsyncSession, name: str) -> Permission | None:
    """Get permission by name"""
    result = await db.execute(select(Permission).where(Permission.name == name))
    return result.scalar_one_or_none()

async def get_all_permissions(db: AsyncSession) -> List[Permission]:
    """Get all permissions"""
    result = await db.execute(select(Permission))
    return result.scalars().all()

async def delete_permission(db: AsyncSession, permission_id: int) -> bool:
    """Delete a permission"""
    result = await db.execute(select(Permission).where(Permission.id == permission_id))
    permission = result.scalar_one_or_none()
    if permission:
        await db.delete(permission)
        await db.commit()
        return True
    return False

# Role-Permission management 

async def assign_permission_to_role(db: AsyncSession, role: str, permission_id: int) -> RolePermission:
    """Assign permission to role"""
    role_permission = RolePermission(role=role, permission_id=permission_id)
    db.add(role_permission)
    await db.commit()
    await db.refresh(role_permission)
    return role_permission

async def get_role_permissions(db: AsyncSession, role: str) -> List[Permission]:
    """Get all permissions for a role"""
    result = await db.execute(
        select(Permission)
        .join(RolePermission)
        .where(RolePermission.role == role)
    )
    return result.scalars().all()

async def remove_permission_from_role(db: AsyncSession, role: str, permission_id: int) -> bool:
    """Remove permission from role"""
    result = await db.execute(
        select(RolePermission)
        .where(RolePermission.role == role, RolePermission.permission_id == permission_id)
    )
    role_permission = result.scalar_one_or_none()
    if role_permission:
        await db.delete(role_permission)
        await db.commit()
        return True
    return False

async def user_has_permission(db: AsyncSession, user_role: str, permission_name: str) -> bool:
    """Check if user's role has specific permission"""
    result = await db.execute(
        select(Permission)
        .join(RolePermission)
        .where(RolePermission.role == user_role, Permission.name == permission_name)
    )
    permission = result.scalar_one_or_none()
    return permission is not None