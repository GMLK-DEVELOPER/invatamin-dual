#!/bin/bash

echo "======================================"
echo "Admin Panel Setup with MySQL Database"
echo "======================================"
echo

# Проверка наличия папки venv
if [ -d "venv" ]; then
    echo "Виртуальная среда найдена, активируем её..."
else
    echo "Создание виртуальной среды Python..."
    python3 -m venv venv
    if [ ! -d "venv" ]; then
        echo "Ошибка: Не удалось создать виртуальную среду."
        echo "Убедитесь, что Python 3.7+ установлен."
        exit 1
    fi
    echo "Виртуальная среда создана успешно."
fi

# Активация виртуальной среды
source venv/bin/activate
echo "Виртуальная среда активирована."

echo
echo "Установка необходимых пакетов..."
pip install -r requirements.txt

echo
echo "Настройка базы данных MySQL..."
python init_db.py

# Спросить пользователя, какой способ установки предпочтительнее
echo
echo "Выберите способ создания таблиц:"
echo "1. Использовать миграции Flask (рекомендуется)"
echo "2. Создать таблицы напрямую (без миграций)"
read -p "Выберите опцию (1/2): " option

if [ "$option" == "1" ]; then
    echo
    echo "Создание таблиц с использованием миграций..."
    flask --app app db init
    flask --app app db migrate -m "Initial migration"
    flask --app app db upgrade
else
    echo
    echo "Создание таблиц напрямую..."
    python create_tables.py
fi

echo
echo "Установка статических файлов..."
chmod +x setup_static.sh
./setup_static.sh

echo
echo "Установка завершена! Теперь вы можете запустить приложение:"
echo "python app.py"
echo
echo "Для доступа к админ-панели перейдите по адресу: http://localhost:5000/admin/login"
echo "Логин: qwe"
echo "Пароль: qwe"
echo
echo "Для выхода из виртуальной среды введите 'deactivate'"
echo

# Спросить пользователя, хочет ли он запустить приложение сейчас
read -p "Хотите запустить приложение сейчас? (y/n): " run_option
if [ "$run_option" == "y" ] || [ "$run_option" == "Y" ]; then
    python app.py
fi 