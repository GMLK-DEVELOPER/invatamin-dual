#!/usr/bin/env python
import os
import shutil
import sys
import subprocess
import platform

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def main():
    print("=== Digital Agency Admin Panel Installation ===")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)
    
    # Create necessary directories
    print("\nCreating directories...")
    
    # Admin static directories
    create_directory("static/admin/css")
    create_directory("static/admin/js")
    create_directory("static/admin/img")
    create_directory("static/admin/video")
    
    # Create sample images and videos
    print("\nCreating placeholder images and videos...")
    
    # Create placeholder images if they don't exist
    if not os.path.exists("static/admin/img/logo.png"):
        # Check if any logo files exist in static/img
        found_logo = False
        for img_file in os.listdir("static/img"):
            if "logo" in img_file.lower():
                try:
                    shutil.copy(f"static/img/{img_file}", "static/admin/img/logo.png")
                    print(f"Copied logo from static/img/{img_file}")
                    found_logo = True
                    break
                except Exception as e:
                    print(f"Error copying logo: {str(e)}")
        
        if not found_logo:
            print("No logo found. Please add a logo.png file to static/admin/img/")
    
    if not os.path.exists("static/admin/img/logo-white.png"):
        # Check if any logo-white files exist in static/img
        found_logo_white = False
        for img_file in os.listdir("static/img"):
            if "logo-white" in img_file.lower():
                try:
                    shutil.copy(f"static/img/{img_file}", "static/admin/img/logo-white.png")
                    print(f"Copied white logo from static/img/{img_file}")
                    found_logo_white = True
                    break
                except Exception as e:
                    print(f"Error copying white logo: {str(e)}")
        
        if not found_logo_white and os.path.exists("static/admin/img/logo.png"):
            shutil.copy("static/admin/img/logo.png", "static/admin/img/logo-white.png")
            print("Created white logo from regular logo")
    
    # Create placeholder user images
    for i in range(1, 5):
        user_img = f"static/admin/img/user{i}.jpg"
        if not os.path.exists(user_img):
            # Check if any user/profile images exist in static/img
            found_user = False
            for img_file in os.listdir("static/img"):
                if "user" in img_file.lower() or "profile" in img_file.lower() or "avatar" in img_file.lower():
                    try:
                        shutil.copy(f"static/img/{img_file}", user_img)
                        print(f"Copied user image from static/img/{img_file} to {user_img}")
                        found_user = True
                        break
                    except Exception as e:
                        print(f"Error copying user image: {str(e)}")
            
            if not found_user:
                print(f"No image found for {user_img}. Please add it manually.")
    
    # Create placeholder profile image
    if not os.path.exists("static/admin/img/profile.jpg"):
        # Check if any profile images exist in static/img
        found_profile = False
        for img_file in os.listdir("static/img"):
            if "profile" in img_file.lower() or "avatar" in img_file.lower() or "user" in img_file.lower():
                try:
                    shutil.copy(f"static/img/{img_file}", "static/admin/img/profile.jpg")
                    print(f"Copied profile image from static/img/{img_file}")
                    found_profile = True
                    break
                except Exception as e:
                    print(f"Error copying profile image: {str(e)}")
        
        if not found_profile:
            print("No profile image found. Please add profile.jpg file to static/admin/img/")
    
    # Create placeholder login background image
    if not os.path.exists("static/admin/img/login-bg.jpg"):
        # Check if any background images exist in static/img
        found_bg = False
        for img_file in os.listdir("static/img"):
            if "background" in img_file.lower() or "bg" in img_file.lower() or "hero" in img_file.lower():
                try:
                    shutil.copy(f"static/img/{img_file}", "static/admin/img/login-bg.jpg")
                    print(f"Copied background image from static/img/{img_file}")
                    found_bg = True
                    break
                except Exception as e:
                    print(f"Error copying background image: {str(e)}")
        
        if not found_bg:
            print("No background image found. Please add login-bg.jpg file to static/admin/img/")
    
    # Create placeholder login video
    if not os.path.exists("static/admin/video/login-bg.mp4"):
        print("Login background video not found. Please add login-bg.mp4 file to static/admin/video/")
    
    # Install required packages
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {str(e)}")
    
    print("\n=== Installation Complete ===")
    print("\nYou can now access the admin panel at: http://localhost:5000/admin/login")
    print("Default credentials:")
    print("  Username: qwe")
    print("  Password: qwe")
    print("\nIMPORTANT: For production, please change the default credentials and secret key in app.py")
    
    # Detect operating system and suggest how to run the application
    system = platform.system()
    if system == "Windows":
        print("\nTo run the application on Windows:")
        print("  python app.py")
        print("  or double-click on run.bat")
    elif system == "Linux" or system == "Darwin":  # Darwin is MacOS
        print("\nTo run the application on Linux/MacOS:")
        print("  python3 app.py")
        print("  or chmod +x run.sh && ./run.sh")
    
    print("\nEnjoy your new admin panel!")

if __name__ == "__main__":
    main() 