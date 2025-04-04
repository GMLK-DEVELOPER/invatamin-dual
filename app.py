from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import socket
import os
import datetime
from functools import wraps
import hashlib
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import sys

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key in production
csrf = CSRFProtect(app)  # Initialize CSRF protection

# Add a context processor to add the current year to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qwe:qwe@localhost/qwe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def check_password(self, password):
        # In a real app, use a secure password hashing method like bcrypt
        return self.password == hashlib.sha256(password.encode()).hexdigest()
    
    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    permissions = db.Column(db.Text, nullable=True)  # Храним как JSON строку
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def get_permissions(self):
        if not self.permissions:
            return []
        import json
        return json.loads(self.permissions)
    
    def set_permissions(self, permissions_list):
        import json
        self.permissions = json.dumps(permissions_list)

# Helper functions
def get_hashed_password(password):
    # In a real app, use a secure password hashing method like bcrypt
    return hashlib.sha256(password.encode()).hexdigest()

def is_logged_in():
    return 'admin_user' in session

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access the admin area', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database
def initialize_database():
    # Create tables if they don't exist
    with app.app_context():
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
            
        # Проверяем наличие базовых ролей
        basic_roles = ['admin', 'user', 'moderator']
        for role_name in basic_roles:
            if not Role.query.filter_by(name=role_name).first():
                new_role = Role(name=role_name)
                
                if role_name == 'admin':
                    new_role.description = 'Administrator with full access'
                    new_role.set_permissions(['view_users', 'edit_users', 'delete_users', 
                                             'manage_roles', 'view_settings', 'edit_settings'])
                elif role_name == 'user':
                    new_role.description = 'Regular user with limited access'
                    new_role.set_permissions(['view_users'])
                elif role_name == 'moderator':
                    new_role.description = 'Moderator with limited administrative access'
                    new_role.set_permissions(['view_users', 'edit_users', 'view_settings'])
                
                db.session.add(new_role)
                db.session.commit()
                print(f"Basic role '{role_name}' created!")

# Вызов инициализации при запуске
with app.app_context():
    initialize_database()

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html', active_page='home')

@app.route('/about')
def about():
    return render_template('about.html', active_page='about')

@app.route('/service')
def service():
    return render_template('service.html', active_page='service')

@app.route('/project')
def project():
    return render_template('project.html', active_page='project')

@app.route('/team')
def team():
    return render_template('team.html', active_page='team')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html', active_page='testimonial')

