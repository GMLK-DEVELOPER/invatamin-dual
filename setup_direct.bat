@echo off
echo ======================================
echo Admin Panel Setup with MySQL Database
echo ======================================
echo.

REM Проверка наличия папки venv
IF EXIST venv (
    echo Виртуальная среда найдена, активируем её...
) ELSE (
    echo Создание виртуальной среды Python...
    python -m venv venv
    IF NOT EXIST venv (
        echo Ошибка: Не удалось создать виртуальную среду.
        echo Убедитесь, что Python 3.7+ установлен и доступен в PATH.
        pause
        exit /b 1
    )
    echo Виртуальная среда создана успешно.
)

REM Активация виртуальной среды
call venv\Scripts\activate.bat
echo Виртуальная среда активирована.

echo.
echo Установка необходимых пакетов...
pip install -r requirements.txt

echo.
echo Настройка базы данных MySQL...
python init_db.py

echo.
echo Создание таблиц напрямую (без миграций)...
python create_tables.py

echo.
echo Установка статических файлов...
call setup_static.bat

echo.
echo Установка завершена! Теперь вы можете запустить приложение:
echo python app.py
echo.
echo Для доступа к админ-панели перейдите по адресу: http://localhost:5000/admin/login
echo Логин: qwe
echo Пароль: qwe
echo.
echo Для выхода из виртуальной среды введите 'deactivate'
echo.
pause 