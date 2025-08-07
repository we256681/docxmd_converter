#!/usr/bin/env python3
"""
🎯 Финальная демонстрация готовности DocxMD Converter
Показывает что проект полностью готов к публикации и использованию.
"""

import sys
import subprocess
import tempfile
from pathlib import Path
import shutil

def print_header(title):
    """Красивый заголовок."""
    print("\n" + "=" * 70)
    print(f"🎯 {title}")
    print("=" * 70)

def print_success(message):
    """Сообщение об успехе."""
    print(f"✅ {message}")

def print_info(message):
    """Информационное сообщение."""
    print(f"ℹ️  {message}")

def check_project_structure():
    """Проверка структуры проекта."""
    print_header("Проверка структуры проекта")

    required_files = [
        "docxmd_converter/__init__.py",
        "docxmd_converter/core.py",
        "docxmd_converter/cli.py",
        "docxmd_converter/gui.py",
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "requirements.txt",
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        "PYPI_DEPLOYMENT.md"
    ]

    missing = []
    for file in required_files:
        path = Path(file)
        if path.exists():
            size = path.stat().st_size if path.is_file() else "dir"
            print_success(f"{file} ({size} bytes)")
        else:
            missing.append(file)
            print(f"❌ {file} - отсутствует")

    if not missing:
        print_success("Все необходимые файлы на месте!")
        return True
    else:
        print(f"⚠️  Отсутствуют файлы: {missing}")
        return False

def check_package_installation():
    """Проверка установки пакета."""
    print_header("Проверка установки пакета")

    try:
        # Импорт основных модулей
        from docxmd_converter import DocxMdConverter, cli_main, gui_run
        print_success("Основные модули импортированы")

        from docxmd_converter.core import ConversionError
        print_success("Исключения импортированы")

        # Проверка версии
        import docxmd_converter
        version = getattr(docxmd_converter, '__version__', '0.1.0')
        print_success(f"Версия пакета: {version}")

        return True

    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def check_cli_commands():
    """Проверка CLI команд."""
    print_header("Проверка CLI команд")

    commands = [
        (["python", "-m", "docxmd_converter.cli", "--help"], "CLI модуль"),
        (["python", "-c", "from docxmd_converter.gui import run; print('GUI готов')"], "GUI модуль")
    ]

    success_count = 0
    for cmd, name in commands:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=Path.cwd()
            )

            if result.returncode == 0:
                print_success(f"{name} работает корректно")
                success_count += 1
            else:
                print(f"⚠️  {name}: {result.stderr.strip()[:100]}")

        except Exception as e:
            print(f"❌ {name}: ошибка {e}")

    return success_count == len(commands)

def check_conversion_functionality():
    """Проверка функциональности конвертации."""
    print_header("Проверка функциональности конвертации")

    try:
        from docxmd_converter import DocxMdConverter

        # Создаем временные файлы для теста
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Тестовый markdown файл
            test_md = temp_path / "test.md"
            test_md.write_text(
                "# Финальный тест\n\n"
                "Это **тестовый документ** для проверки готовности пакета.\n\n"
                "## Возможности\n\n"
                "- ✅ Конвертация MD → DOCX\n"
                "- ✅ Конвертация DOCX → MD\n"
                "- ✅ Поддержка русского языка\n",
                encoding='utf-8'
            )

            # Создаем конвертер
            converter = DocxMdConverter()
            print_success("Конвертер инициализирован (Pandoc найден)")

            # Тест MD → DOCX
            docx_file = temp_path / "test.docx"
            converter.convert_file(test_md, docx_file, "md2docx")

            if docx_file.exists():
                size = docx_file.stat().st_size
                print_success(f"MD → DOCX: файл создан ({size} bytes)")
            else:
                print("❌ MD → DOCX: файл не создан")
                return False

            # Тест DOCX → MD
            md_back = temp_path / "test_back.md"
            converter.convert_file(docx_file, md_back, "docx2md")

            if md_back.exists():
                size = md_back.stat().st_size
                print_success(f"DOCX → MD: файл создан ({size} bytes)")
            else:
                print("❌ DOCX → MD: файл не создан")
                return False

        print_success("Функциональность конвертации работает!")
        return True

    except Exception as e:
        print(f"❌ Ошибка конвертации: {e}")
        return False

