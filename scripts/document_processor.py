#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматический обработчик должностных инструкций
Очищает и структурирует документы .md согласно стилевому руководству
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class DocumentProcessor:
    def __init__(self):
        self.processed_count = 0
        self.skipped_count = 0
        self.error_count = 0

    def clean_line_breaks(self, text: str) -> str:
        """Очистка лишних переносов строк и backslash переносов"""
        # Удаляем backslash переносы
        text = re.sub(r"\\\n", " ", text)
        text = re.sub(r"\\\r\n", " ", text)
        # Удаляем лишние пробелы
        text = re.sub(r" +", " ", text)
        return text.strip()

    def remove_consultant_plus_elements(self, content: str) -> str:
        """Удаление элементов КонсультантПлюс"""
        # Удаляем блоки с разделителями
        content = re.sub(r"-{20,}.*?-{20,}", "", content, flags=re.DOTALL)

        # Удаляем изображения и ссылки на медиафайлы
        content = re.sub(r"!\[.*?\]\(.*?media/.*?\).*?\n", "", content)

        # Удаляем ссылки на КонсультантПлюс
        content = re.sub(
            r"Документ предоставлен.*?www\.consultant\.ru.*?\n",
            "",
            content,
            flags=re.DOTALL,
        )

        # Удаляем информацию о дате сохранения
        content = re.sub(r"Дата сохранения:.*?\n", "", content)

        # Удаляем блоки "Актуально на"
        content = re.sub(r"\*\*Актуально на.*?\*\*", "", content)

        # Удаляем таблицы с информацией
        content = re.sub(r"\+.*?\+.*?\n", "", content)
        content = re.sub(r"\|.*?\|.*?\n", "", content)

        # Удаляем блоки "См.:"
        content = re.sub(r"См\.:.*?Путеводитель.*?\n", "", content, flags=re.DOTALL)

        return content

    def remove_formatting_artifacts(self, content: str) -> str:
        """Удаление артефактов форматирования из Word"""
        # Удаляем служебные разделители
        content = re.sub(r"_{10,}", "", content)
        content = re.sub(r"─{10,}", "", content)
        content = re.sub(r"--+ --+.*?--+", "", content, flags=re.DOTALL)

        # Очищаем лишние пробелы и отступы в начале строк
        lines = content.split("\n")
        cleaned_lines = []
        for line in lines:
            # Убираем лишние пробелы в начале строки
            line = re.sub(r"^ +", "", line)
            if line.strip():  # Добавляем только не пустые строки
                cleaned_lines.append(line)

        content = "\n".join(cleaned_lines)

        # Удаляем множественные пустые строки
        content = re.sub(r"\n{3,}", "\n\n", content)

        return content

    def extract_position_name(self, content: str) -> str:
        """Извлечение названия должности из документа"""
        # Ищем в начале документа название должности
        match = re.search(r"\*\*(.*?)\*\*", content)
        if match:
            position = match.group(1).strip()
            # Очищаем от служебных слов
            position = re.sub(
                r"(должностная инструкция|агент.*)", "", position, flags=re.IGNORECASE
            )
            return position.strip()

        # Попытаемся извлечь из имени файла
        return "должность"

    def structure_content(self, content: str, filename: str) -> str:
        """Структурирование содержимого согласно стилевому руководству"""

        # Извлекаем название должности
        position_name = self.extract_position_from_filename(filename)

        # Начинаем с чистого шаблона
        structured_content = f"# Должностная инструкция: {position_name}\n\n"
        structured_content += "## Информация о документе\n\n"
        structured_content += "**Организация:** _(наименование организации)_\n\n"
        structured_content += (
            "**Утверждено:** _(подпись, инициалы, фамилия руководителя)_\n\n"
        )
        structured_content += "**Дата утверждения:** _(дата)_\n\n"

        # Извлекаем и структурируем разделы
        sections = self.extract_sections(content)

        # Общие положения
        if "general" in sections:
            structured_content += "## 1. Общие положения\n\n"
            structured_content += self.format_general_section(sections["general"])

        # Функции
        if "functions" in sections:
            structured_content += "## 2. Функции\n\n"
            structured_content += self.format_functions_section(sections["functions"])

        # Обязанности
        if "duties" in sections:
            structured_content += "## 3. Должностные обязанности\n\n"
            structured_content += self.format_duties_section(sections["duties"])

        # Права
        if "rights" in sections:
            structured_content += "## 4. Права\n\n"
            structured_content += self.format_rights_section(sections["rights"])

        # Ответственность
        if "responsibility" in sections:
            structured_content += "## 5. Ответственность\n\n"
            structured_content += self.format_responsibility_section(
                sections["responsibility"]
            )

        # Подписи
        structured_content += "## 6. Согласование и утверждение\n\n"
        structured_content += "### Подписи\n\n"
        structured_content += "**Руководитель структурного подразделения:** _________________ _(инициалы, фамилия)_\n\n"
        structured_content += "**Дата:** _(дата)_\n\n"
        structured_content += "### Ознакомление сотрудника\n\n"
        structured_content += "С должностной инструкцией ознакомлен(а), один экземпляр получил(а) на руки и обязуюсь хранить его на рабочем месте.\n\n"
        structured_content += (
            "**Подпись сотрудника:** _________________ _(инициалы, фамилия)_\n\n"
        )
        structured_content += "**Дата:** _(дата)_\n\n"

        return structured_content

    def extract_position_from_filename(self, filename: str) -> str:
        """Извлечение названия должности из имени файла"""
        # Убираем расширение
        name = os.path.splitext(filename)[0]
        # Заменяем некоторые сокращения
        name = re.sub(r"^ПР\s+", "", name)  # Убираем префикс ПР
        return name.strip()

    def extract_sections(self, content: str) -> Dict[str, str]:
        """Извлечение разделов из содержимого"""
        sections = {}

        # Общие положения
        general_match = re.search(
            r"1\.\s*Общие положения(.*?)(?=\d+\.|$)", content, re.DOTALL | re.IGNORECASE
        )
        if general_match:
            sections["general"] = general_match.group(1).strip()

        # Функции
        functions_match = re.search(
            r"2\.\s*Функции(.*?)(?=\d+\.|$)", content, re.DOTALL | re.IGNORECASE
        )
        if functions_match:
            sections["functions"] = functions_match.group(1).strip()

        # Должностные обязанности
        duties_match = re.search(
            r"3\.\s*Должностные обязанности(.*?)(?=\d+\.|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if duties_match:
            sections["duties"] = duties_match.group(1).strip()

        # Права
        rights_match = re.search(
            r"4\.\s*Права(.*?)(?=\d+\.|$)", content, re.DOTALL | re.IGNORECASE
        )
        if rights_match:
            sections["rights"] = rights_match.group(1).strip()

        # Ответственность
        resp_match = re.search(
            r"5\.\s*Ответственность(.*?)(?=\d+\.|─|$)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if resp_match:
            sections["responsibility"] = resp_match.group(1).strip()

        return sections

    def format_general_section(self, content: str) -> str:
        """Форматирование раздела общих положений"""
        result = ""

        # Ищем подразделы
        parts = re.split(r"(\d+\.\d+\.)", content)
        current_subsection = ""

        for i, part in enumerate(parts):
            if re.match(r"\d+\.\d+\.", part):
                current_subsection = part
            elif current_subsection and part.strip():
                subsection_content = self.clean_line_breaks(part)

                if "1.1." in current_subsection:
                    result += "### 1.1. Категория должности\n\n"
                elif "1.2." in current_subsection:
                    result += "### 1.2. Требования к образованию и опыту\n\n"
                elif "1.3." in current_subsection:
                    result += "### 1.3. Знания и навыки\n\n"
                    # Форматируем список знаний
                    subsection_content = self.format_knowledge_list(subsection_content)
                elif "1.4." in current_subsection:
                    result += "### 1.4. Руководящие документы\n\n"
                elif "1.5." in current_subsection:
                    result += "### 1.5. Подчиненность\n\n"
                elif "1.6." in current_subsection:
                    result += "### 1.6. Замещение\n\n"
                else:
                    result += f"### {current_subsection.strip()}\n\n"

                result += f"{subsection_content}\n\n"

        return result

    def format_knowledge_list(self, content: str) -> str:
        """Форматирование списка знаний в виде markdown списка"""
        result = "Агент должен знать:\n\n"

        # Разбиваем на элементы списка
        items = re.split(r"[-–]\s*", content)
        for item in items:
            item = item.strip()
            if item and not re.match(r"^\d", item):  # Исключаем номера разделов
                item = re.sub(r";$", "", item)  # Убираем точку с запятой в конце
                result += f"- {item}\n"

        return result

    def format_functions_section(self, content: str) -> str:
        """Форматирование раздела функций"""
        result = "Основные функции:\n\n"

        # Ищем пункты функций
        functions = re.findall(r"2\.\d+\.\s*(.*?)(?=2\.\d+\.|$)", content, re.DOTALL)
        for func in functions:
            func = self.clean_line_breaks(func).strip()
            if func:
                result += f"- {func}\n"

        return result + "\n"

    def format_duties_section(self, content: str) -> str:
        """Форматирование раздела обязанностей"""
        result = "Сотрудник исполняет следующие обязанности:\n\n"

        # Ищем пункты обязанностей
        duties = re.findall(r"3\.\d+\.\s*(.*?)(?=3\.\d+\.|$)", content, re.DOTALL)
        for i, duty in enumerate(duties, 1):
            duty = self.clean_line_breaks(duty).strip()
            if duty and not re.match(r"_{5,}", duty):  # Исключаем строки подчеркиваний
                result += f"{i}. {duty}\n\n"

        return result

    def format_rights_section(self, content: str) -> str:
        """Форматирование раздела прав"""
        result = "Сотрудник имеет право:\n\n"

        # Ищем пункты прав
        rights = re.findall(r"4\.\d+\.\s*(.*?)(?=4\.\d+\.|$)", content, re.DOTALL)
        for i, right in enumerate(rights, 1):
            right = self.clean_line_breaks(right).strip()
            if right and not re.match(
                r"_{5,}", right
            ):  # Исключаем строки подчеркиваний
                result += f"{i}. {right}\n\n"

        return result

    def format_responsibility_section(self, content: str) -> str:
        """Форматирование раздела ответственности"""
        result = "### 5.1. Виды ответственности\n\n"
        result += "Сотрудник привлекается к ответственности:\n\n"

        # Ищем пункты ответственности
        resp_items = re.split(r"[-–]\s*", content)
        for item in resp_items:
            item = self.clean_line_breaks(item).strip()
            if (
                item and len(item) > 10 and not re.match(r"5\.\d", item)
            ):  # Исключаем номера и короткие строки
                result += f"- {item}\n\n"

        return result

    def add_metadata(self, content: str, position: str, department: str) -> str:
        """Добавление метаданных в конец документа"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        metadata = {
            "created_at": now,
            "updated_at": now,
            "author": "document_processor",
            "version": "1.0.0",
            "document_type": "должностная_инструкция",
            "position": self.normalize_position_name(position),
            "department": self.normalize_department_name(department),
            "_fingerprint": "",
        }

        metadata_str = (
            f"<!-- METADATA\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n-->"
        )

        return content + metadata_str

    def normalize_position_name(self, name: str) -> str:
        """Нормализация названия должности для метаданных"""
        return re.sub(r"[^а-яА-Яa-zA-Z0-9\s]", "", name).lower().replace(" ", "_")

    def normalize_department_name(self, path: str) -> str:
        """Извлечение и нормализация названия отдела из пути"""
        parts = path.split("/")
        for part in parts:
            if (
                part.isupper() and len(part) > 5
            ):  # Находим название отдела в верхнем регистре
                return part.lower().replace(" ", "_").replace("_и_", "_")
        return "неопределен"

    def is_already_processed(self, content: str) -> bool:
        """Проверка, был ли файл уже обработан"""
        return (
            "<!-- METADATA" in content
            and '"document_type": "должностная_инструкция"' in content
        )

    def process_file(self, file_path: str) -> bool:
        """Обработка одного файла"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Проверяем, не обработан ли уже файл
            if self.is_already_processed(content):
                print(f"Пропуск (уже обработан): {os.path.basename(file_path)}")
                self.skipped_count += 1
                return True

            # Очищаем от артефактов КонсультантПлюс
            content = self.remove_consultant_plus_elements(content)

            # Удаляем артефакты форматирования
            content = self.remove_formatting_artifacts(content)

            # Структурируем содержимое
            filename = os.path.basename(file_path)
            structured_content = self.structure_content(content, filename)

            # Добавляем метаданные
            position = self.extract_position_from_filename(filename)
            department = self.normalize_department_name(file_path)
            final_content = self.add_metadata(structured_content, position, department)

            # Сохраняем обработанный файл
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            print(f"Обработан: {os.path.basename(file_path)}")
            self.processed_count += 1
            return True

        except Exception as e:
            print(f"Ошибка при обработке {os.path.basename(file_path)}: {str(e)}")
            self.error_count += 1
            return False

    def process_directory(self, directory_path: str) -> None:
        """Обработка всех файлов в директории"""
        print(f"Начинаем обработку директории: {directory_path}")

        md_files = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))

        print(f"Найдено файлов для обработки: {len(md_files)}")

        for file_path in md_files:
            self.process_file(file_path)

        print(f"\n=== ИТОГИ ОБРАБОТКИ ===")
        print(f"Обработано успешно: {self.processed_count}")
        print(f"Пропущено: {self.skipped_count}")
        print(f"Ошибок: {self.error_count}")
        print(f"Всего файлов: {len(md_files)}")


def main():
    """Основная функция"""
    processor = DocumentProcessor()
    base_path = "/home/uduntu33/Документы/PROJECT/modules/docs/Инструкции/Должностные инструкции"

    if not os.path.exists(base_path):
        print(f"Ошибка: Директория {base_path} не найдена")
        return

    processor.process_directory(base_path)


if __name__ == "__main__":
    main()
