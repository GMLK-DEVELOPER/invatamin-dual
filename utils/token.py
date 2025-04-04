from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app
import datetime

def generate_token(user_id, expiration=3600):
    """
    Generate a secure token for password reset or email verification
    
    Args:
        user_id: The user ID to encode in the token
        expiration: Token expiration time in seconds (default: 1 hour)
        
    Returns:
        A URL-safe encoded token
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token_data = {
        'user_id': user_id,
        'exp': datetime.datetime.now().timestamp() + expiration
    }
    return serializer.dumps(token_data, salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'password-reset-salt'))

def verify_token(token, max_age=3600):
    """
    Verify a token and return the user ID if valid
    
    Args:
        token: The token to verify
        max_age: Maximum age of the token in seconds (default: 1 hour)
        
    Returns:
        The user ID if the token is valid, None otherwise
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        token_data = serializer.loads(
            token,
            salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'password-reset-salt'),
            max_age=max_age
        )
        
        # Check if token is expired
        if 'exp' in token_data and token_data['exp'] < datetime.datetime.now().timestamp():
            return None
            
        return token_data['user_id']
    except (SignatureExpired, BadSignature):
        return None 