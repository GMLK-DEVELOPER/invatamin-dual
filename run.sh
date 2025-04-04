#!/bin/bash

echo "======================================"
echo "Запуск админ-панели на Flask"
echo "======================================"
echo

# Проверка наличия папки venv
if [ -d "venv" ]; then
    echo "Виртуальная среда найдена, активируем её..."
    source venv/bin/activate
    echo "Виртуальная среда активирована."
else
    echo "Виртуальная среда не найдена."
    echo "Запуск без виртуальной среды..."
    echo "Для создания виртуальной среды запустите setup.sh"
fi

echo
echo "Запуск Flask-приложения..."
python app.py

# После завершения работы приложения, деактивируем виртуальную среду
if [ -d "venv" ]; then
    deactivate
fi 