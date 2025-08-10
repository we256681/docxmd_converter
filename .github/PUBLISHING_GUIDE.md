# 📦 Руководство по публикации пакета DocxMD Converter на PyPI

## 🎯 Обзор

Данное руководство описывает все способы публикации пакета `docxmd-converter` на PyPI (Python Package Index) - как напрямую, так и через GitHub Actions.

---

## 🔧 Предварительная подготовка

### 1. Установка необходимых инструментов

```bash
# Установить инструменты сборки и публикации
pip install build twine bump2version

# Или установить через dev-зависимости проекта
pip install -e .[dev]
```

### 2. Создание аккаунта на PyPI

1. **Регистрация**: https://pypi.org/account/register/
2. **Test PyPI** (для тестирования): https://test.pypi.org/account/register/
3. **API Токены**: Настройте API токены для безопасной аутентификации

### 3. Настройка аутентификации

#### Вариант A: API токены (рекомендуемо)
```bash
# Создать ~/.pypirc
cat > ~/.pypirc << EOF
[distutils]
index-servers = pypi testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_API_TOKEN_HERE
EOF

chmod 600 ~/.pypirc
```

#### Вариант B: Username/Password (устаревший)
```bash
# В ~/.pypirc указать username и password
[pypi]
username = your_username
password = your_password
```

---

## 🚀 Способ 1: Прямая публикация через командную строку

### Шаг 1: Обновление версии

```bash
# Автоматическое обновление версии (рекомендуемо)
bump2version patch  # 2.0.1 -> 2.0.2
bump2version minor  # 2.0.1 -> 2.1.0
bump2version major  # 2.0.1 -> 3.0.0

# Или ручное обновление в pyproject.toml:
# version = "2.0.2"
```

### Шаг 2: Сборка пакета

```bash
# Очистить предыдущие сборки
rm -rf dist/ build/ *.egg-info/

# Собрать пакет
python -m build

# Проверить созданные файлы
ls -la dist/
# docxmd_converter-2.0.2-py3-none-any.whl
# docxmd_converter-2.0.2.tar.gz
```

### Шаг 3: Проверка пакета

```bash
# Проверить пакет на ошибки
twine check dist/*

# Проверить установку локально
pip install dist/docxmd_converter-2.0.2-py3-none-any.whl --force-reinstall
docxmd --version
```

### Шаг 4: Тестовая публикация

```bash
# Загрузить на Test PyPI
twine upload --repository testpypi dist/*

# Проверить установку с Test PyPI
pip install --index-url https://test.pypi.org/simple/ docxmd-converter
```

### Шаг 5: Продакшн публикация

```bash
# Загрузить на PyPI
twine upload dist/*

# Или указать конкретные файлы
twine upload dist/docxmd_converter-2.0.2*
```

### Шаг 6: Проверка публикации

```bash
# Проверить на PyPI
open https://pypi.org/project/docxmd-converter/

# Установить опубликованный пакет
pip install docxmd-converter --upgrade
docxmd --version
```

---

## 🤖 Способ 2: Автоматическая публикация через GitHub Actions

### Настройка GitHub Secrets

1. Перейти в **Settings** → **Secrets and variables** → **Actions**
2. Добавить secrets:
   - `PYPI_API_TOKEN` - токен для PyPI
   - `TEST_PYPI_API_TOKEN` - токен для Test PyPI (опционально)

### Создание workflow файла

Создать `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      test_pypi:
        description: 'Publish to Test PyPI only'
        required: false
        default: false
        type: boolean

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Check package
      run: twine check dist/*

    - name: Publish to Test PyPI
      if: github.event.inputs.test_pypi == 'true'
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.TEST_PYPI_API_TOKEN }}
      run: |
        twine upload --repository testpypi dist/*

    - name: Publish to PyPI
      if: github.event_name == 'release' && github.event.action == 'published'
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        twine upload dist/*
```

### Использование GitHub Actions

#### Вариант A: Через релизы (автоматически)
1. Создать новый релиз в GitHub
2. GitHub Actions автоматически соберет и опубликует пакет
3. Пакет появится на PyPI

#### Вариант B: Ручной запуск
1. Перейти в **Actions** → **Publish to PyPI**
2. Нажать **Run workflow**
3. Выбрать опции (например, только Test PyPI)
4. Запустить workflow

---

## 📋 Способ 3: Полуавтоматическая публикация

### Скрипт для упрощения процесса

