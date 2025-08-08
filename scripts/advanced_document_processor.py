#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Продвинутый обработчик должностных инструкций v2.0
Расширенная версия с дополнительными возможностями
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AdvancedDocumentProcessor:
    def __init__(self, force_reprocess=False, dry_run=False):
        self.processed_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.force_reprocess = force_reprocess
        self.dry_run = dry_run

    def clean_consultant_plus_artifacts(self, content: str) -> str:
        """Расширенная очистка от артефактов КонсультантПлюс"""
        # Удаляем блоки с разделителями
        content = re.sub(r'-{15,}.*?-{15,}', '', content, flags=re.DOTALL)
        content = re.sub(r'_{15,}', '', content)
        content = re.sub(r'─{15,}', '', content)

        # Удаляем изображения и ссылки на медиафайлы
        content = re.sub(r'!\[.*?\]\(.*?media.*?\).*?\n', '', content)
        content = re.sub(r'!\[.*?\]\(.*?\){[^}]*}', '', content)

        # Удаляем информацию КонсультантПлюс
        content = re.sub(r'Форма:.*?\n', '', content)
        content = re.sub(r'\(Подготовлен для системы КонсультантПлюс.*?\)', '', content)
        content = re.sub(r'Документ предоставлен.*?www\.consultant\.ru.*?\n', '', content, flags=re.DOTALL)
        content = re.sub(r'Дата сохранения:.*?\n', '', content)
        content = re.sub(r'\*\*Актуально на.*?\*\*', '', content)

        # Удаляем таблицы
        content = re.sub(r'\+[-+]+\+.*?\n', '', content)
        content = re.sub(r'\|.*?\|.*?\n', '', content)

        # Удаляем ссылки
        content = re.sub(r'См\.:.*?Путеводитель.*?\n', '', content, flags=re.DOTALL)

        # Удаляем служебные блоки
        content = re.sub(r'-- -- -+ --.*?-- -- -+ --', '', content, flags=re.DOTALL)

        return content

    def advanced_structure_content(self, content: str, filename: str) -> str:
        """Улучшенное структурирование содержимого"""
        position_name = self.extract_position_from_filename(filename)

        # Начинаем с шаблона
        result = f"# Должностная инструкция: {position_name}\n\n"
        result += "## Информация о документе\n\n"
        result += "**Организация:** _(наименование организации)_\n\n"
        result += "**Утверждено:** _(подпись, инициалы, фамилия руководителя)_\n\n"
        result += "**Дата утверждения:** _(дата)_\n\n"

        # Извлекаем основные разделы
        sections = self.improved_extract_sections(content)

        # Строим структуру
        if sections['general']:
            result += self.format_general_section_advanced(sections['general'])
        else:
            result += self.create_default_general_section(position_name)

        if sections['functions']:
            result += "## 2. Функции\n\n" + self.format_functions_advanced(sections['functions'])
        else:
            result += "## 2. Функции\n\n_(Функции должности указываются отдельно)_\n\n"

        if sections['duties']:
            result += "## 3. Должностные обязанности\n\n" + self.format_duties_advanced(sections['duties'])
        else:
            result += "## 3. Должностные обязанности\n\n_(Обязанности указываются отдельно)_\n\n"

        if sections['rights']:
            result += "## 4. Права\n\n" + self.format_rights_advanced(sections['rights'])
        else:
            result += "## 4. Права\n\n_(Права указываются отдельно)_\n\n"

        if sections['responsibility']:
            result += "## 5. Ответственность\n\n" + self.format_responsibility_advanced(sections['responsibility'])
        else:
            result += "## 5. Ответственность\n\n_(Виды ответственности указываются отдельно)_\n\n"

        # Подписи
        result += self.get_signatures_section()

        return result

    def improved_extract_sections(self, content: str) -> Dict[str, str]:
        """Улучшенное извлечение разделов"""
        sections = {
            'general': '',
            'functions': '',
            'duties': '',
            'rights': '',
            'responsibility': ''
        }

        # Очищаем контент от служебной информации
        content = self.clean_consultant_plus_artifacts(content)

        # Общие положения - расширенный поиск
        general_patterns = [
            r'1\.\s*Общие положения(.*?)(?=\d+\.|$)',
            r'\*\*1\.\s*Общие положения\*\*(.*?)(?=\*\*\d+\.|$)',
            r'Общие положения(.*?)(?=Функции|Обязанности|$)'
        ]

        for pattern in general_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match and match.group(1).strip():
                sections['general'] = match.group(1).strip()
                break

        # Функции
        functions_patterns = [
            r'2\.\s*Функции(.*?)(?=\d+\.|$)',
            r'\*\*2\.\s*Функции\*\*(.*?)(?=\*\*\d+\.|$)'
        ]

        for pattern in functions_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match and match.group(1).strip():
                sections['functions'] = match.group(1).strip()
                break

        # Должностные обязанности
        duties_patterns = [
            r'3\.\s*Должностные обязанности(.*?)(?=\d+\.|$)',
            r'\*\*3\.\s*Должностные обязанности\*\*(.*?)(?=\*\*\d+\.|$)',
            r'обязанности.*?исполняет следующие обязанности:(.*?)(?=\d+\.|$)'
        ]

        for pattern in duties_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match and match.group(1).strip():
                sections['duties'] = match.group(1).strip()
                break

        # Права
        rights_patterns = [
            r'4\.\s*Права(.*?)(?=\d+\.|$)',
            r'\*\*4\.\s*Права\*\*(.*?)(?=\*\*\d+\.|$)',
            r'имеет право:(.*?)(?=\d+\.|$)'
        ]

        for pattern in rights_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match and match.group(1).strip():
                sections['rights'] = match.group(1).strip()
                break

        # Ответственность
        resp_patterns = [
            r'5\.\s*Ответственность(.*?)(?=\d+\.|─|С должностной инструкцией|$)',
            r'\*\*5\.\s*Ответственность\*\*(.*?)(?=\*\*\d+\.|─|С должностной инструкцией|$)',
            r'привлекается к ответственности:(.*?)(?=\d+\.|─|С должностной инструкцией|$)'
        ]

        for pattern in resp_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match and match.group(1).strip():
                sections['responsibility'] = match.group(1).strip()
                break

        return sections

    def format_general_section_advanced(self, content: str) -> str:
        """Продвинутое форматирование общих положений"""
        result = "## 1. Общие положения\n\n"

        # Попытка извлечь подразделы
        subsections = re.split(r'(\d+\.\d+\.)', content)

        current_subsection = ""
        subsection_map = {
            '1.1.': ('### 1.1. Категория должности\n\n', self.format_category),
            '1.2.': ('### 1.2. Требования к образованию и опыту\n\n', self.format_requirements),
            '1.3.': ('### 1.3. Знания и навыки\n\n', self.format_knowledge),
            '1.4.': ('### 1.4. Руководящие документы\n\n', self.format_documents),
            '1.5.': ('### 1.5. Подчиненность\n\n', self.format_subordination),
            '1.6.': ('### 1.6. Замещение\n\n', self.format_replacement)
        }

        for i, part in enumerate(subsections):
            if re.match(r'\d+\.\d+\.', part):
                current_subsection = part
            elif current_subsection and part.strip():
                if current_subsection in subsection_map:
                    header, formatter = subsection_map[current_subsection]
                    result += header + formatter(part) + "\n\n"

        return result

    def format_category(self, text: str) -> str:
        """Форматирование категории должности"""
        text = self.clean_text(text)
        if 'относится к категории' in text.lower():
            return text
        else:
            return f"_(Информация о категории должности)_"

    def format_requirements(self, text: str) -> str:
        """Форматирование требований"""
        text = self.clean_text(text)
        if any(word in text.lower() for word in ['образование', 'принимается лицо', 'требования']):
            return text
        else:
            return f"_(Требования к образованию и опыту работы)_"

    def format_knowledge(self, text: str) -> str:
        """Форматирование знаний и навыков"""
        text = self.clean_text(text)

        if 'должен знать' in text.lower():
            # Попытка извлечь список знаний
            knowledge_items = re.split(r'[-–]\s*', text)
            if len(knowledge_items) > 1:
                result = "Сотрудник должен знать:\n\n"
                for item in knowledge_items[1:]:  # Пропускаем первый элемент
                    item = item.strip().rstrip(';.,')
                    if item and len(item) > 3:
                        result += f"- {item}\n"
                return result
            else:
                return text
        else:
            return "_(Перечень необходимых знаний и навыков)_"

    def format_documents(self, text: str) -> str:
        """Форматирование руководящих документов"""
        text = self.clean_text(text)
        if 'руководствуется' in text.lower():
            return f"Сотрудник в своей деятельности руководствуется:\n\n{text}"
        else:
            return "_(Перечень руководящих документов)_"

    def format_subordination(self, text: str) -> str:
        """Форматирование подчиненности"""
        text = self.clean_text(text)
        if 'подчиняется' in text.lower():
            return text
        else:
            return "_(Информация о подчиненности)_"

    def format_replacement(self, text: str) -> str:
        """Форматирование замещения"""
        text = self.clean_text(text)
        if any(word in text.lower() for word in ['замещ', 'отсутств', 'отпуск']):
            return text
        else:
            return "_(Порядок замещения при отсутствии)_"

    def clean_text(self, text: str) -> str:
        """Очистка текста"""
        # Убираем лишние пробелы и переносы
        text = re.sub(r'\s+', ' ', text.strip())
        # Убираем подчеркивания
        text = re.sub(r'_{3,}', '', text)
        return text

    def create_default_general_section(self, position: str) -> str:
        """Создание шаблона общих положений"""
        return f"""## 1. Общие положений

### 1.1. Категория должности

_(Укажите категорию должности {position})_

### 1.2. Требования к образованию и опыту

_(Укажите требования к образованию и опыту для должности {position})_

### 1.3. Знания и навыки

Сотрудник должен знать:

- _(перечень необходимых знаний)_
- основы трудового законодательства
- правила внутреннего трудового распорядка
- правила охраны труда и техники безопасности

### 1.4. Руководящие документы

Сотрудник в своей деятельности руководствуется:

- настоящей должностной инструкцией
- положением о структурном подразделении
- _(иные документы)_

### 1.5. Подчиненность

_(Укажите, кому подчиняется сотрудник)_

### 1.6. Замещение

_(Порядок замещения при отсутствии сотрудника)_

"""

    def format_functions_advanced(self, content: str) -> str:
        """Продвинутое форматирование функций"""
        result = "Основные функции:\n\n"

        # Ищем функции в различных форматах
        functions = re.findall(r'2\.\d+\.\s*(.*?)(?=2\.\d+\.|$)', content, re.DOTALL)
        if functions:
            for func in functions:
                func = self.clean_text(func)
                if func:
                    result += f"- {func}\n"
        else:
            # Попытка найти другие паттерны
            lines = content.split('\n')
            for line in lines:
                line = self.clean_text(line)
                if line and len(line) > 5:
                    result += f"- {line}\n"

        return result + "\n"

    def format_duties_advanced(self, content: str) -> str:
        """Продвинутое форматирование обязанностей"""
        result = "Сотрудник исполняет следующие обязанности:\n\n"

        # Ищем обязанности в различных форматах
        duties = re.findall(r'3\.\d+\.\s*(.*?)(?=3\.\d+\.|$)', content, re.DOTALL)
        counter = 1

        if duties:
            for duty in duties:
                duty = self.clean_text(duty)
                if duty and not re.match(r'_{3,}', duty):
                    result += f"{counter}. {duty}\n\n"
                    counter += 1
        else:
            # Альтернативный поиск
            lines = content.split('\n')
            for line in lines:
                line = self.clean_text(line)
                if line and len(line) > 10 and not re.match(r'\d+\.\d+\.', line):
                    result += f"{counter}. {line}\n\n"
                    counter += 1

        return result

    def format_rights_advanced(self, content: str) -> str:
        """Продвинутое форматирование прав"""
        result = "Сотрудник имеет право:\n\n"

        # Ищем права
        rights = re.findall(r'4\.\d+\.\s*(.*?)(?=4\.\d+\.|$)', content, re.DOTALL)
        counter = 1

        if rights:
            for right in rights:
                right = self.clean_text(right)
                if right and not re.match(r'_{3,}', right):
                    result += f"{counter}. {right}\n\n"
                    counter += 1

        return result

    def format_responsibility_advanced(self, content: str) -> str:
        """Продвинутое форматирование ответственности"""
        result = "### 5.1. Виды ответственности\n\n"
        result += "Сотрудник привлекается к ответственности:\n\n"

        # Стандартные типы ответственности
        standard_resp = [
            "за ненадлежащее исполнение или неисполнение своих должностных обязанностей - в порядке, установленном действующим трудовым законодательством РФ",
            "за правонарушения, совершенные в процессе своей деятельности - в порядке, установленном административным, уголовным и гражданским законодательством РФ",
            "за причинение ущерба имуществу организации - в порядке, установленном трудовым законодательством РФ"
        ]

        # Ищем в контенте или используем стандартные
        responsibility_found = False
        resp_items = re.split(r'[-–]\s*', content)

        for item in resp_items:
            item = self.clean_text(item)
            if item and len(item) > 15 and not re.match(r'5\.\d', item):
                result += f"- {item}\n\n"
                responsibility_found = True

        if not responsibility_found:
            for resp in standard_resp:
                result += f"- {resp}\n\n"

        return result

    def get_signatures_section(self) -> str:
        """Секция подписей"""
        return """## 6. Согласование и утверждение

### Подписи

**Руководитель структурного подразделения:** _________________ _(инициалы, фамилия)_

**Дата:** _(дата)_

### Ознакомление сотрудника

С должностной инструкцией ознакомлен(а), один экземпляр получил(а) на руки и обязуюсь хранить его на рабочем месте.

**Подпись сотрудника:** _________________ _(инициалы, фамилия)_

**Дата:** _(дата)_

"""

    def extract_position_from_filename(self, filename: str) -> str:
        """Улучшенное извлечение должности"""
        name = os.path.splitext(filename)[0]
        # Убираем префиксы
        name = re.sub(r'^(ПР\s+|Производственная инструкция\s+)', '', name)
        # Убираем лишние пробелы
        name = re.sub(r'\s+', ' ', name.strip())
        return name

    def add_metadata_advanced(self, content: str, position: str, department: str) -> str:
        """Расширенные метаданные"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        metadata = {
            "created_at": now,
            "updated_at": now,
            "author": "advanced_document_processor",
            "version": "2.0.0",
            "document_type": "должностная_инструкция",
            "position": self.normalize_name(position),
            "department": self.normalize_name(department),
            "processing_quality": self.assess_content_quality(content),
            "_fingerprint": ""
        }

        return content + f"<!-- METADATA\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n-->"

    def assess_content_quality(self, content: str) -> str:
        """Оценка качества обработки контента"""
        # Подсчитываем заполненные разделы
        filled_sections = 0
        total_sections = 5  # общие положения, функции, обязанности, права, ответственность

        if "### 1.1." in content: filled_sections += 1
        if "Основные функции:" in content and "_(Функции" not in content: filled_sections += 1
        if "исполняет следующие обязанности:" in content and "_(Обязанности" not in content: filled_sections += 1
        if "имеет право:" in content and "_(Права" not in content: filled_sections += 1
        if "Виды ответственности" in content: filled_sections += 1

        percentage = (filled_sections / total_sections) * 100

        if percentage >= 80:
            return "высокое"
        elif percentage >= 50:
            return "среднее"
        else:
            return "низкое"

    def normalize_name(self, name: str) -> str:
        """Нормализация имен"""
        name = re.sub(r'[^а-яА-Яa-zA-Z0-9\s]', '', str(name))
        return name.lower().replace(' ', '_')

    def is_already_processed(self, content: str) -> bool:
        """Проверка обработки"""
        return "<!-- METADATA" in content and (
            '"document_type": "должностная_инструкция"' in content or
            '"author": "document_processor"' in content or
            '"author": "advanced_document_processor"' in content
        )

    def process_file_advanced(self, file_path: str) -> bool:
        """Продвинутая обработка файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Проверяем обработку
            if self.is_already_processed(content) and not self.force_reprocess:
                print(f"Пропуск (уже обработан): {os.path.basename(file_path)}")
                self.skipped_count += 1
                return True

            if self.dry_run:
                print(f"[DRY RUN] Будет обработан: {os.path.basename(file_path)}")
                return True

            # Структурируем
            filename = os.path.basename(file_path)
            structured_content = self.advanced_structure_content(content, filename)

            # Добавляем метаданные
            position = self.extract_position_from_filename(filename)
            department = self.extract_department_from_path(file_path)
            final_content = self.add_metadata_advanced(structured_content, position, department)

            # Сохраняем
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(final_content)

            print(f"✅ Обработан: {os.path.basename(file_path)}")
            self.processed_count += 1
            return True

        except Exception as e:
            print(f"❌ Ошибка при обработке {os.path.basename(file_path)}: {str(e)}")
            self.error_count += 1
            return False

    def extract_department_from_path(self, path: str) -> str:
        """Извлечение департамента из пути"""
        parts = path.split('/')
        for part in parts:
            if part.isupper() and len(part) > 5:
                return part.lower().replace(' ', '_')
        return "неопределен"

    def process_directory_advanced(self, directory_path: str, file_pattern: str = "*.md") -> None:
        """Продвинутая обработка директории"""
        print(f"🚀 Начинаем обработку: {directory_path}")
        print(f"📁 Паттерн файлов: {file_pattern}")

        if self.force_reprocess:
            print("🔄 Режим: принудительная перезапись")

        if self.dry_run:
            print("🧪 Режим: пробный запуск (без изменений)")

        md_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))

        print(f"📊 Найдено файлов: {len(md_files)}")

        for file_path in md_files:
            self.process_file_advanced(file_path)

        print(f"\n{'='*50}")
        print(f"📈 ИТОГОВЫЙ ОТЧЕТ:")
        print(f"✅ Обработано успешно: {self.processed_count}")
        print(f"⏭️  Пропущено: {self.skipped_count}")
        print(f"❌ Ошибок: {self.error_count}")
        print(f"📁 Всего файлов: {len(md_files)}")
        print(f"{'='*50}")

def main():
    parser = argparse.ArgumentParser(description='Продвинутый обработчик должностных инструкций v2.0')
    parser.add_argument('directory', help='Путь к директории для обработки')
    parser.add_argument('--force', '-f', action='store_true', help='Принудительная перезапись уже обработанных файлов')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Пробный запуск без изменений')
    parser.add_argument('--pattern', '-p', default='*.md', help='Паттерн файлов (по умолчанию *.md)')

    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print(f"❌ Ошибка: Директория {args.directory} не найдена")
        return

    processor = AdvancedDocumentProcessor(
        force_reprocess=args.force,
        dry_run=args.dry_run
    )

    processor.process_directory_advanced(args.directory, args.pattern)

if __name__ == "__main__":
    # Если запускается без аргументов, используем базовый путь
    import sys
    if len(sys.argv) == 1:
        processor = AdvancedDocumentProcessor()
        base_path = "/home/uduntu33/Документы/PROJECT/modules/docs/Инструкции/Должностные инструкции"
        processor.process_directory_advanced(base_path)
    else:
        main()