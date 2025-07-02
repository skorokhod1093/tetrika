# Тестовые задания

## Структура
- task1/solution.py — декоратор strict
- task2/solution.py — парсер Википедии
- task3/solution.py — вычисление времени
- test_solution.py — тесты для каждой задачи

## Настройка виртуального окружения (руками)

### Windows
```bat
python3 -m venv env
venv\Scripts\activate.bat
```

### Linux
```bash
python3 -m venv env
source venv/bin/activate
```

### После активации окружения установите зависимости:
    `python3 -m pip install -r requirements.txt`

## Настройка виртуального окружения (через скрипт)
    `insall_deps.bat`

## Запуск тестов
    `python3 -m pytest task1/test_solution.py`
    `python3 -m pytest task2/test_solution.py`
    `python3 -m pytest task3/test_solution.py`

## Линтер и форматтер
```bash
flake8
black .
```