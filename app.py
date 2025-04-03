from flask import Flask, render_template, request, redirect, url_for
import socket

app = Flask(__name__)

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

# Обработка ошибок
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Получение IP-адреса машины
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Сервер запущен на:")
    print(f"* Локальный адрес: http://127.0.0.1:5000")
    print(f"* Сетевой адрес: http://{local_ip}:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 