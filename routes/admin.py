from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from forms.admin import LoginForm, ForgotPasswordForm, ResetPasswordForm
from utils.token import generate_token, verify_token
from utils.email import send_password_reset_email
from utils.decorators import admin_required
import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard homepage"""
    stats = {
        'total_users': User.query.count(),
        'new_users': User.query.filter(
            User.created_at >= datetime.datetime.now() - datetime.timedelta(days=30)
        ).count(),
        'total_products': 150,  # Example static data, replace with actual DB query
        'total_orders': 1250,   # Example static data, replace with actual DB query
    }
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          title='Dashboard',
                          stats=stats,
                          recent_users=recent_users)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        # Check if user exists
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check if user exists and is an admin and password is correct
        if user and user.is_admin and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            
            # Record login time
            user.last_login = datetime.datetime.now()
            user.save()
            
            # Redirect to the requested page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin.index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('admin/login.html', title='Admin Login', form=form)

@admin.route('/logout')
@login_required
def logout():
    """Logout route for admin users"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('admin.login'))

@admin.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Always show success message even if email doesn't exist (security)
        if user and user.is_admin:
            # Generate token
            token = generate_token(user.id)
            
            # Send reset email
            reset_url = url_for('admin.reset_password', token=token, _external=True)
            send_password_reset_email(user.email, reset_url)
            
        flash('If your email exists in our system, you will receive a password reset link', 'success')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/forgot_password.html', title='Forgot Password', form=form)

@admin.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    
    # Verify token
    user_id = verify_token(token)
    
    if not user_id:
        flash('Invalid or expired reset link. Please try again.', 'danger')
        return redirect(url_for('admin.forgot_password'))
    
    # Get user
    user = User.query.get(user_id)
    
    # Check if user exists and is an admin
    if not user or not user.is_admin:
        flash('Invalid reset link', 'danger')
        return redirect(url_for('admin.login'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        # Update password
        user.set_password(form.password.data)
        user.save()
        
        flash('Your password has been updated. You can now log in with your new password', 'success')
        return redirect(url_for('admin.login'))
    
    return render_template('admin/reset_password.html', title='Reset Password', form=form)

@admin.route('/profile')
@login_required
@admin_required
def profile():
    """Admin profile page"""
    return render_template('admin/profile.html', title='My Profile')

@admin.route('/users')
@login_required
@admin_required
def users():
    """Users management page"""
    users = User.query.all()
    return render_template('admin/users.html', title='User Management', users=users)

@admin.route('/settings')
@login_required
@admin_required
def settings():
    """Admin settings page"""
    return render_template('admin/settings.html', title='Settings')

# Error handler for 403 errors (Forbidden)
@admin.app_errorhandler(403)
def forbidden_error(error):
    return render_template('admin/errors/403.html', title='Access Denied'), 403

# Error handler for 404 errors (Not Found)
@admin.app_errorhandler(404)
def not_found_error(error):
    return render_template('admin/errors/404.html', title='Page Not Found'), 404

# Error handler for 500 errors (Internal Server Error)
@admin.app_errorhandler(500)
def internal_error(error):
    return render_template('admin/errors/500.html', title='Server Error'), 500 