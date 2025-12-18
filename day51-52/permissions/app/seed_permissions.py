import asyncio
from app.database import AsyncSessionLocal
from app.modules.permissions.repository import (
    create_permission,
    assign_permission_to_role,
    get_permission_by_name
)

async def seed_permissions():
    """Seed initial permissions and assign them to roles"""
    async with AsyncSessionLocal() as db:
        # Define permissions
        permissions_data = [
            # Post permissions
            ("create:post", "Can create posts"),
            ("edit:post", "Can edit posts"),
            ("delete:post", "Can delete posts"),
            ("view:post", "Can view posts"),
            
            # User permissions
            ("manage:users", "Can manage users (create, edit, delete)"),
            ("view:users", "Can view user list"),
            ("edit:profile", "Can edit own profile"),
            
            # Admin permissions
            ("manage:permissions", "Can manage permissions and roles"),
            ("view:analytics", "Can view analytics and statistics"),
        ]
        
        # Create permissions
        print("Creating permissions...")
        created_permissions = {}
        for name, description in permissions_data:
            existing = await get_permission_by_name(db, name)
            if not existing:
                permission = await create_permission(db, name, description)
                created_permissions[name] = permission.id
                print(f"Created: {name}")
            else:
                created_permissions[name] = existing.id
                print(f"- Already exists: {name}")
        
        # Assign permissions to roles
        print("\nAssigning permissions to roles...")
        
        # ADMIN: All permissions
        admin_permissions = [
            "create:post", "edit:post", "delete:post", "view:post",
            "manage:users", "view:users", "edit:profile",
            "manage:permissions", "view:analytics"
        ]
        for perm_name in admin_permissions:
            await assign_permission_to_role(db, "admin", created_permissions[perm_name])
        print("Admin permissions assigned")
        
        # MODERATOR: Post management + view users
        moderator_permissions = [
            "create:post", "edit:post", "delete:post", "view:post",
            "view:users", "edit:profile", "view:analytics"
        ]
        for perm_name in moderator_permissions:
            await assign_permission_to_role(db, "moderator", created_permissions[perm_name])
        print("Moderator permissions assigned")
        
        # USER: Basic permissions
        user_permissions = [
            "create:post", "edit:post", "view:post", "edit:profile"
        ]
        for perm_name in user_permissions:
            await assign_permission_to_role(db, "user", created_permissions[perm_name])
        print("User permissions assigned")
        
        print("\nPermission seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_permissions())