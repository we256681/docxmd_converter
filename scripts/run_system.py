#!/usr/bin/env python3
"""
Универсальный запускатор системы DocxMD Converter
Позволяет выбрать и запустить любой интерфейс системы
"""

import sys
import subprocess
from pathlib import Path

# Добавляем путь к src для импортов
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def print_banner():
    """Печать баннера системы"""
    print("🚀 DocxMD Converter v3.0.0")
    print("=" * 50)
    print("Универсальная система обработки документов")
    print("с интеллектуальным анализом и NLP")
    print("=" * 50)


def print_menu():
    """Печать меню выбора"""
    print("\n📋 Выберите интерфейс для запуска:")
    print("1. 🧠 Интеллектуальный процессор (intelligent_processor.py)")
    print("2. 🎭 Демонстрация всех возможностей (demo_all_features.py)")
    print("3. 🌐 Веб-интерфейс (web_interface.py)")
    print("4. 🖥️  GUI интерфейс (gui.py)")
    print("5. ⚙️  CLI помощь (cli.py --help)")
    print("6. 🧪 Тестирование системы")
    print("7. 📊 Статистика обработки")
    print("0. ❌ Выход")


def run_intelligent_processor():
    """Запуск интеллектуального процессора"""
    print("\n🧠 Запуск интеллектуального процессора...")
    script_path = Path(__file__).parent.parent / "src" / "docxmd_converter" / "intelligent_processor.py"
    subprocess.run([sys.executable, str(script_path)])


def run_demo():
    """Запуск демонстрации"""
    print("\n🎭 Запуск демонстрации всех возможностей...")
    script_path = Path(__file__).parent / "demo_all_features.py"
    subprocess.run([sys.executable, str(script_path)])


def run_web_interface():
    """Запуск веб-интерфейса"""
    print("\n🌐 Запуск веб-интерфейса...")
    print("📍 Будет доступен по адресу: http://localhost:5000")
    print("⚠️  Убедитесь, что Flask установлен: pip install flask")

    try:
        script_path = Path(__file__).parent.parent / "src" / "docxmd_converter" / "web_interface.py"
        subprocess.run([sys.executable, str(script_path)])
    except KeyboardInterrupt:
        print("\n🛑 Веб-сервер остановлен")


def run_gui():
    """Запуск GUI интерфейса"""
    print("\n🖥️  Запуск GUI интерфейса...")
    try:
        from docxmd_converter.gui import run
        run()
    except ImportError as e:
        print(f"❌ Ошибка импорта GUI: {e}")
        script_path = Path(__file__).parent.parent / "src" / "docxmd_converter" / "gui.py"
        subprocess.run([sys.executable, str(script_path)])


def show_cli_help():
    """Показать помощь CLI"""
    print("\n⚙️  CLI интерфейс - справка:")
    subprocess.run([sys.executable, "-m", "docxmd_converter.cli", "--help"])


def run_tests():
    """Запуск тестов системы"""
    print("\n🧪 Запуск тестирования системы...")

    # Проверяем основные компоненты
    base_path = Path(__file__).parent.parent
    components = [
        (base_path / "src" / "docxmd_converter" / "intelligent_processor.py", "Интеллектуальный процессор"),
        (base_path / "config" / "document_templates.json", "Конфигурация шаблонов"),
        (base_path / "src" / "docxmd_converter" / "core.py", "Основной модуль"),
        (base_path / "src" / "docxmd_converter" / "gui.py", "GUI интерфейс"),
        (base_path / "src" / "docxmd_converter" / "web_interface.py", "Веб-интерфейс")
    ]

    print("📋 Проверка компонентов:")
    for filepath, description in components:
        if filepath.exists():
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description} - файл не найден")

    # Тест импортов
    print("\n🔍 Проверка импортов:")
    try:
        from docxmd_converter.intelligent_processor import IntelligentProcessor
        print("   ✅ IntelligentProcessor")
    except ImportError as e:
        print(f"   ❌ IntelligentProcessor: {e}")

    try:
        from docxmd_converter.core import DocxMdConverter
        print("   ✅ DocxMdConverter")
    except ImportError as e:
        print(f"   ❌ DocxMdConverter: {e}")

    # Тест обработки
    print("\n⚡ Быстрый тест обработки:")
    try:
        from docxmd_converter.intelligent_processor import IntelligentProcessor
        processor = IntelligentProcessor()
        stats = processor.get_processing_statistics()

        if stats.get('total_files_processed', 0) > 0:
            print(f"   ✅ Обработано файлов: {stats['total_files_processed']}")
            print(f"   📊 Средняя оценка: {stats['average_quality_score']:.1f}/100")
        else:
            print("   ℹ️  История обработки пуста")

    except Exception as e:
        print(f"   ❌ Ошибка тестирования: {e}")


def show_statistics():
    """Показать статистику обработки"""
    print("\n📊 Статистика системы:")

    try:
        from docxmd_converter.intelligent_processor import IntelligentProcessor
        processor = IntelligentProcessor()
        stats = processor.get_processing_statistics()

        if stats.get('total_files_processed', 0) > 0:
            print(f"📁 Всего обработано файлов: {stats['total_files_processed']}")
            print(f"⏱️  Среднее время обработки: {stats['average_processing_time']:.3f}с")
            print(f"📊 Средняя оценка качества: {stats['average_quality_score']:.1f}/100")
            print(f"📅 Последняя обработка: {stats.get('last_processed', 'Нет данных')}")

            print(f"\n📋 Распределение по типам документов:")
            for doc_type, count in stats['document_types_distribution'].items():
                print(f"   {doc_type}: {count}")
        else:
            print("ℹ️  История обработки пуста")
            print("💡 Запустите обработку документов для получения статистики")

    except Exception as e:
        print(f"❌ Ошибка получения статистики: {e}")


def main():
    """Основная функция"""
    print_banner()

    while True:
        print_menu()

        try:
            choice = input("\n👉 Введите номер (0-7): ").strip()

            if choice == "0":
                print("\n👋 До свидания!")
                break
            elif choice == "1":
                run_intelligent_processor()
            elif choice == "2":
                run_demo()
            elif choice == "3":
                run_web_interface()
            elif choice == "4":
                run_gui()
            elif choice == "5":
                show_cli_help()
            elif choice == "6":
                run_tests()
            elif choice == "7":
                show_statistics()
            else:
                print("❌ Неверный выбор. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем")
            break
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")

        input("\n📱 Нажмите Enter для продолжения...")


if __name__ == "__main__":
    main()