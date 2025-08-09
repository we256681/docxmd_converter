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
