#!/bin/bash

echo "======================================"
echo "Установка статических файлов для админ-панели"
echo "======================================"
echo

# Создаем необходимые директории, если они не существуют
echo "Создание структуры директорий..."
mkdir -p static/admin/css
mkdir -p static/admin/js
mkdir -p static/admin/img
mkdir -p static/admin/fonts
mkdir -p static/admin/video
mkdir -p static/img

# Загружаем изображение профиля, если оно не существует
if [ ! -f static/admin/img/profile.jpg ]; then
    echo "Загрузка изображения профиля..."
    curl -o static/admin/img/profile.jpg https://i.pravatar.cc/300
fi

# Загружаем иконку сайта, если она не существует
if [ ! -f static/img/favicon.ico ]; then
    echo "Загрузка favicon..."
    curl -o static/img/favicon.ico https://www.google.com/favicon.ico
fi

# Создаем файл robots.txt, если он не существует
if [ ! -f static/robots.txt ]; then
    echo "Создание robots.txt..."
    cat > static/robots.txt << EOL
User-agent: *
Disallow: /admin/
Disallow: /static/admin/

User-agent: *
Allow: /
EOL
fi

# Создаем фоновое видео для админ-панели, если оно не существует
if [ ! -f static/admin/video/login-bg.mp4 ]; then
    echo "Загрузка фонового видео..."
    curl -o static/admin/video/login-bg.mp4 https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_10mb.mp4
fi

echo
echo "Установка статических файлов завершена!"
echo 