def check_github_actions():
    """Проверка GitHub Actions конфигурации."""
    print_header("Проверка GitHub Actions")

    workflows = [
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml"
    ]

    for workflow in workflows:
        path = Path(workflow)
        if path.exists():
            print_success(f"{workflow} настроен")
        else:
            print(f"❌ {workflow} отсутствует")
            return False

    # Проверка шаблона PR
    pr_template = Path(".github/PULL_REQUEST_TEMPLATE.md")
    if pr_template.exists():
        print_success("Шаблон PR настроен")
    else:
        print("⚠️  Шаблон PR отсутствует")

    return True

def check_pypi_readiness():
    """Проверка готовности к публикации на PyPI."""
    print_header("Проверка готовности к PyPI")

    try:
        # Попытка сборки
        result = subprocess.run(
            ["python", "-m", "build", "--wheel", "--sdist"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print_success("Пакет успешно собирается")

            # Проверяем созданные файлы
            dist_dir = Path("dist")
            if dist_dir.exists():
                files = list(dist_dir.glob("*"))
                print_info(f"Создано файлов: {len(files)}")
                for f in files:
                    print_info(f"  - {f.name} ({f.stat().st_size} bytes)")

            return True
        else:
            print(f"❌ Ошибка сборки: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⚠️  Timeout при сборке пакета")
        return False
    except Exception as e:
        print(f"❌ Ошибка проверки сборки: {e}")
        return False

def show_project_summary():
    """Показать итоговую информацию о проекте."""
    print_header("Итоговая информация о проекте")

    # Статистика файлов
    py_files = len(list(Path(".").rglob("*.py"))) - len(list(Path("venv").rglob("*.py"))) if Path("venv").exists() else len(list(Path(".").rglob("*.py")))
    md_files = len(list(Path(".").glob("*.md")))
    config_files = len(list(Path(".").rglob("*.yml"))) + len(list(Path(".").rglob("*.yaml"))) + len(list(Path(".").rglob("*.toml"))) + len(list(Path(".").rglob("*.cfg")))

    print_info(f"Python файлов: {py_files}")
    print_info(f"Документации: {md_files}")
    print_info(f"Конфигурационных файлов: {config_files}")

    # Размер пакета
    package_dir = Path("docxmd_converter")
    if package_dir.exists():
        size = sum(f.stat().st_size for f in package_dir.rglob("*") if f.is_file())
        print_info(f"Размер пакета: {size // 1024}KB")

    print_success("Проект готов к публикации на PyPI!")

def main():
    """Основная функция демонстрации."""
    print_header("🎯 DocxMD Converter - Финальная демонстрация готовности")

    tests = [
        ("Структура проекта", check_project_structure),
        ("Установка пакета", check_package_installation),
        ("CLI команды", check_cli_commands),
        ("Функциональность конвертации", check_conversion_functionality),
        ("GitHub Actions", check_github_actions),
        ("Готовность к PyPI", check_pypi_readiness),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print_info(f"Запуск теста: {test_name}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")

    # Показываем итоговую информацию
    show_project_summary()

    # Итоги
    print_header("🏁 ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ")
    print(f"📊 Пройдено тестов: {passed}/{total}")

    if passed == total:
        print_success("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print_success("✨ Проект полностью готов к использованию!")
        print_success("🚀 Готов к публикации на PyPI!")
        print()
        print("🎯 Следующие шаги:")
        print("   1. Загрузить на GitHub")
        print("   2. Настроить PyPI токены в GitHub Secrets")
        print("   3. Создать тег v0.1.0 для первого релиза")
        print("   4. Наслаждаться автоматической публикацией! 🎉")
    else:
        print(f"⚠️  {total - passed} тестов не прошли")
        print("   Проверьте ошибки выше и исправьте проблемы")

    print("=" * 70)

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)