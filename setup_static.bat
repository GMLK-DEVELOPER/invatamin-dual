@echo off
echo ======================================
echo Установка статических файлов для админ-панели
echo ======================================
echo.

REM Создаем необходимые директории, если они не существуют
echo Создание структуры директорий...
mkdir static\admin\css 2>nul
mkdir static\admin\js 2>nul
mkdir static\admin\img 2>nul
mkdir static\admin\fonts 2>nul
mkdir static\admin\video 2>nul

REM Загружаем изображение профиля, если оно не существует
if not exist static\admin\img\profile.jpg (
    echo Загрузка изображения профиля...
    curl -o static\admin\img\profile.jpg https://i.pravatar.cc/300
)

REM Загружаем иконку сайта, если она не существует
if not exist static\img\favicon.ico (
    echo Создание директории для favicon...
    mkdir static\img 2>nul
    echo Загрузка favicon...
    curl -o static\img\favicon.ico https://www.google.com/favicon.ico
)

REM Создаем файл robots.txt, если он не существует
if not exist static\robots.txt (
    echo Создание robots.txt...
    (
        echo User-agent: *
        echo Disallow: /admin/
        echo Disallow: /static/admin/
        echo.
        echo User-agent: *
        echo Allow: /
    ) > static\robots.txt
)

REM Создаем фоновое видео для админ-панели, если оно не существует
if not exist static\admin\video\login-bg.mp4 (
    echo Загрузка фонового видео...
    curl -o static\admin\video\login-bg.mp4 https://sample-videos.com/video123/mp4/240/big_buck_bunny_240p_10mb.mp4
)

echo.
echo Установка статических файлов завершена!
echo.

pause 