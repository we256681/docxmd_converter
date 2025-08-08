#!/usr/bin/env python3
"""
Test script for post-processing functionality
"""

import tempfile
import os
from pathlib import Path

# Create test markdown files
test_content = """
# Должностная инструкция: Тестовая должность

## 1. Общие положения

1.1. Тестовая должность относится к категории специалистов.

1.2. На должность принимается лицо, имеющее высшее профессиональное образование.

1.3. Агент должен знать:
- основы трудового законодательства;
- правила внутреннего трудового распорядка;
- инструкции по охране труда.

## 2. Функции

2.1. Выполнение основных функций.
2.2. Контроль качества работы.

## 3. Должностные обязанности

3.1. Исполняет следующие обязанности по работе.
3.2. Ведет документооборот.

## 4. Права

4.1. Имеет право на информацию.
4.2. Вносит предложения по улучшению работы.

## 5. Ответственность

Сотрудник привлекается к ответственности:
- за нарушение трудовой дисциплины;
- за некачественное выполнение обязанностей.
"""

def main():
    # Create temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Created temporary test directory: {temp_dir}")

        # Create test markdown files
        test_files = [
            "Агент по розыску.md",
            "Специалист отдела.md",
            "Менеджер проекта.md"
        ]

        for filename in test_files:
            filepath = Path(temp_dir) / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(test_content)
            print(f"✅ Created: {filename}")

        print("\n" + "="*60)
        print("🧪 TESTING CLI FUNCTIONALITY")
        print("="*60)

        # Test basic processing (no conversion, only post-processing)
        print("\n📋 Testing basic post-processing...")
        os.system(f'python -m docxmd_converter.cli --src "{temp_dir}" --dst "{temp_dir}" --format docx2md --post-process --processor basic --report console')

        print("\n📋 Testing advanced post-processing with file report...")
        os.system(f'python -m docxmd_converter.cli --src "{temp_dir}" --dst "{temp_dir}" --format docx2md --post-process --processor advanced --report file --force-process')

        # Check if files were processed
        print("\n📂 Checking processed files...")
        for filename in test_files:
            filepath = Path(temp_dir) / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "<!-- METADATA" in content:
                        print(f"✅ {filename} was processed (contains metadata)")
                    else:
                        print(f"⚠️ {filename} was not processed (no metadata)")

        # Check if report was generated
        report_files = list(Path(temp_dir).glob("processing_report*.md"))
        if report_files:
            print(f"📄 Generated report: {report_files[0].name}")
        else:
            print("⚠️ No report file found")

        print(f"\n🔗 Test files location: {temp_dir}")
        print("You can manually inspect the files before the temp directory is cleaned up")
        input("Press Enter to continue and cleanup...")

if __name__ == "__main__":
    main()