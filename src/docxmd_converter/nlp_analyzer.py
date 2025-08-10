#!/usr/bin/env python3
"""
NLP анализатор для обработки текста документов
"""

import re
import statistics
from collections import Counter
from typing import Dict, List, Tuple

from .models import DocumentFeatures


class NLPAnalyzer:
    """Анализатор естественного языка для документов"""

    def __init__(self):
        # Стоп-слова для русского языка (базовый набор)
        self.stop_words = {
            "и", "в", "на", "с", "по", "для", "от", "до", "при", "за", "под",
            "над", "между", "через", "без", "про", "против", "около", "возле",
            "что", "как", "где", "когда", "почему", "зачем", "который", "какой",
            "чей", "сколько", "насколько", "откуда", "куда", "отсюда", "туда",
            "здесь", "там", "везде", "нигде", "всюду", "где-то", "куда-то",
            "не", "ни", "да", "нет", "или", "либо", "то", "если", "хотя",
            "чтобы", "пока", "пусть", "будто", "словно", "точно", "именно"
        }

        # Формальные слова и фразы
        self.formal_indicators = {
            "согласно", "в соответствии", "на основании", "в целях", "с целью",
            "в связи", "в рамках", "посредством", "путем", "в ходе", "в процессе",
            "настоящий", "данный", "указанный", "вышеуказанный", "нижеследующий",
            "должен", "обязан", "вправе", "имеет право", "несет ответственность",
            "осуществляет", "обеспечивает", "контролирует", "утверждает"
        }

    def extract_features(self, text: str) -> DocumentFeatures:
        """Извлечение признаков из текста"""

        # Базовые метрики
        words = self._extract_words(text)
        sentences = self._extract_sentences(text)
        paragraphs = text.split('\n\n')

        # Структурные элементы
        headings = re.findall(r'^#+\s+.+$', text, re.MULTILINE)
        lists = re.findall(r'^\s*[-*+]\s+.+$', text, re.MULTILINE)
        tables = re.findall(r'\|.*\|', text)

        # Вычисляемые метрики
        word_count = len(words)
        sentence_count = len(sentences)
        paragraph_count = len([p for p in paragraphs if p.strip()])

        avg_sentence_length = (
            sum(len(s.split()) for s in sentences) / sentence_count
            if sentence_count > 0 else 0
        )

        vocabulary_richness = (
            len(set(words)) / word_count if word_count > 0 else 0
        )

        structure_complexity = self._calculate_structure_complexity(
            len(headings), len(lists), len(tables), paragraph_count
        )

        formality_score = self._calculate_formality_score(text, words)

        return DocumentFeatures(
            word_count=word_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            heading_count=len(headings),
            list_count=len(lists),
            table_count=len(tables),
            avg_sentence_length=avg_sentence_length,
            vocabulary_richness=vocabulary_richness,
            structure_complexity=structure_complexity,
            formality_score=formality_score
        )

    def _extract_words(self, text: str) -> List[str]:
        """Извлечение слов из текста"""
        # Удаляем markdown разметку и специальные символы
        clean_text = re.sub(r'[#*_`\[\](){}]', ' ', text)
        clean_text = re.sub(r'https?://\S+', ' ', clean_text)

        # Извлекаем слова (только кириллица и латиница)
        words = re.findall(r'\b[а-яёa-z]+\b', clean_text.lower())

        # Фильтруем стоп-слова
        return [word for word in words if word not in self.stop_words and len(word) > 2]

    def _extract_sentences(self, text: str) -> List[str]:
        """Извлечение предложений из текста"""
        # Простое разделение по знакам препинания
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    def _calculate_structure_complexity(self, headings: int, lists: int,
                                      tables: int, paragraphs: int) -> float:
        """Расчет сложности структуры документа"""
        if paragraphs == 0:
            return 0.0

        # Нормализуем показатели
        heading_ratio = min(headings / paragraphs, 1.0)
        list_ratio = min(lists / paragraphs, 1.0)
        table_ratio = min(tables / paragraphs, 1.0)

        # Взвешенная сумма
        complexity = (
            heading_ratio * 0.4 +
            list_ratio * 0.3 +
            table_ratio * 0.3
        )

        return min(complexity, 1.0)

    def _calculate_formality_score(self, text: str, words: List[str]) -> float:
        """Расчет уровня формальности текста"""
        if not words:
            return 0.0

        formal_count = 0
        text_lower = text.lower()

        # Подсчитываем формальные индикаторы
        for indicator in self.formal_indicators:
            formal_count += text_lower.count(indicator)

        # Нормализуем по количеству слов
        formality_ratio = formal_count / len(words)

        # Дополнительные индикаторы формальности
        if re.search(r'\d+\.\d+\.\d+', text):  # Нумерация разделов
            formality_ratio += 0.1

        if re.search(r'статья|пункт|подпункт|раздел|глава', text_lower):
            formality_ratio += 0.1

        if re.search(r'должностная инструкция|положение|регламент|приказ', text_lower):
            formality_ratio += 0.2

        return min(formality_ratio, 1.0)

    def analyze_terminology_consistency(self, text: str) -> Dict[str, int]:
        """Анализ согласованности терминологии"""
        words = self._extract_words(text)
        word_freq = Counter(words)

        # Ищем потенциальные вариации терминов
        variations = {}
        for word in word_freq:
            if len(word) > 4:  # Только длинные слова
                # Ищем похожие слова (простая эвристика)
                similar = [w for w in word_freq if w != word and
                          (word in w or w in word) and abs(len(w) - len(word)) <= 2]
                if similar:
                    variations[word] = word_freq[word]

        return variations

    def extract_key_phrases(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Извлечение ключевых фраз"""
        # Простое извлечение биграмм и триграмм
        words = self._extract_words(text)

        phrases = []

        # Биграммы
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            phrases.append(phrase)

        # Триграммы
        for i in range(len(words) - 2):
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            phrases.append(phrase)

        # Подсчитываем частоту
        phrase_freq = Counter(phrases)

        return phrase_freq.most_common(top_n)

    def detect_document_language(self, text: str) -> str:
        """Определение языка документа"""
        # Простая эвристика на основе алфавита
        cyrillic_count = len(re.findall(r'[а-яё]', text.lower()))
        latin_count = len(re.findall(r'[a-z]', text.lower()))

        total_letters = cyrillic_count + latin_count
        if total_letters == 0:
            return "unknown"

        cyrillic_ratio = cyrillic_count / total_letters

        if cyrillic_ratio > 0.7:
            return "ru"
        elif cyrillic_ratio < 0.3:
            return "en"
        else:
            return "mixed"

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Извлечение именованных сущностей"""
        entities = {
            "dates": [],
            "organizations": [],
            "positions": [],
            "numbers": []
        }

        # Даты (простые паттерны)
        date_patterns = [
            r'\d{1,2}\.\d{1,2}\.\d{4}',
            r'\d{1,2}\s+[а-я]+\s+\d{4}',
            r'\d{4}\s*г\.?'
        ]

        for pattern in date_patterns:
            entities["dates"].extend(re.findall(pattern, text, re.IGNORECASE))

        # Организации (простые паттерны)
        org_patterns = [
            r'[А-Я][а-я]+\s+[А-Я][а-я]+\s+[А-Я][а-я]+',  # Три слова с заглавных
            r'ООО\s+"[^"]+"',
            r'ЗАО\s+"[^"]+"',
            r'ОАО\s+"[^"]+"'
        ]

        for pattern in org_patterns:
            entities["organizations"].extend(re.findall(pattern, text))

        # Должности
        position_keywords = [
            "директор", "менеджер", "специалист", "инженер", "бухгалтер",
            "секретарь", "администратор", "консультант", "аналитик"
        ]

        for keyword in position_keywords:
            pattern = rf'\b[а-я]*\s*{keyword}[а-я]*\b'
            matches = re.findall(pattern, text.lower())
            entities["positions"].extend(matches)

        # Числа
        entities["numbers"] = re.findall(r'\b\d+(?:\.\d+)?\b', text)

        return entities

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Анализ тональности текста"""
        # Простой анализ на основе словарей
        positive_words = {
            "хорошо", "отлично", "успешно", "эффективно", "качественно",
            "положительно", "улучшение", "развитие", "достижение"
        }

        negative_words = {
            "плохо", "неудовлетворительно", "проблема", "ошибка", "недостаток",
            "нарушение", "отрицательно", "ухудшение", "снижение"
        }

        words = self._extract_words(text)

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

        positive_score = positive_count / total_sentiment_words
        negative_score = negative_count / total_sentiment_words
        neutral_score = 1.0 - positive_score - negative_score

        return {
            "positive": positive_score,
            "negative": negative_score,
            "neutral": max(neutral_score, 0.0)
        }