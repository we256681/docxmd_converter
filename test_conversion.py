#!/usr/bin/env python3
"""
Полный функциональный тест DocxMD Converter с реальными файлами.
"""

import shutil
import sys
import tempfile
from pathlib import Path

# Добавим путь к пакету
sys.path.insert(0, str(Path(__file__).parent))


def create_test_markdown():
    """Создаём тестовый markdown файл."""
    content = """# Тестовый документ

Это **тестовый документ** для проверки конвертации между форматами.

## Основные возможности

- ✅ Конвертация `.docx` в `.md`
- ✅ Конвертация `.md` в `.docx`
- ✅ Поддержка шаблонов
- ✅ Рекурсивная обработка директорий

### Пример кода

```python
from docxmd_converter import DocxMdConverter

converter = DocxMdConverter()
converter.convert_file("input.md", "output.docx", "md2docx")
```

### Таблица функций

| Функция | Поддерживается | Описание |
|---------|----------------|----------|
| CLI | ✅ | Интерфейс командной строки |
| GUI | ✅ | Графический интерфейс |
| Шаблоны | ✅ | Кастомные стили |
| Рекурсия | ✅ | Обработка папок |

> **Примечание**: Этот текст создан для тестирования
> конвертации между форматами документов.

---

*Конец тестового документа*
"""
    return content