Создать `scripts/publish.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 DocxMD Converter - Публикация пакета"
echo "======================================"

# Проверка, что мы в правильной директории
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Ошибка: pyproject.toml не найден. Запустите из корня проекта."
    exit 1
fi

# Получить текущую версию
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "📋 Текущая версия: $CURRENT_VERSION"

# Запросить тип обновления версии
echo "Выберите тип обновления версии:"
echo "1. patch ($CURRENT_VERSION -> например 2.0.2)"
echo "2. minor ($CURRENT_VERSION -> например 2.1.0)"
echo "3. major ($CURRENT_VERSION -> например 3.0.0)"
echo "4. Пропустить обновление версии"
read -p "Ваш выбор [1-4]: " VERSION_CHOICE

case $VERSION_CHOICE in
    1) bump2version patch ;;
    2) bump2version minor ;;
    3) bump2version major ;;
    4) echo "Пропускаем обновление версии" ;;
    *) echo "❌ Неверный выбор"; exit 1 ;;
esac

# Получить новую версию
NEW_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "📋 Новая версия: $NEW_VERSION"

# Очистка предыдущих сборок
echo "🧹 Очистка предыдущих сборок..."
rm -rf dist/ build/ *.egg-info/

# Сборка пакета
echo "📦 Сборка пакета..."
python -m build

# Проверка пакета
echo "🔍 Проверка пакета..."
twine check dist/*

# Выбор репозитория для публикации
echo "Выберите репозиторий для публикации:"
echo "1. Test PyPI (для тестирования)"
echo "2. PyPI (продакшн)"
echo "3. Оба (сначала Test, затем PyPI)"
read -p "Ваш выбор [1-3]: " REPO_CHOICE

case $REPO_CHOICE in
    1)
        echo "📤 Публикация в Test PyPI..."
        twine upload --repository testpypi dist/*
        echo "✅ Опубликовано в Test PyPI: https://test.pypi.org/project/docxmd-converter/"
        ;;
    2)
        echo "📤 Публикация в PyPI..."
        twine upload dist/*
        echo "✅ Опубликовано в PyPI: https://pypi.org/project/docxmd-converter/"
        ;;
    3)
        echo "📤 Публикация в Test PyPI..."
        twine upload --repository testpypi dist/*
        echo "✅ Опубликовано в Test PyPI"

        read -p "Продолжить публикацию в PyPI? [y/N]: " CONFIRM
        if [[ $CONFIRM =~ ^[Yy]$ ]]; then
            echo "📤 Публикация в PyPI..."
            twine upload dist/*
            echo "✅ Опубликовано в PyPI: https://pypi.org/project/docxmd-converter/"
        fi
        ;;
    *)
        echo "❌ Неверный выбор"
        exit 1
        ;;
esac

echo ""
echo "🎉 Публикация завершена!"
echo "📦 Версия: $NEW_VERSION"
echo "🔗 PyPI: https://pypi.org/project/docxmd-converter/"
```

Использование:
```bash
chmod +x scripts/publish.sh
./scripts/publish.sh
```

---

## 🔄 Способ 4: Интеграция с git workflow

### Настройка git hooks

Создать `.git/hooks/pre-push`:

```bash
#!/bin/bash

echo "🔍 Проверка перед push..."

# Проверить, что все тесты проходят
if ! python -m pytest; then
    echo "❌ Тесты не прошли. Push отменен."
    exit 1
fi

# Проверить, что пакет собирается
if ! python -m build; then
    echo "❌ Ошибка сборки пакета. Push отменен."
    exit 1
fi

echo "✅ Проверки прошли успешно"
```

### Автоматическая публикация по тегам

```bash
# Создание тега запускает публикацию
git tag v2.0.2
git push origin v2.0.2

# GitHub Actions автоматически опубликует пакет
```

---

## 📊 Мониторинг и проверки

### Проверка статуса публикации

```bash
# Проверить последнюю версию на PyPI
pip index versions docxmd-converter

# Проверить установку
pip install docxmd-converter --upgrade
docxmd --version

# Проверить зависимости
pip show docxmd-converter
```

### Статистика загрузок

- **PyPI Stats**: https://pypistats.org/packages/docxmd-converter
- **GitHub Insights**: Repository → Insights → Traffic

---

## ⚠️ Важные моменты и лучшие практики

### ✅ Рекомендации

1. **Всегда тестируйте сначала на Test PyPI**
2. **Используйте API токены вместо паролей**
3. **Обновляйте версию перед каждой публикацией**
4. **Проверяйте пакет с `twine check` перед публикацией**
5. **Документируйте изменения в CHANGELOG.md**
6. **Создавайте git теги для релизов**

### ❌ Чего избегать

1. **Не публикуйте одну версию дважды** (PyPI не позволит)
2. **Не включайте секретные данные в пакет**
3. **Не пропускайте тестирование на Test PyPI**
4. **Не публикуйте незавершенные функции в продакшн**

### 🔐 Безопасность

1. **Используйте API токены с ограниченными правами**
2. **Не коммитьте .pypirc в git**
3. **Регулярно обновляйте токены**
4. **Используйте 2FA для аккаунта PyPI**

---

## 🛠️ Отладка проблем

### Частые ошибки и решения

```bash
# Ошибка: "File already exists"
# Решение: Обновить версию в pyproject.toml

# Ошибка: "Invalid authentication credentials"
# Решение: Проверить API токен в ~/.pypirc

# Ошибка: "Package description invalid"
# Решение: Проверить README.md и long_description

# Ошибка: "Metadata validation failed"
# Решение: Исправить pyproject.toml
```

### Проверка конфигурации

```bash
# Проверить конфигурацию twine
twine check dist/* --verbose

# Проверить метаданные пакета
python setup.py check --metadata --strict

# Проверить структуру пакета
python -m build --check
```

---

## 📚 Полезные ссылки

- **PyPI**: https://pypi.org/project/docxmd-converter/
- **Test PyPI**: https://test.pypi.org/project/docxmd-converter/
- **Документация twine**: https://twine.readthedocs.io/
- **Python Packaging Guide**: https://packaging.python.org/
- **GitHub Actions**: https://docs.github.com/en/actions

---

**🎯 Следуя этому руководству, вы сможете надежно и безопасно публиковать DocxMD Converter на PyPI любым удобным способом!**
