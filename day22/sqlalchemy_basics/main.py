from database import Base, engine, SessionLocal
from crud import (
    create_user,
    get_all_users,
    get_user_by_email,
    update_user_name,
    delete_user,
)
#create table automatically
Base.metadata.create_all(bind=engine)

# Create a session
db = SessionLocal()

# 1. Create sample users
print("Creating users...")
create_user(db, "mehwash@example.com", "mehwash")
create_user(db, "muhammad@example.com", "muhamad")

# 2. Get all users
print("\nAll users:")
print(get_all_users(db))

# 3. Get user by email
print("\nSearch user by email:")
print(get_user_by_email(db, "mehwash@example.com"))


# 4. Update user
print("\nUpdate user name:")
print(update_user_name(db, 1, "Mehwash Updated"))

# 5. Delete user
print("\nDelete user with ID 2:")
print(delete_user(db, 2))

# 6. Show remaining users
print("\nUsers left in DB:")
print(get_all_users(db))
