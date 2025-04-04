from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from flask import current_app
import uuid

Base = declarative_base()

class User(Base, UserMixin):
    """User model for authentication and profile information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    profile_image = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships (uncomment and modify as needed)
    # posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')
    # comments = relationship('Comment', back_populates='author', cascade='all, delete-orphan')
    
    def __init__(self, name, email, password=None, is_admin=False, **kwargs):
        self.name = name
        self.email = email.lower()
        if password:
            self.set_password(password)
        self.is_admin = is_admin
        
        # Apply any additional attributes from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def set_password(self, password):
        """Set the password hash from a plain text password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        """Save the user to the database"""
        from app import db
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """Delete the user from the database"""
        from app import db
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, user_id):
        """Get a user by ID"""
        from app import db
        return db.session.query(cls).filter_by(id=user_id).first()
    
    @classmethod
    def get_by_email(cls, email):
        """Get a user by email"""
        from app import db
        return db.session.query(cls).filter_by(email=email.lower()).first()
    
    def to_dict(self):
        """Convert user to dictionary (for API responses)"""
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'profile_image': self.profile_image,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def has_permission(self, permission):
        """Check if user has a specific permission"""
        # For simplicity, we're just checking if the user is an admin
        # In a real app, you would implement a proper permission system
        if self.is_admin:
            return True
        
        # Example of a more complex permission system
        # if permission == 'posts.create' and self.is_active:
        #     return True
        
        return False
    
    def __repr__(self):
        return f'<User {self.id}: {self.email}>' 