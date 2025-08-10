#!/usr/bin/env python3
"""
Скрипт для публикации пакета на PyPI
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


def final_checks():
    """Финальные проверки перед публикацией"""
    print("🔍 Финальные проверки...")

    checks = [
        "✅ Код протестирован",
        "✅ Документация обновлена",
        "✅ Версия увеличена",
        "✅ CHANGELOG.md обновлен",
        "✅ Тестовая публикация прошла успешно",
        "✅ Все изменения закоммичены в git"
    ]

    print("\n📋 Чек-лист перед публикацией:")
    for check in checks:
        print(f"   {check}")

    print("\n⚠️  ВНИМАНИЕ: Это публикация на РЕАЛЬНЫЙ PyPI!")
    print("   После публикации версию нельзя будет изменить или удалить.")

    response = input("\n❓ Все проверки пройдены? Продолжить? (yes/N): ").strip()

    return response.lower() == 'yes'


def publish_to_pypi():
    """Публикация на PyPI"""
    print("🚀 Публикация на PyPI...")

    # Команда для публикации на PyPI
    cmd = "python -m twine upload dist/*"

    print("📋 Команда для выполнения:")
    print(f"   {cmd}")
    print("\n⚠️  Вам потребуется:")
    print("   - Аккаунт на https://pypi.org/")
    print("   - API токен или логин/пароль")
    print("\n🔑 Настройка токена:")
    print("   1. Зайдите на https://pypi.org/manage/account/")
    print("   2. Создайте API токен")
    print("   3. Используйте __token__ как username и токен как password")

    # Финальное подтверждение
    response = input("\n❓ ФИНАЛЬНОЕ ПОДТВЕРЖДЕНИЕ: Опубликовать на PyPI? (YES/N): ").strip()

    if response != 'YES':
        print("❌ Публикация отменена")
        return False

    # Выполнить публикацию
    result = subprocess.run(cmd, shell=True)

    if result.returncode == 0:
        print("✅ Публикация на PyPI успешна!")
        print("\n🎉 Поздравляем! Пакет опубликован!")
        print("\n📋 Проверьте пакет:")
        print("   https://pypi.org/project/docxmd-converter/")
        print("\n📦 Установка:")
        print("   pip install docxmd-converter")
        print("\n📊 Следующие шаги:")
        print("   1. Обновите README с новой версией")
        print("   2. Создайте git tag для версии")
        print("   3. Опубликуйте release на GitHub")
        return True
    else:
        print("❌ Ошибка публикации")
        return False


def main():
    """Главная функция"""
    print("🚀 Публикация пакета DocxMD Converter на PyPI")
    print("=" * 60)

    # Переход в корневую директорию
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    os.chdir(root_dir)

    print(f"📁 Рабочая директория: {os.getcwd()}")

    # Проверка файлов
    if not check_dist_files():
        sys.exit(1)

    # Финальные проверки
    if not final_checks():
        print("❌ Публикация отменена")
        sys.exit(1)

    # Публикация
    if not publish_to_pypi():
        sys.exit(1)

    print("=" * 60)
    print("🎉 Публикация на PyPI завершена успешно!")


if __name__ == "__main__":
    main()