#!/usr/bin/env python3
"""
Модели данных для системы обработки документов
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentFeatures:
    """Признаки документа для анализа"""

    word_count: int
    sentence_count: int
    paragraph_count: int
    heading_count: int
    list_count: int
    table_count: int
    avg_sentence_length: float
    vocabulary_richness: float
    structure_complexity: float
    formality_score: float


@dataclass
class ProcessingMetrics:
    """Метрики обработки документа"""

    processing_time: float
    memory_usage: float
    quality_score: float
    confidence_level: float
    issues_found: List[str]


@dataclass
class QualityAssessment:
    """Результат оценки качества документа"""

    overall_score: float
    structure_score: float
    content_score: float
    consistency_score: float
    completeness_score: float
    formatting_score: float
    issues: List[str]
    recommendations: List[str]
    critical_issues: List[str]


@dataclass
class ProcessingResult:
    """Результат обработки документа"""

    success: bool
    input_file: str
    output_file: Optional[str]
    document_type: str
    features: DocumentFeatures
    quality: QualityAssessment
    metrics: ProcessingMetrics
    extracted_data: Dict[str, Any]
    timestamp: str