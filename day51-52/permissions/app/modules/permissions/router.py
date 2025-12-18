from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.dependencies import get_db_session, require_permission
from app.modules.users.schemas import PermissionCreate, PermissionOut, RolePermissionOut
from app.modules.permissions.repository import (
    create_permission,
    get_all_permissions,
    delete_permission,
    assign_permission_to_role,
    get_role_permissions,
    remove_permission_from_role
)

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.post("/", response_model=PermissionOut, dependencies=[Depends(require_permission("manage:permissions"))])
async def create_new_permission(
    permission_in: PermissionCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new permission - Requires 'manage:permissions' permission"""
    permission = await create_permission(db, permission_in.name, permission_in.description)
    return permission

@router.get("/", response_model=List[PermissionOut])
async def list_permissions(db: AsyncSession = Depends(get_db_session)):
    """Get all permissions - Any authenticated user"""
    permissions = await get_all_permissions(db)
    return permissions

@router.delete("/{permission_id}", dependencies=[Depends(require_permission("manage:permissions"))])
async def delete_permission_endpoint(
    permission_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Delete a permission - Requires 'manage:permissions' permission"""
    success = await delete_permission(db, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted successfully"}

@router.post("/roles/{role}/permissions/{permission_id}", dependencies=[Depends(require_permission("manage:permissions"))])
async def assign_permission(
    role: str,
    permission_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Assign permission to role - Requires 'manage:permissions' permission"""
    role_permission = await assign_permission_to_role(db, role, permission_id)
    return {"message": f"Permission assigned to {role} successfully"}

@router.get("/roles/{role}", response_model=List[PermissionOut])
async def get_permissions_for_role(
    role: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Get all permissions for a role"""
    permissions = await get_role_permissions(db, role)
    return permissions

@router.delete("/roles/{role}/permissions/{permission_id}", dependencies=[Depends(require_permission("manage:permissions"))])
async def remove_permission(
    role: str,
    permission_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Remove permission from role - Requires 'manage:permissions' permission"""
    success = await remove_permission_from_role(db, role, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role permission not found")
    return {"message": f"Permission removed from {role} successfully"}