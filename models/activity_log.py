from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class ActivityLog(Base):
    """Model for tracking user activities in the admin panel"""
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 can be up to 45 chars
    user_agent = Column(String(255), nullable=True)
    endpoint = Column(String(100), nullable=True)
    method = Column(String(10), nullable=True)
    params = Column(Text, nullable=True)
    status_code = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='activity_logs')
    
    def __init__(self, user_id, activity_type, description=None, ip_address=None, 
                 user_agent=None, endpoint=None, method=None, params=None, status_code=None):
        self.user_id = user_id
        self.activity_type = activity_type
        self.description = description
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.endpoint = endpoint
        self.method = method
        self.params = params
        self.status_code = status_code
    
    def save(self):
        """Save the activity log to the database"""
        from app import db
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_user_activity(cls, user_id, limit=50):
        """Get recent activity for a specific user"""
        from app import db
        return (db.session.query(cls)
                .filter_by(user_id=user_id)
                .order_by(cls.created_at.desc())
                .limit(limit)
                .all())
    
    @classmethod
    def get_recent_activity(cls, limit=50):
        """Get recent activity across all users"""
        from app import db
        return (db.session.query(cls)
                .order_by(cls.created_at.desc())
                .limit(limit)
                .all())
    
    @classmethod
    def search(cls, activity_type=None, user_id=None, start_date=None, end_date=None, limit=50):
        """Search activity logs with filters"""
        from app import db
        
        query = db.session.query(cls)
        
        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(cls.created_at >= start_date)
        
        if end_date:
            query = query.filter(cls.created_at <= end_date)
        
        return query.order_by(cls.created_at.desc()).limit(limit).all()
    
    def to_dict(self):
        """Convert activity log to dictionary (for API responses)"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'ip_address': self.ip_address,
            'endpoint': self.endpoint,
            'method': self.method,
            'status_code': self.status_code,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ActivityLog {self.id}: {self.activity_type}>' 