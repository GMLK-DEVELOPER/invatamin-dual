@echo off
echo ======================================
echo Запуск админ-панели на Flask
echo ======================================
echo.

REM Проверка наличия папки venv
IF EXIST venv (
    echo Виртуальная среда найдена, активируем её...
    call venv\Scripts\activate.bat
    echo Виртуальная среда активирована.
) ELSE (
    echo Виртуальная среда не найдена.
    echo Запуск без виртуальной среды...
    echo Для создания виртуальной среды запустите setup_admin.bat или setup_direct.bat
)

echo.
echo Запуск Flask-приложения...
python app.py

REM Если была активирована виртуальная среда, деактивируем её
IF EXIST venv (
    deactivate
) 