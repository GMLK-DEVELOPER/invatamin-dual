from functools import wraps
from flask import flash, redirect, url_for, abort, request, current_app
from flask_login import current_user

def admin_required(f):
    """
    Decorator to restrict access to admin users only
    
    Usage:
        @login_required  # Must be used along with login_required
        @admin_required
        def admin_view():
            # Only accessible to admin users
            return "Admin view"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            
            # Check if request is AJAX/API
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {'error': 'Unauthorized', 'message': 'Admin access required'}, 403
                
            # Normal request
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """
    Decorator to restrict access based on user permissions
    
    Usage:
        @login_required
        @permission_required('users.edit')
        def edit_user():
            # Only accessible to users with 'users.edit' permission
            return "Edit user"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_permission(permission):
                flash('You do not have permission to access this page.', 'danger')
                
                # Check if request is AJAX/API
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return {'error': 'Unauthorized', 'message': f'Required permission: {permission}'}, 403
                    
                # Normal request
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_activity(activity_type):
    """
    Decorator to log admin activity
    
    Usage:
        @login_required
        @admin_required
        @log_activity('user.create')
        def create_user():
            # This action will be logged
            return "User created"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Execute the original function
            result = f(*args, **kwargs)
            
            # Log the activity (if the function was successful)
            if current_user.is_authenticated:
                try:
                    # Import here to avoid circular imports
                    from models.activity_log import ActivityLog
                    
                    # Create log entry
                    log = ActivityLog(
                        user_id=current_user.id,
                        activity_type=activity_type,
                        ip_address=request.remote_addr,
                        user_agent=request.user_agent.string,
                        endpoint=request.endpoint,
                        method=request.method,
                        params=str(request.view_args),
                    )
                    log.save()
                except Exception as e:
                    current_app.logger.error(f"Failed to log activity: {str(e)}")
            
            return result
        return decorated_function
    return decorator 