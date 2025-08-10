#!/usr/bin/env python3
"""
Модуль анализаторов контента для различных типов документов
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ContentElement:
    """Элемент контента"""

    type: str  # 'heading', 'paragraph', 'list', 'table', 'quote', 'code'
    level: int  # Уровень вложенности
    content: str
    metadata: Dict[str, str]


class ContentAnalyzer(ABC):
    """Базовый класс анализатора контента"""

    @abstractmethod
    def analyze(self, content: str) -> List[ContentElement]:
        """Анализ контента"""
        pass

    @abstractmethod
    def clean(self, content: str) -> str:
        """Очистка контента"""
        pass


class TableAnalyzer(ContentAnalyzer):
    """Анализатор таблиц"""

    def analyze(self, content: str) -> List[ContentElement]:
        """Анализ таблиц в контенте"""
        elements = []

        # Поиск таблиц в различных форматах
        table_patterns = [
            # Markdown таблицы
            r"(\|[^\n]*\|[\n\r]*\|[-\s\|]*\|[\n\r]*(?:\|[^\n]*\|[\n\r]*)*)",
            # HTML таблицы
            r"(<table[^>]*>.*?</table>)",
            # Псевдо-таблицы с табуляцией
            r"((?:^[^\n]*\t[^\n]*$[\n\r]*){2,})",
        ]

        for i, pattern in enumerate(table_patterns):
            matches = re.finditer(
                pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE
            )
            for match in matches:
                table_content = match.group(1)
                elements.append(
                    ContentElement(
                        type="table",
                        level=0,
                        content=table_content,
                        metadata={
                            "format": f"type_{i}",
                            "position": str(match.start()),
                        },
                    )
                )

        return elements

    def clean(self, content: str) -> str:
        """Очистка таблиц"""
        # Удаление поврежденных таблиц
        content = re.sub(r"\|[\s\-\|]*\|\s*$", "", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*\|\s*$", "", content, flags=re.MULTILINE)

        # Преобразование простых таблиц в списки
        simple_table_pattern = r"^\|([^|]+)\|([^|]+)\|$"
        matches = re.findall(simple_table_pattern, content, re.MULTILINE)

        for col1, col2 in matches:
            if col1.strip() and col2.strip():
                replacement = f"**{col1.strip()}:** {col2.strip()}"
                original = f"|{col1}|{col2}|"
                content = content.replace(original, replacement)

        return content


class ListAnalyzer(ContentAnalyzer):
    """Анализатор списков"""

    def analyze(self, content: str) -> List[ContentElement]:
        """Анализ списков"""
        elements = []

        # Нумерованные списки
        numbered_pattern = r"^(\s*)(\d+\.)\s*(.+)$"
        numbered_matches = re.finditer(numbered_pattern, content, re.MULTILINE)

        for match in numbered_matches:
            indent, number, text = match.groups()
            level = len(indent) // 2
            elements.append(
                ContentElement(
                    type="numbered_list",
                    level=level,
                    content=text.strip(),
                    metadata={"number": number, "indent": indent},
                )
            )

        # Маркированные списки
        bullet_pattern = r"^(\s*)([-*•▪▫])\s*(.+)$"
        bullet_matches = re.finditer(bullet_pattern, content, re.MULTILINE)

        for match in bullet_matches:
            indent, bullet, text = match.groups()
            level = len(indent) // 2
            elements.append(
                ContentElement(
                    type="bullet_list",
                    level=level,
                    content=text.strip(),
                    metadata={"bullet": bullet, "indent": indent},
                )
            )

        return elements

    def clean(self, content: str) -> str:
        """Очистка списков"""
        # Исправление неправильных маркеров
        content = re.sub(r"^(\s*)[•▪▫]\s*", r"\1- ", content, flags=re.MULTILINE)

        # Удаление пустых элементов списка
        content = re.sub(r"^(\s*)[-*]\s*$", "", content, flags=re.MULTILINE)

        # Исправление нумерации
        lines = content.split("\n")
        in_numbered_list = False
        current_number = 1

        for i, line in enumerate(lines):
            if re.match(r"^\s*\d+\.\s", line):
                if not in_numbered_list:
                    in_numbered_list = True
                    current_number = 1

                # Исправляем нумерацию
                indent_match = re.match(r"^(\s*)\d+\.(\s*.+)$", line)
                if indent_match:
                    indent, rest = indent_match.groups()
                    lines[i] = f"{indent}{current_number}.{rest}"
                    current_number += 1
            else:
                if in_numbered_list and not line.strip():
                    continue
                else:
                    in_numbered_list = False
                    current_number = 1

        return "\n".join(lines)


class HeadingAnalyzer(ContentAnalyzer):
    """Анализатор заголовков"""

    def analyze(self, content: str) -> List[ContentElement]:
        """Анализ заголовков"""
        elements = []

        # Markdown заголовки
        heading_pattern = r"^(#{1,6})\s*(.+)$"
        matches = re.finditer(heading_pattern, content, re.MULTILINE)

        for match in matches:
            hashes, title = match.groups()
            level = len(hashes)
            elements.append(
                ContentElement(
                    type="heading",
                    level=level,
                    content=title.strip(),
                    metadata={"markdown_level": str(level)},
                )
            )

        # Заголовки с подчеркиванием
        underline_pattern = r"^(.+)\n(=+|-+)$"
        underline_matches = re.finditer(underline_pattern, content, re.MULTILINE)

        for match in underline_matches:
            title, underline = match.groups()
            level = 1 if underline[0] == "=" else 2
            elements.append(
                ContentElement(
                    type="heading",
                    level=level,
                    content=title.strip(),
                    metadata={"underline_style": underline[0]},
                )
            )

        return elements

    def clean(self, content: str) -> str:
        """Очистка заголовков"""
        # Исправление пробелов в заголовках
        content = re.sub(r"^(#{1,6})([^\s#])", r"\1 \2", content, flags=re.MULTILINE)

        # Удаление лишних символов в заголовках
        content = re.sub(
            r"^(#{1,6}\s*)(.+?)\s*#+\s*$", r"\1\2", content, flags=re.MULTILINE
        )

        # Преобразование заголовков с подчеркиванием в Markdown
        underline_pattern = r"^(.+)\n(=+)$"
        content = re.sub(underline_pattern, r"# \1", content, flags=re.MULTILINE)

        underline_pattern2 = r"^(.+)\n(-+)$"
        content = re.sub(underline_pattern2, r"## \1", content, flags=re.MULTILINE)

        return content


class ParagraphAnalyzer(ContentAnalyzer):
    """Анализатор параграфов"""

    def analyze(self, content: str) -> List[ContentElement]:
        """Анализ параграфов"""
        elements = []

        # Разделяем контент на параграфы
        paragraphs = re.split(r"\n\s*\n", content)

        for para in paragraphs:
            para = para.strip()
            if not para or para.startswith("#"):
                continue

            # Определяем тип параграфа
            para_type = "paragraph"
            metadata = {}

            # Цитаты
            if para.startswith(">"):
                para_type = "quote"
                metadata["quote_level"] = str(len(re.match(r"^>+", para).group()))

            # Код
            elif para.startswith("```") or para.startswith("    "):
                para_type = "code"
                if para.startswith("```"):
                    lang_match = re.match(r"^```(\w+)", para)
                    if lang_match:
                        metadata["language"] = lang_match.group(1)

            # Определяем важность по ключевым словам
            important_keywords = [
                "важно",
                "внимание",
                "примечание",
                "осторожно",
                "предупреждение",
            ]
            if any(keyword in para.lower() for keyword in important_keywords):
                metadata["importance"] = "high"

            elements.append(
                ContentElement(type=para_type, level=0, content=para, metadata=metadata)
            )

        return elements

    def clean(self, content: str) -> str:
        """Очистка параграфов"""
        # Исправление разорванных предложений
        lines = content.split("\n")
        cleaned_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                cleaned_lines.append("")
                i += 1
                continue

            # Если строка не заканчивается знаком препинания и следующая строка не является заголовком/списком
            if (
                i + 1 < len(lines)
                and not re.search(r"[.!?:;]$", line)
                and lines[i + 1].strip()
                and not re.match(r"^(#{1,6}|\s*[-*•]\s*|\s*\d+\.\s*)", lines[i + 1])
            ):

                # Объединяем строки
                next_line = lines[i + 1].strip()
                if next_line and not next_line[0].isupper():
                    line += " " + next_line
                    i += 2
                else:
                    cleaned_lines.append(line)
                    i += 1
            else:
                cleaned_lines.append(line)
                i += 1

        content = "\n".join(cleaned_lines)

        # Удаление лишних пробелов
        content = re.sub(r" {2,}", " ", content)

        # Исправление кавычек
        content = re.sub(r'[""]', '"', content)
        content = content.replace(""", "'").replace(""", "'")

        return content


class ContentProcessor:
    """Основной процессор контента"""

    def __init__(self):
        self.analyzers = {
            "table": TableAnalyzer(),
            "list": ListAnalyzer(),
            "heading": HeadingAnalyzer(),
            "paragraph": ParagraphAnalyzer(),
        }

    def process_content(
        self, content: str
    ) -> Tuple[str, Dict[str, List[ContentElement]]]:
        """Обработка контента"""

        # Анализируем контент всеми анализаторами
        analysis_results = {}
        for name, analyzer in self.analyzers.items():
            analysis_results[name] = analyzer.analyze(content)

        # Применяем очистку
        cleaned_content = content
        for analyzer in self.analyzers.values():
            cleaned_content = analyzer.clean(cleaned_content)

        return cleaned_content, analysis_results

    def generate_content_report(
        self, analysis_results: Dict[str, List[ContentElement]]
    ) -> str:
        """Генерация отчета об анализе контента"""

        report = "## Анализ контента\n\n"

        for analyzer_name, elements in analysis_results.items():
            if elements:
                report += f"### {analyzer_name.title()}\n"
                report += f"Найдено элементов: {len(elements)}\n\n"

                for i, element in enumerate(elements[:5]):  # Показываем первые 5
                    report += f"**Элемент {i+1}:**\n"
                    report += f"- Тип: {element.type}\n"
                    report += f"- Уровень: {element.level}\n"
                    report += f"- Содержимое: {element.content[:100]}...\n"
                    if element.metadata:
                        report += f"- Метаданные: {element.metadata}\n"
                    report += "\n"

                if len(elements) > 5:
                    report += f"... и еще {len(elements) - 5} элементов\n\n"

        return report


class SmartContentExtractor:
    """Умный извлекатель контента"""

    def __init__(self):
        self.content_processor = ContentProcessor()

    def extract_structured_content(self, content: str) -> Dict[str, str]:
        """Извлечение структурированного контента"""

        cleaned_content, analysis = self.content_processor.process_content(content)

        # Извлекаем заголовки и их содержимое
        headings = analysis.get("heading", [])
        sections = {}

        if not headings:
            return {"main_content": cleaned_content}

        # Сортируем заголовки по позиции в тексте
        heading_positions = []
        for heading in headings:
            pos = cleaned_content.find(heading.content)
            if pos != -1:
                heading_positions.append((pos, heading))

        heading_positions.sort(key=lambda x: x[0])

        # Извлекаем содержимое между заголовками
        for i, (pos, heading) in enumerate(heading_positions):
            section_start = pos

            # Находим начало следующего заголовка того же или более высокого уровня
            section_end = len(cleaned_content)
            for j in range(i + 1, len(heading_positions)):
                next_pos, next_heading = heading_positions[j]
                if next_heading.level <= heading.level:
                    section_end = next_pos
                    break

            # Извлекаем содержимое секции
            section_content = cleaned_content[section_start:section_end].strip()

            # Убираем сам заголовок из содержимого
            section_lines = section_content.split("\n")
            if section_lines and heading.content in section_lines[0]:
                section_content = "\n".join(section_lines[1:]).strip()

            sections[heading.content] = section_content

        return sections

    def smart_merge_sections(
        self, sections: Dict[str, str], target_sections: List[str]
    ) -> Dict[str, str]:
        """Умное объединение разделов"""

        merged = {}

        for target in target_sections:
            target_clean = re.sub(r"^\d+\.\s*", "", target).lower()

            # Прямое совпадение
            for section_name, content in sections.items():
                section_clean = section_name.lower()
                if target_clean == section_clean:
                    merged[target] = content
                    break
            else:
                # Поиск по ключевым словам
                best_match = None
                best_score = 0

                keywords = target_clean.split()

                for section_name, content in sections.items():
                    section_clean = section_name.lower()
                    score = sum(1 for keyword in keywords if keyword in section_clean)

                    if score > best_score:
                        best_score = score
                        best_match = content

                if best_match and best_score > 0:
                    merged[target] = best_match
                else:
                    merged[target] = ""

        return merged
