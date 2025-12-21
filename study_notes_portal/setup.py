#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_notes_portal.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from notes_portal.models import Manager

def create_managers():
    """Create managers that will work with your login system"""
    print("Creating managers...")
    
    managers = [
        {"username": "admin", "password": "admin123"},
        {"username": "professor1", "password": "prof123"},
        {"username": "professor2", "password": "prof456"},
    ]
    
    for data in managers:
        if not Manager.objects.filter(username=data["username"]).exists():
            manager = Manager(username=data["username"])
            manager.set_password(data["password"])  # This hashes the password
            manager.save()
            print(f"✓ Created manager: {manager.username}")
        else:
            print(f"→ Manager '{data['username']}' already exists")
    
    print("\n✅ Manager Credentials:")
    print("1. Username: admin, Password: admin123")
    print("2. Username: professor1, Password: prof123")
    print("3. Username: professor2, Password: prof456")
    print("\n⚠️  IMPORTANT: To create MORE managers:")
    print("1. Go to: http://127.0.0.1:8000/admin/")
    print("2. Login with superuser credentials")
    print("3. Click 'Managers' → 'Add Manager'")
    print("4. Enter username and password (it will be hashed automatically)")

if __name__ == "__main__":
    create_managers()