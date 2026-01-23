"""
Database Reset Script - Clear all user registration data
Run this to delete all users, applications, documents, and account credentials
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app.database import engine, SessionLocal, Base
from backend.app.models import User, Document, ElectricityAccount, GasAccount, WaterAccount, PropertyAccount, Application

def reset_database():
    """Drop all tables and recreate them empty"""
    print("🗑️  RESETTING DATABASE...")
    print("⚠️  WARNING: This will delete ALL user data, credentials, and applications!")
    print("")
    
    confirm = input("Are you sure? Type 'YES' to continue: ")
    if confirm != "YES":
        print("❌ Operation cancelled")
        return
    
    try:
        # Drop all tables
        print("\n1️⃣  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped")
        
        # Recreate all tables
        print("\n2️⃣  Creating fresh tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Fresh tables created")
        
        print("\n✅ DATABASE RESET COMPLETE!")
        print("Database is now empty and ready for fresh registrations")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise

def delete_all_users():
    """Delete all users and related data"""
    db = SessionLocal()
    try:
        print("🗑️  DELETING ALL USERS AND CREDENTIALS...")
        
        # Count before deletion
        user_count = db.query(User).count()
        doc_count = db.query(Document).count()
        app_count = db.query(Application).count()
        
        print(f"\n📊 Current data:")
        print(f"   Users: {user_count}")
        print(f"   Documents: {doc_count}")
        print(f"   Applications: {app_count}")
        
        confirm = input("\nType 'YES' to delete all: ")
        if confirm != "YES":
            print("❌ Operation cancelled")
            return
        
        # Delete in order of dependencies
        print("\n1️⃣  Deleting applications...")
        db.query(Application).delete()
        
        print("2️⃣  Deleting documents...")
        db.query(Document).delete()
        
        print("3️⃣  Deleting account credentials...")
        db.query(ElectricityAccount).delete()
        db.query(GasAccount).delete()
        db.query(WaterAccount).delete()
        db.query(PropertyAccount).delete()
        
        print("4️⃣  Deleting users...")
        db.query(User).delete()
        
        db.commit()
        
        print("\n✅ ALL DATA DELETED!")
        print("System is ready for fresh registration")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RESET UTILITY")
    print("=" * 60)
    print("\nChoose an option:")
    print("1. Full database reset (drop and recreate all tables)")
    print("2. Delete all user data only (keep structure)")
    print("3. Exit")
    print("")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        reset_database()
    elif choice == "2":
        delete_all_users()
    else:
        print("Exiting...")
