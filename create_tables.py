"""
Script to create database tables directly without using migrations
"""
import sys
from app import app, db, User

def create_tables():
    try:
        print("Creating tables directly...")
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Check if there are any admin users
            if not User.query.filter_by(role='admin').first():
                # Create default admin user
                admin = User(
                    username='qwe',
                    name='Administrator',
                    email='admin@example.com',
                    role='admin'
                )
                admin.set_password('qwe')
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created!")
            else:
                print("Admin user already exists.")
                
            print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables() 