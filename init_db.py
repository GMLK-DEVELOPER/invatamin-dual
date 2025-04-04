# Database Initialization Script
import pymysql
import os
import sys
from getpass import getpass

def create_database():
    try:
        # Connect to MySQL server
        print("Connecting to MySQL server...")
        username = input("Enter MySQL username (default: root): ") or "root"
        password = getpass("Enter MySQL password (leave blank if none): ")
        
        # Connect to MySQL
        connection = pymysql.connect(
            host='localhost',
            user=username,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("Connected to MySQL successfully!")
        
        # Create database
        db_name = input("Enter database name (default: admin_panel): ") or "admin_panel"
        with connection.cursor() as cursor:
            sql = f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            cursor.execute(sql)
            print(f"Database '{db_name}' created successfully!")
        
        # Create database URL for Flask
        db_url = f"mysql+pymysql://{username}:{password}@localhost/{db_name}"
        
        # Update app.py with the database URL
        update_app_config(db_url)
        
        print("\nDatabase initialized successfully!")
        print(f"Database URL: mysql+pymysql://{username}:******@localhost/{db_name}")
        print("\nNow run the following commands to set up the tables:")
        print("flask --app app db init")
        print("flask --app app db migrate -m 'Initial migration'")
        print("flask --app app db upgrade")
        
        # Ask if user wants to run migration commands now
        run_migrations = input("\nDo you want to run migration commands now? (y/n): ").lower() == 'y'
        if run_migrations:
            os.system("flask --app app db init")
            os.system("flask --app app db migrate -m 'Initial migration'")
            os.system("flask --app app db upgrade")
            print("\nMigrations completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals():
            connection.close()

def update_app_config(db_url):
    """Update the database URL in app.py"""
    try:
        with open('app.py', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace the database configuration line
        old_config = "app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/admin_panel'"
        
        # Попробуем найти текущую конфигурацию, если она отличается
        import re
        match = re.search(r"app\.config\['SQLALCHEMY_DATABASE_URI'\]\s*=\s*['\"](.*?)['\"]", content)
        if match:
            old_config = f"app.config['SQLALCHEMY_DATABASE_URI'] = '{match.group(1)}'"
        
        new_config = f"app.config['SQLALCHEMY_DATABASE_URI'] = '{db_url}'"
        
        updated_content = content.replace(old_config, new_config)
        
        with open('app.py', 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        print("Database configuration updated in app.py!")
    except Exception as e:
        print(f"Failed to update app.py configuration: {e}")

if __name__ == '__main__':
    print("=== Admin Panel MySQL Database Initialization ===")
    create_database() 