@app.route('/404')
def error_404():
    return render_template('404.html', active_page='404')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Здесь можно добавить логику для отправки сообщений
        # Например, отправка email или сохранение в БД
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # После обработки формы можно сделать редирект
        return redirect(url_for('contact', success=True))
    
    success = request.args.get('success', False)
    return render_template('contact.html', active_page='contact', success=success)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if is_logged_in():
        return redirect(url_for('admin_dashboard'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['admin_user'] = username
            session['admin_name'] = user.name
            session['admin_role'] = user.role
            session.permanent = remember
            
            # Update last login time
            user.last_login = datetime.datetime.now()
            db.session.commit()
            
            flash('You have been successfully logged in', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid username or password'
    
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_user', None)
    session.pop('admin_name', None)
    session.pop('admin_role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Get counts for dashboard
    user_count = User.query.count()
    post_count = Post.query.count()
    page_count = Page.query.count()
    comment_count = Comment.query.count()
    
    # Get recent posts
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Get current_user info
    current_user = {
        'name': session.get('admin_name', 'Admin'),
        'username': session.get('admin_user', ''),
        'is_authenticated': is_logged_in()
    }
    
    # Get Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Get current date for the footer
    now = datetime.datetime.now()
    
    return render_template('admin/dashboard.html', 
                           active_menu='dashboard', 
                           current_user=current_user,
                           now=now,
                           user_count=user_count,
                           post_count=post_count,
                           page_count=page_count,
                           comment_count=comment_count,
                           recent_posts=recent_posts,
                           recent_users=recent_users,
                           python_version=python_version)

@app.route('/admin/users')
@admin_required
def admin_users_list():
    # Get all users from database
    users = User.query.all()
    
    return render_template('admin/users_list.html', 
                           active_menu='users', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now(),
                           users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('admin_add_user'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('admin_add_user'))
        
        # Create new user
        user = User(
            username=username,
            name=name,
            email=email,
            role=role
        )
        user.set_password(password)
        
        # Save user to database
        db.session.add(user)
        db.session.commit()
        
        flash('User added successfully', 'success')
        return redirect(url_for('admin_users_list'))
    
    return render_template('admin/add_user.html', 
                           active_menu='users', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/users/roles', methods=['GET', 'POST'])
@admin_required
def admin_user_roles():
    if request.method == 'POST':
        # Обработка формы добавления или изменения роли
        name = request.form.get('name')
        description = request.form.get('description')
        permissions = request.form.getlist('permissions[]')
        role_id = request.form.get('role_id')
        action = request.form.get('action', 'edit')  # По умолчанию действие - редактирование
        
        # Добавление сообщения для отладки
        print(f"Form data: name={name}, description={description}, permissions={permissions}, role_id={role_id}, action={action}")
        
        if action == 'delete' and role_id:
            # Режим удаления роли
            role = Role.query.get(role_id)
            if role:
                if role.name in ['admin', 'user', 'moderator']:
                    flash(f'Системную роль "{role.name}" нельзя удалить', 'danger')
                else:
                    # Найти всех пользователей с этой ролью и изменить их роль на 'user'
                    users_with_role = User.query.filter_by(role=role.name).all()
                    for user in users_with_role:
                        user.role = 'user'
                    
                    # Удалить роль
                    role_name = role.name
                    db.session.delete(role)
                    db.session.commit()
                    flash(f'Роль "{role_name}" успешно удалена. Пользователи переназначены на роль "user"', 'success')
            else:
                flash('Роль не найдена', 'danger')
        elif role_id:
            # Режим редактирования существующей роли
            role = Role.query.get(role_id)
            if role:
                if role.name not in ['admin', 'user', 'moderator'] or role.name == name:
                    # Обновляем только описание и права для системных ролей
                    role.description = description
                    role.set_permissions(permissions)
                    db.session.commit()
                    flash(f'Роль "{role.name}" успешно обновлена', 'success')
                else:
                    flash('Нельзя изменить имя системной роли', 'danger')
            else:
                flash('Роль не найдена', 'danger')
        else:
            # Режим добавления новой роли
            
            # Проверка на дубликат имени роли
            existing_role = Role.query.filter_by(name=name).first()
            if existing_role:
                flash(f'Роль с именем "{name}" уже существует', 'danger')
            else:
                new_role = Role(name=name, description=description)
                new_role.set_permissions(permissions)
                db.session.add(new_role)
                db.session.commit()
                flash(f'Роль "{name}" успешно создана', 'success')
        
        return redirect(url_for('admin_user_roles'))
    
    # Получаем все роли из базы данных
    roles_from_db = Role.query.all()
    
    # Подготавливаем список ролей для шаблона
    roles = []
    for role in roles_from_db:
        # Подсчитываем количество пользователей с этой ролью
        users_count = User.query.filter_by(role=role.name).count()
        
        roles.append({
            'id': role.id,
            'name': role.name,
            'description': role.description,
            'permissions': role.get_permissions(),
            'users_count': users_count,
            'created_at': role.created_at
        })
    
    # Если базовых ролей нет в базе, создаем их
    basic_roles = ['admin', 'user', 'moderator']
    existing_role_names = [role['name'] for role in roles]
    
    for basic_role in basic_roles:
        if basic_role not in existing_role_names:
            # Создаем базовую роль
            new_role = Role(name=basic_role)
            
            if basic_role == 'admin':
                new_role.description = 'Administrator with full access'
                new_role.set_permissions(['view_users', 'edit_users', 'delete_users', 
                                         'manage_roles', 'view_settings', 'edit_settings'])
            elif basic_role == 'user':
                new_role.description = 'Regular user with limited access'
                new_role.set_permissions(['view_users'])
            elif basic_role == 'moderator':
                new_role.description = 'Moderator with limited administrative access'
                new_role.set_permissions(['view_users', 'edit_users', 'view_settings'])
            
            db.session.add(new_role)
            db.session.commit()
            
            # Добавляем в список для отображения
            users_count = User.query.filter_by(role=basic_role).count()
            roles.append({
                'id': new_role.id,
                'name': new_role.name,
                'description': new_role.description,
                'permissions': new_role.get_permissions(),
                'users_count': users_count,
                'created_at': new_role.created_at
            })
    
    return render_template('admin/user_roles.html', 
                           active_menu='users', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now(),
                           roles=roles)

@app.route('/admin/profile')
@admin_required
def admin_profile():
    return render_template('admin/profile.html', 
                           active_menu='profile', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/settings')
@admin_required
def admin_general_settings():
    return render_template('admin/settings.html', 
                           active_menu='settings', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/appearance')
@admin_required
def admin_appearance():
    return render_template('admin/appearance.html', 
                           active_menu='settings', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/pages')
@admin_required
def admin_pages_list():
    return render_template('admin/pages_list.html', 
                           active_menu='pages', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/pages/add')
@admin_required
def admin_add_page():
    return render_template('admin/add_page.html', 
                           active_menu='pages', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/blog/posts')
@admin_required
def admin_posts_list():
    return render_template('admin/posts_list.html', 
                           active_menu='blog', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/blog/posts/add')
@admin_required
def admin_add_post():
    return render_template('admin/add_post.html', 
                           active_menu='blog', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/blog/categories')
@admin_required
def admin_categories():
    return render_template('admin/categories.html', 
                           active_menu='blog', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/blog/tags')
@admin_required
def admin_tags():
    return render_template('admin/tags.html', 
                           active_menu='blog', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/blog/comments')
@admin_required
def admin_comments():
    return render_template('admin/comments.html', 
                           active_menu='blog', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/media')
@admin_required
def admin_media_library():
    return render_template('admin/media_library.html', 
                           active_menu='media', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/forms')
@admin_required
def admin_forms():
    return render_template('admin/forms.html', 
                           active_menu='forms', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    return render_template('admin/analytics.html', 
                           active_menu='analytics', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/backups')
@admin_required
def admin_backups():
    return render_template('admin/backups.html', 
                           active_menu='settings', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/account-settings')
@admin_required
def admin_account_settings():
    return render_template('admin/account_settings.html', 
                           active_menu='settings', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/notifications')
@admin_required
def admin_notifications():
    return render_template('admin/notifications.html', 
                           active_menu='notifications', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now())

@app.route('/admin/search')
@admin_required
def admin_search():
    query = request.args.get('q', '')
    # In a real app, perform the search operation here
    results = []
    return render_template('admin/search_results.html', 
                           active_menu='search', 
                           current_user={'name': session.get('admin_name', 'Admin')},
                           now=datetime.datetime.now(),
                           query=query,
                           results=results)

@app.route('/admin/forgot-password', methods=['GET', 'POST'])
def admin_forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # In a real app, send password reset email
        flash('Password reset instructions have been sent to your email', 'info')
        return redirect(url_for('admin_login'))
    return render_template('admin/forgot_password.html', 
                         current_user={'name': 'Guest', 'is_authenticated': False})

@app.route('/admin/register')
def admin_register():
    # In this admin panel, typically registration is not open but controlled by admins
    return render_template('admin/register.html',
                         current_user={'name': 'Guest', 'is_authenticated': False})

@app.route('/admin/reset-password/<token>', methods=['GET', 'POST'])
def admin_reset_password(token):
    # In a real app, verify the token and allow password reset
    # For now, just show the reset password form
    class MockForm:
        def __init__(self):
            self.csrf_token = ''
            self.password = ''
            self.confirm_password = ''
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            # In a real app, update the password in the database
            flash('Your password has been reset successfully', 'success')
            return redirect(url_for('admin_login'))
    
    return render_template('admin/reset_password.html', 
                          form=MockForm(),
                          current_user={'name': 'Guest', 'is_authenticated': False})

# Models for admin panel
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    posts = db.relationship('Post', backref='category', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text, nullable=True)
    featured_image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='draft')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    author = db.relationship('User', backref='posts')
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pending')
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    
class Page(db.Model):
    __tablename__ = 'pages'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='published')
    featured_image = db.Column(db.String(255), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    author = db.relationship('User', backref='pages')

# Обработка ошибок
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Получение IP-адреса машины
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Сервер запущен на:")
    print(f"* Локальный адрес: http://127.0.0.1:5000")
    print(f"* Сетевой адрес: http://{local_ip}:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 