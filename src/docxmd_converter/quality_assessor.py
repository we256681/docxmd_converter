#!/usr/bin/env python3
"""
Оценщик качества документов
"""

import re
from collections import Counter
from typing import Dict, List

from .models import DocumentFeatures, QualityAssessment


class IntelligentQualityAssessor:
    """Интеллектуальный оценщик качества документов"""

    def __init__(self):
        # Пороговые значения для оценки качества
        self.thresholds = {
            'min_word_count': 50,
            'max_avg_sentence_length': 25,
            'min_vocabulary_richness': 0.3,
            'min_structure_complexity': 0.1,
            'min_formality_score': 0.2
        }

    def assess_quality(self, text: str, features: DocumentFeatures,
                      document_type: str = "general",
                      extracted_data: Dict = None) -> QualityAssessment:
        """Комплексная оценка качества документа"""

        if extracted_data is None:
            extracted_data = {}

        # Оценка структуры
        structure_score = self._assess_structure(features)

        # Оценка содержания
        content_score = self._assess_content(text, features, document_type, extracted_data)

        # Оценка согласованности
        consistency_score = self._assess_consistency(text, features)

        # Оценка полноты
        completeness_score = self._assess_completeness(text, document_type, extracted_data)

        # Оценка форматирования
        formatting_score = self._assess_formatting(text, features)

        # Общая оценка (взвешенная)
        overall_score = (
            structure_score * 0.25 +
            content_score * 0.35 +
            consistency_score * 0.20 +
            completeness_score * 0.20
        )

        # Выявление проблем
        issues = self._identify_issues(text, features, document_type)
        critical_issues = self._identify_critical_issues(text, features, document_type)

        # Рекомендации
        recommendations = self._generate_recommendations(
            structure_score, content_score, consistency_score,
            completeness_score, issues
        )

        return QualityAssessment(
            overall_score=overall_score,
            structure_score=structure_score,
            content_score=content_score,
            consistency_score=consistency_score,
            completeness_score=completeness_score,
            formatting_score=formatting_score,
            issues=issues,
            recommendations=recommendations,
            critical_issues=critical_issues
        )

    def _assess_structure(self, features: DocumentFeatures) -> float:
        """Оценка структуры документа"""
        score = 1.0

        # Проверка наличия заголовков
        if features.heading_count == 0:
            score -= 0.3
        elif features.heading_count < features.paragraph_count / 5:
            score -= 0.1

        # Проверка сложности структуры
        if features.structure_complexity < self.thresholds['min_structure_complexity']:
            score -= 0.2

        # Проверка длины предложений
        if features.avg_sentence_length > self.thresholds['max_avg_sentence_length']:
            score -= 0.2

        # Проверка наличия списков и таблиц
        if features.list_count == 0 and features.table_count == 0:
            score -= 0.1

        return max(score, 0.0)

    def _assess_content(self, text: str, features: DocumentFeatures,
                       document_type: str, extracted_data: Dict) -> float:
        """Оценка содержания документа"""
        score = 1.0

        # Проверка объема
        if features.word_count < self.thresholds['min_word_count']:
            score -= 0.3

        # Проверка богатства словаря
        if features.vocabulary_richness < self.thresholds['min_vocabulary_richness']:
            score -= 0.2

        # Проверка формальности (для официальных документов)
        if document_type in ["должностная_инструкция", "положение", "регламент"]:
            if features.formality_score < self.thresholds['min_formality_score']:
                score -= 0.2

        # Проверка наличия ключевой информации
        if not extracted_data or len(extracted_data) < 3:
            score -= 0.2

        # Проверка на артефакты конвертации
        artifacts = re.findall(r'[^\w\s\.,!?;:()\[\]{}"\'-]', text)
        if len(artifacts) > features.word_count * 0.05:  # Более 5% артефактов
            score -= 0.3

        return max(score, 0.0)

    def _assess_consistency(self, text: str, features: DocumentFeatures) -> float:
        """Оценка согласованности документа"""
        score = 1.0

        # Проверка согласованности нумерации
        numbered_items = re.findall(r"^\s*(\d+)\.", text, re.MULTILINE)
        if numbered_items:
            numbers = [int(n) for n in numbered_items]
            expected = list(range(1, len(numbers) + 1))
            if numbers != expected:
                score -= 0.3

        # Проверка согласованности терминологии
        words = re.findall(r'\b[а-яёa-z]+\b', text.lower())
        word_freq = Counter(words)

        # Ищем потенциальные вариации терминов
        variations = 0
        for word in word_freq:
            if len(word) > 4:
                similar = [w for w in word_freq if w != word and
                          (word in w or w in word) and abs(len(w) - len(word)) <= 2]
                if similar:
                    variations += 1

        if variations > len(set(words)) * 0.1:  # Более 10% вариаций
            score -= 0.2

        # Проверка согласованности стиля заголовков
        headings = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
        if headings:
            # Проверяем единообразие заглавных букв
            title_case_count = sum(1 for h in headings if h[0].isupper())
            if title_case_count != len(headings) and title_case_count != 0:
                score -= 0.1

        return max(score, 0.0)

    def _assess_completeness(self, text: str, document_type: str,
                           extracted_data: Dict) -> float:
        """Оценка полноты документа"""
        score = 1.0

        if document_type == "должностная_инструкция":
            required_sections = [
                "общие положения", "обязанности", "права", "ответственность"
            ]
            found_sections = sum(
                1 for section in required_sections if section in text.lower()
            )
            score = found_sections / len(required_sections)

        elif document_type == "отчет":
            required_sections = ["введение", "результаты", "выводы"]
            found_sections = sum(
                1 for section in required_sections if section in text.lower()
            )
            score = found_sections / len(required_sections)

        elif document_type == "положение":
            required_sections = [
                "общие положения", "основные понятия", "порядок", "заключительные положения"
            ]
            found_sections = sum(
                1 for section in required_sections if section in text.lower()
            )
            score = found_sections / len(required_sections)

        else:
            # Для других типов документов - базовая оценка
            if len(extracted_data) > 5:
                score = 1.0
            elif len(extracted_data) > 2:
                score = 0.8
            elif len(extracted_data) > 0:
                score = 0.5
            else:
                score = 0.2

        return max(score, 0.0)

    def _identify_issues(self, text: str, features: DocumentFeatures,
                        document_type: str) -> List[str]:
        """Выявление проблем в документе"""
        issues = []

        # Проблемы структуры
        if features.heading_count == 0:
            issues.append("Отсутствуют заголовки")

        if features.avg_sentence_length > 30:
            issues.append("Слишком длинные предложения (усложняют восприятие)")

        if features.paragraph_count < 3:
            issues.append("Недостаточное разделение на абзацы")

        # Проблемы содержания
        if features.word_count < 100:
            issues.append("Слишком короткий документ")

        if features.vocabulary_richness < 0.2:
            issues.append("Низкое разнообразие словаря")

        # Проблемы конвертации
        artifacts_count = len(re.findall(r'[^\w\s\.,!?;:()\[\]{}"\'-]', text))
        if artifacts_count > features.word_count * 0.05:
            issues.append(f"Множественные артефакты конвертации ({artifacts_count})")

        # Проблемы формата
        if "требует заполнения" in text.lower():
            issues.append("Документ содержит незаполненные разделы")

        if re.search(r'\b[A-Z]{3,}\b', text):
            issues.append("Обнаружены слова в верхнем регистре (возможно, ошибки форматирования)")

        return issues

    def _generate_recommendations(self, structure_score: float, content_score: float,
                                consistency_score: float, completeness_score: float,
                                issues: List[str]) -> List[str]:
        """Генерация рекомендаций по улучшению"""
        recommendations = []

        if structure_score < 0.7:
            recommendations.append("Добавьте заголовки для лучшей структуризации")
            recommendations.append("Разбейте длинные абзацы на более короткие")

        if content_score < 0.7:
            recommendations.append("Расширьте содержание документа")
            recommendations.append("Используйте более разнообразную лексику")

        if consistency_score < 0.7:
            recommendations.append("Проверьте согласованность терминологии")
            recommendations.append("Унифицируйте стиль заголовков")

        if completeness_score < 0.7:
            recommendations.append("Добавьте недостающие обязательные разделы")
            recommendations.append("Заполните все необходимые поля")

        if "артефакты конвертации" in str(issues):
            recommendations.append("Выполните дополнительную очистку от артефактов конвертации")

        if not recommendations:
            recommendations.append("Документ соответствует основным требованиям качества")

        return recommendations

    def _assess_formatting(self, text: str, features: DocumentFeatures) -> float:
        """Оценка форматирования документа"""
        score = 1.0

        # Проверка на артефакты форматирования
        formatting_issues = 0

        # Множественные пробелы
        if re.search(r'  +', text):
            formatting_issues += 1

        # Неправильные переносы строк
        if re.search(r'\n\s*\n\s*\n', text):
            formatting_issues += 1

        # Смешанные стили заголовков
        markdown_headers = len(re.findall(r'^#+\s', text, re.MULTILINE))
        if markdown_headers > 0 and markdown_headers != features.heading_count:
            formatting_issues += 1

        # Неправильная пунктуация
        if re.search(r'[.!?]{2,}', text):
            formatting_issues += 1

        # Снижаем оценку за каждую проблему
        score -= formatting_issues * 0.2

        return max(score, 0.0)

    def _identify_critical_issues(self, text: str, features: DocumentFeatures,
                                 document_type: str) -> List[str]:
        """Выявление критических проблем"""
        critical_issues = []

        # Критически короткий документ
        if features.word_count < 20:
            critical_issues.append("Критически малый объем документа")

        # Отсутствие структуры
        if features.heading_count == 0 and features.paragraph_count < 2:
            critical_issues.append("Полное отсутствие структуры документа")

        # Множественные артефакты
        artifacts_count = len(re.findall(r'[^\w\s\.,!?;:()\[\]{}"\'-]', text))
        if artifacts_count > features.word_count * 0.1:
            critical_issues.append("Критическое количество артефактов конвертации")

        # Нечитаемый текст
        if features.vocabulary_richness < 0.1:
            critical_issues.append("Крайне низкое качество текста")

        return critical_issues