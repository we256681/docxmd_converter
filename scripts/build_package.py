#!/usr/bin/env python3
"""
Скрипт для сборки пакета для PyPI
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Выполнить команду с описанием"""
    print(f"🔧 {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Ошибка: {result.stderr}")
        return False
    else:
        print(f"✅ {description} завершено")
        if result.stdout.strip():
            print(f"   {result.stdout.strip()}")
        return True


def clean_build_dirs():
    """Очистить директории сборки"""
    dirs_to_clean = ['build', 'dist', 'src/docxmd_converter.egg-info']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️  Удалена директория: {dir_name}")


def check_requirements():
    """Проверить наличие необходимых инструментов"""
    required_packages = ['build', 'twine']

    for package in required_packages:
        if not run_command(f"python -c 'import {package}'", f"Проверка {package}"):
            print(f"📦 Установка {package}...")
            if not run_command(f"pip install {package}", f"Установка {package}"):
                return False

    return True


def validate_package_structure():
    """Проверить структуру пакета"""
    required_files = [
        'pyproject.toml',
        'setup.py',
        'README.md',
        'LICENSE',
        'src/docxmd_converter/__init__.py'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print("❌ Отсутствуют обязательные файлы:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False

    print("✅ Структура пакета корректна")
    return True


def build_package():
    """Собрать пакет"""
    print("🏗️  Сборка пакета...")

    # Очистка
    clean_build_dirs()

    # Проверка требований
    if not check_requirements():
        return False

    # Проверка структуры
    if not validate_package_structure():
        return False

    # Сборка
    if not run_command("python -m build", "Сборка пакета"):
        return False

    # Проверка результата
    dist_files = list(Path('dist').glob('*'))
    if not dist_files:
        print("❌ Файлы сборки не найдены")
        return False

    print("📦 Созданные файлы:")
    for file_path in dist_files:
        print(f"   - {file_path}")

    return True


def check_package():
    """Проверить собранный пакет"""
    print("🔍 Проверка пакета...")

    # Проверка с помощью twine
    if not run_command("python -m twine check dist/*", "Проверка пакета twine"):
        return False

    return True


def main():
    """Главная функция"""
    print("🚀 Сборка пакета DocxMD Converter для PyPI")
    print("=" * 50)

    # Переход в корневую директорию
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    os.chdir(root_dir)

    print(f"📁 Рабочая директория: {os.getcwd()}")

    # Сборка
    if not build_package():
        print("❌ Сборка не удалась")
        sys.exit(1)

    # Проверка
    if not check_package():
        print("❌ Проверка не удалась")
        sys.exit(1)

    print("=" * 50)
    print("🎉 Пакет успешно собран и проверен!")
    print("\n📋 Следующие шаги:")
    print("1. Проверьте файлы в директории dist/")
    print("2. Для тестовой публикации: python scripts/publish_test.py")
    print("3. Для публикации на PyPI: python scripts/publish_pypi.py")


if __name__ == "__main__":
    main()