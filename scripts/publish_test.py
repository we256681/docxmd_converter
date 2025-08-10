#!/usr/bin/env python3
"""
Скрипт для публикации пакета на TestPyPI
"""

import os
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


def check_dist_files():
    """Проверить наличие файлов для публикации"""
    dist_dir = Path('dist')

    if not dist_dir.exists():
        print("❌ Директория dist/ не найдена. Запустите сначала build_package.py")
        return False

    dist_files = list(dist_dir.glob('*'))
    if not dist_files:
        print("❌ Файлы для публикации не найдены в dist/")
        return False

    print("📦 Файлы для публикации:")
    for file_path in dist_files:
        print(f"   - {file_path}")

    return True


def publish_to_testpypi():
    """Публикация на TestPyPI"""
    print("🚀 Публикация на TestPyPI...")

    # Команда для публикации на TestPyPI
    cmd = "python -m twine upload --repository testpypi dist/*"

    print("📋 Команда для выполнения:")
    print(f"   {cmd}")
    print("\n⚠️  Вам потребуется:")
    print("   - Аккаунт на https://test.pypi.org/")
    print("   - API токен или логин/пароль")
    print("\n🔑 Настройка токена:")
    print("   1. Зайдите на https://test.pypi.org/manage/account/")
    print("   2. Создайте API токен")
    print("   3. Используйте __token__ как username и токен как password")

    # Спросить подтверждение
    response = input("\n❓ Продолжить публикацию? (y/N): ").strip().lower()

    if response != 'y':
        print("❌ Публикация отменена")
        return False

    # Выполнить публикацию
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print("✅ Публикация на TestPyPI успешна!")
        print("\n📋 Проверьте пакет:")
        print("   https://test.pypi.org/project/docxmd-converter/")
        print("\n🧪 Тестовая установка:")
        print("   pip install -i https://test.pypi.org/simple/ docxmd-converter")
        return True
    else:
        print("❌ Ошибка публикации")
        return False


def main():
    """Главная функция"""
    print("🧪 Публикация пакета DocxMD Converter на TestPyPI")
    print("=" * 60)

    # Переход в корневую директорию
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    os.chdir(root_dir)

    print(f"📁 Рабочая директория: {os.getcwd()}")

    # Проверка файлов
    if not check_dist_files():
        sys.exit(1)

    # Публикация
    if not publish_to_testpypi():
        sys.exit(1)

    print("=" * 60)
    print("🎉 Тестовая публикация завершена!")


if __name__ == "__main__":
    main()