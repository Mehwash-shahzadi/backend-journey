"""
Transaction Demo Test Script
"""

from .database import SessionLocal
from . import crud, models

def print_line():
    print("=" * 60)

def show_balances(db):
    users = db.query(models.User).all()
    print("\nCurrent Balances:")
    for user in users:
        print(f"  {user.name} (ID: {user.id}): ${float(user.balance):.2f}")

def test_successful_transfer():
    print_line()
    print("TEST 1: Successful Transfer")
    print_line()
    
    db = SessionLocal()
    
    try:
        print("Before transfer:")
        show_balances(db)
        
        # Use users with balance (ID:4 has 9000, ID:5 has 7000)
        print("\nTransferring $100 from maheen (ID:4) to anabia (ID:5)...")
        try:
            result = crud.transfer_money(db, sender_id=4, receiver_id=5, amount=100)
            print(f"Result: {result['message']}")
            
            print("\nAfter transfer:")
            show_balances(db)
        except ValueError as e:
            print(f"Error: {e}")
            print("Skipping - users don't have enough balance")
        
    finally:
        db.close()

def test_insufficient_balance():
    print_line()
    print("TEST 2: Insufficient Balance (Rollback)")
    print_line()
    
    db = SessionLocal()
    
    try:
        print("Before failed transfer:")
        show_balances(db)
        
        print("\nTrying to transfer $20000 from anabia (ID:5) to maheen (ID:4)...")
        try:
            crud.transfer_money(db, sender_id=5, receiver_id=4, amount=20000)
        except ValueError as e:
            print(f"Error: {e}")
            print("Transaction rolled back!")
        
        print("\nAfter rollback (balances unchanged):")
        show_balances(db)
        
    finally:
        db.close()

def test_user_not_found():
    print_line()
    print("TEST 3: User Not Found (Rollback)")
    print_line()
    
    db = SessionLocal()
    
    try:
        print("Before failed transfer:")
        show_balances(db)
        
        print("\nTrying to transfer $50 from maheen (ID:4) to user (ID:999)...")
        try:
            crud.transfer_money(db, sender_id=4, receiver_id=999, amount=50)
        except ValueError as e:
            print(f"Error: {e}")
            print("Transaction rolled back!")
        
        print("\nAfter rollback (balances unchanged):")
        show_balances(db)
        
    finally:
        db.close()

def test_duplicate_email():
    print_line()
    print("TEST 4: Duplicate Email")
    print_line()
    
    db = SessionLocal()
    
    try:
        print("Trying to create user with email 'asif@mail.com'...")
        try:
            crud.create_user(db, name="Fake Asif", email="asif@mail.com", balance=500)
        except ValueError as e:
            print(f"Error: {e}")
            print("Duplicate email prevented!")
        
    finally:
        db.close()

def run_all_tests():
    print("\n" + "=" * 60)
    print("  TRANSACTION DEMO")
    print("=" * 60)
    
    test_successful_transfer()
    test_insufficient_balance()
    test_user_not_found()
    test_duplicate_email()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_all_tests()