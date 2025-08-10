"""
Основной пакет DocxMD Converter
"""

from .intelligent_processor import IntelligentProcessor
from .core import DocxMdConverter
from .nlp_analyzer import NLPAnalyzer
from .quality_assessor import IntelligentQualityAssessor
from .models import DocumentFeatures, ProcessingResult, QualityAssessment

__all__ = [
    'IntelligentProcessor',
    'DocxMdConverter',
    'NLPAnalyzer',
    'IntelligentQualityAssessor',
    'DocumentFeatures',
    'ProcessingResult',
    'QualityAssessment',
]