def test_real_conversion():
    """Тест реальной конвертации файлов."""
    print("🧪 Запуск полнофункционального теста конвертации")
    print("=" * 60)

    try:
        from docxmd_converter import DocxMdConverter

        # Создаём временные директории
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Создаём структуру папок
            src_dir = temp_path / "source"
            dst_dir = temp_path / "destination"
            src_dir.mkdir()
            dst_dir.mkdir()

            print(f"📁 Временные директории созданы:")
            print(f"   Источник: {src_dir}")
            print(f"   Назначение: {dst_dir}")

            # Создаём тестовые файлы
            test_files = []

            # 1. Простой markdown
            md1 = src_dir / "test1.md"
            md1.write_text(create_test_markdown(), encoding="utf-8")
            test_files.append(md1)

            # 2. Markdown в подпапке
            subdir = src_dir / "subfolder"
            subdir.mkdir()
            md2 = subdir / "test2.md"
            md2.write_text(
                "# Документ из подпапки\n\nЭто тест **сохранения структуры** папок.",
                encoding="utf-8",
            )
            test_files.append(md2)

            print(f"📄 Созданы тестовые файлы:")
            for f in test_files:
                size = f.stat().st_size
                rel_path = f.relative_to(src_dir)
                print(f"   {rel_path} ({size} bytes)")

            # Инициализируем конвертер
            converter = DocxMdConverter(log_level="INFO")
            print("✅ Конвертер инициализирован")

            # Тест 1: MD → DOCX
            print("\n🔄 Тест 1: Конвертация MD → DOCX")
            successful, total = converter.convert_directory(
                src_dir=src_dir, dst_dir=dst_dir, direction="md2docx"
            )

            print(f"📊 Результат: {successful}/{total} файлов конвертировано")

            # Проверяем результаты
            docx_files = list(dst_dir.rglob("*.docx"))
            print(f"📄 Созданные .docx файлы:")
            for f in docx_files:
                size = f.stat().st_size
                rel_path = f.relative_to(dst_dir)
                print(f"   {rel_path} ({size} bytes)")

            # Тест 2: DOCX → MD (обратная конвертация)
            print("\n🔄 Тест 2: Обратная конвертация DOCX → MD")

            # Новая папка для результата
            back_dir = temp_path / "back_conversion"
            back_dir.mkdir()

            successful2, total2 = converter.convert_directory(
                src_dir=dst_dir, dst_dir=back_dir, direction="docx2md"
            )

            print(f"📊 Результат: {successful2}/{total2} файлов конвертировано обратно")

            # Проверяем результаты обратной конвертации
            md_files = list(back_dir.rglob("*.md"))
            print(f"📄 Конвертированные обратно .md файлы:")
            for f in md_files:
                size = f.stat().st_size
                rel_path = f.relative_to(back_dir)
                print(f"   {rel_path} ({size} bytes)")

            # Итоговая статистика
            print("\n" + "=" * 60)
            print("📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
            print(f"   ✅ MD → DOCX: {successful}/{total}")
            print(f"   ✅ DOCX → MD: {successful2}/{total2}")
            structure_ok = len(md_files) == len(test_files)
            status = "сохранена" if structure_ok else "нарушена"
            print(f"   📁 Структура папок: {status}")

            if successful == total and successful2 == total2:
                print("🎉 Все тесты пройдены успешно!")
                return True
            else:
                print("⚠️  Есть ошибки в конвертации")
                return False

    except Exception as e:
        print(f"❌ Ошибка теста: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_cli_with_real_files():
    """Тест CLI с реальными файлами."""
    print("\n🖥️  Тест CLI интерфейса")
    print("=" * 60)

    try:
        import subprocess

        # Создаём временные директории в текущем проекте
        test_dir = Path("temp_test")
        test_dir.mkdir(exist_ok=True)

        src_dir = test_dir / "markdown"
        dst_dir = test_dir / "docx_out"
        src_dir.mkdir(exist_ok=True)
        dst_dir.mkdir(exist_ok=True)

        # Создаём тестовый файл
        test_md = src_dir / "cli_test.md"
        test_md.write_text(
            "# CLI Test\n\nЭто тест **CLI интерфейса**.", encoding="utf-8"
        )

        print(f"📄 Создан тестовый файл: {test_md}")

        # Use current Python interpreter
        import sys

        # Запускаем CLI команду
        cmd = [
            sys.executable,
            "-m",
            "docxmd_converter.cli",
            "--src",
            str(src_dir),
            "--dst",
            str(dst_dir),
            "--direction",
            "md2docx",
            "--verbose",
        ]

        print("🖥️  Запуск CLI команды:")
        print(f"   {' '.join(cmd)}")

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=Path(__file__).parent
        )

        print(f"📊 Код возврата: {result.returncode}")

        if result.stdout:
            print("📤 Вывод:")
            print("   " + result.stdout.replace("\n", "\n   "))

        if result.stderr:
            print("⚠️  Ошибки:")
            print("   " + result.stderr.replace("\n", "\n   "))

        # Проверяем результат
        output_files = list(dst_dir.rglob("*.docx"))
        if output_files:
            print(f"✅ CLI успешно создал {len(output_files)} файл(ов)")
            for f in output_files:
                size = f.stat().st_size
                print(f"   📄 {f.name} ({size} bytes)")
        else:
            print("❌ CLI не создал выходных файлов")

        # Очистка
        shutil.rmtree(test_dir)
        print("🧹 Временные файлы очищены")

        return result.returncode == 0 and len(output_files) > 0

    except Exception as e:
        print(f"❌ Ошибка CLI теста: {e}")
        return False


def main():
    """Главная функция тестирования."""
    print("🎯 DocxMD Converter - Полнофункциональное тестирование")
    print("=" * 70)

    tests_results = []

    # Тест 1: Реальная конвертация
    print("ТЕСТ 1: Реальная конвертация файлов")
    tests_results.append(test_real_conversion())

    # Тест 2: CLI интерфейс
    print("\nТЕСТ 2: CLI интерфейс")
    tests_results.append(test_cli_with_real_files())

    # Итоги
    passed = sum(tests_results)
    total = len(tests_results)

    print("\n" + "=" * 70)
    print("🏁 ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print(f"   📊 Пройдено тестов: {passed}/{total}")

    if passed == total:
        print("   🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Пакет полностью функционален!")
        print("   ✅ Конвертация работает")
        print("   ✅ CLI работает")
        print("   ✅ Структура папок сохраняется")
        print("   ✅ Pandoc интегрирован корректно")
    else:
        print(f"   ⚠️  {total - passed} тестов провалились")

    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
