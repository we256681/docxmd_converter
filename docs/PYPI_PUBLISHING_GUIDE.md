# 📦 Руководство по публикации на PyPI

## 🎯 Подготовка к публикации

### 1. Предварительные требования

```bash
# Установка инструментов сборки
pip install build twine bump2version

# Создание аккаунтов
# - https://test.pypi.org/ (для тестирования)
# - https://pypi.org/ (для продакшена)
```

### 2. Настройка API токенов

#### TestPyPI
1. Зайдите на https://test.pypi.org/manage/account/
2. Создайте API токен
3. Сохраните токен в безопасном месте

#### PyPI
1. Зайдите на https://pypi.org/manage/account/
2. Создайте API токен
3. Сохраните токен в безопасном месте

### 3. Настройка .pypirc (опционально)

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-ваш-токен-здесь

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-ваш-тестовый-токен-здесь
```

## 🚀 Процесс публикации

### Шаг 1: Подготовка версии

```bash
# Обновление версии (опционально)
bump2version patch  # или minor, major

# Проверка версии в файлах
grep -r "version.*3.1.0" pyproject.toml setup.py
```

### Шаг 2: Сборка пакета

```bash
# Автоматическая сборка
python scripts/build_package.py

# Или вручную
python -m build
python -m twine check dist/*
```

### Шаг 3: Тестовая публикация

```bash
# Публикация на TestPyPI
python scripts/publish_test.py

# Или вручную
python -m twine upload --repository testpypi dist/*
```

### Шаг 4: Тестирование установки

```bash
# Создание тестового окружения
python -m venv test_env
source test_env/bin/activate

# Установка с TestPyPI
pip install -i https://test.pypi.org/simple/ docxmd-converter

# Тестирование
python -c "from docxmd_converter import IntelligentProcessor; print('OK')"
```

### Шаг 5: Публикация на PyPI

```bash
# Финальная публикация
python scripts/publish_pypi.py

# Или вручную
python -m twine upload dist/*
```

## 📋 Чек-лист перед публикацией

### ✅ Код и тесты
- [ ] Все тесты проходят
- [ ] Код отформатирован (black, isort)
- [ ] Линтер не выдает ошибок (flake8)
- [ ] Типы проверены (mypy)

### ✅ Документация
- [ ] README.md обновлен
- [ ] CHANGELOG.md содержит изменения
- [ ] Версия увеличена во всех файлах
- [ ] Примеры кода работают

### ✅ Конфигурация
- [ ] pyproject.toml корректен
- [ ] setup.py актуален
- [ ] MANIFEST.in включает все нужные файлы
- [ ] requirements.txt обновлен

### ✅ Git
- [ ] Все изменения закоммичены
- [ ] Создан тег версии
- [ ] Изменения запушены в репозиторий

## 🔧 Структура файлов для PyPI

```
docxmd_converter/
├── pyproject.toml          # ✅ Основная конфигурация
├── setup.py               # ✅ Дополнительная настройка
├── README.md              # ✅ Описание для PyPI
├── LICENSE                # ✅ Лицензия
├── MANIFEST.in            # ✅ Включаемые файлы
├── requirements.txt       # ✅ Зависимости
├── CHANGELOG.md           # ✅ История изменений
├── src/                   # ✅ Исходный код
│   └── docxmd_converter/
│       ├── __init__.py    # ✅ Экспорты
│       └── ...
├── config/                # ✅ Конфигурация
├── data/                  # ✅ Данные
└── scripts/               # ✅ Скрипты публикации
```

## 🚨 Важные моменты

### ⚠️ Версионирование
- Версии на PyPI нельзя перезаписать
- Используйте семантическое версионирование (SemVer)
- Тестируйте на TestPyPI перед публикацией

### ⚠️ Зависимости
- Указывайте минимальные версии зависимостей
- Тестируйте с разными версиями Python
- Избегайте слишком строгих ограничений

### ⚠️ Безопасность
- Не включайте секреты в код
- Используйте API токены вместо паролей
- Проверяйте права доступа к пакету

## 🔄 Автоматизация

### GitHub Actions (пример)

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## 📊 После публикации

### 1. Проверка
- Проверьте страницу пакета на PyPI
- Убедитесь, что установка работает
- Проверьте отображение README

### 2. Документация
- Обновите документацию с новой версией
- Создайте release на GitHub
- Обновите примеры использования

### 3. Мониторинг
- Следите за загрузками
- Отвечайте на issues
- Планируйте следующие версии

## 🆘 Решение проблем

### Ошибка: "File already exists"
```bash
# Увеличьте версию и пересоберите
bump2version patch
python -m build
```

### Ошибка: "Invalid credentials"
```bash
# Проверьте токен и username
# Username должен быть __token__
```

### Ошибка: "Package validation failed"
```bash
# Проверьте пакет
python -m twine check dist/*
```

---

**Удачной публикации! 🚀**