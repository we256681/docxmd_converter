#!/usr/bin/env python3
"""
Интеллектуальный процессор документов с расширенными возможностями
Включает машинное обучение, NLP-анализ и продвинутую обработку
"""

import hashlib
import json
import os
import re
import statistics
import time
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .models import DocumentFeatures, ProcessingMetrics, QualityAssessment, ProcessingResult
from .nlp_analyzer import NLPAnalyzer
from .quality_assessor import IntelligentQualityAssessor


class IntelligentProcessor:
    """Интеллектуальный процессор документов"""

    def __init__(self, config_path: str = None):
        # Определяем базовую директорию относительно текущего файла
        current_file = Path(__file__).resolve()
        self.base_dir = current_file.parent.parent.parent
        self.conversion_dir = self.base_dir / "docs" / "Conversion"

        if config_path is None:
            config_path = str(self.base_dir / "config" / "document_templates.json")

        self.config = self._load_config(config_path)
        self.nlp_analyzer = NLPAnalyzer()
        self.quality_assessor = IntelligentQualityAssessor()

        # История обработки для машинного обучения
        self.processing_history = []

    def _load_config(self, config_path: str) -> Dict:
        """Загрузка конфигурации"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            return {"templates": {}}

    def process_document_intelligently(self, file_path: str) -> Dict[str, Any]:
        """Интеллектуальная обработка документа"""

        start_time = datetime.now()

        try:
            # Читаем файл
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Отделяем метаданные
            if "<!-- METADATA" in content:
                main_content, metadata_part = content.split("<!-- METADATA", 1)
            else:
                main_content = content
                metadata_part = ""

            # Анализируем документ
            features = self.nlp_analyzer.extract_features(main_content)
            entities = self.nlp_analyzer.extract_entities(main_content)
            sentiment = self.nlp_analyzer.analyze_sentiment(main_content)

            # Определяем тип документа
            document_type, confidence = self._intelligent_type_detection(
                main_content, features, entities or {}
            )

            # Извлекаем структурированные данные
            extracted_data = self._extract_structured_data(main_content, document_type)

            # Оцениваем качество
            quality_assessment = self.quality_assessor.assess_quality(
                main_content, features, document_type, extracted_data or {}
            )

            # Применяем интеллектуальные улучшения
            improved_content = self._apply_intelligent_improvements(
                main_content, document_type, quality_assessment, extracted_data or {}
            )

            # Создаем расширенные метаданные
            enhanced_metadata = self._create_enhanced_metadata(
                Path(file_path).name,
                document_type,
                confidence,
                features,
                entities or {},
                sentiment or {},
                quality_assessment,
                extracted_data or {},
            )

            # Сохраняем результат
            final_content = improved_content.strip() + "\n\n" + enhanced_metadata

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)

            processing_time = (datetime.now() - start_time).total_seconds()

            # Сохраняем в историю для обучения
            processing_record = {
                "filename": Path(file_path).name,
                "document_type": document_type,
                "confidence": confidence,
                "features": asdict(features),
                "quality_before": 0,  # Можно добавить оценку до обработки
                "quality_after": quality_assessment.overall_score,
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat(),
            }

            self.processing_history.append(processing_record)

            return {
                "success": True,
                "document_type": document_type,
                "confidence": confidence,
                "features": features,
                "entities": entities or {},
                "sentiment": sentiment or {},
                "quality_assessment": quality_assessment,
                "processing_time": processing_time,
                "improvements_applied": len(quality_assessment.recommendations),
            }

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            return {
                "success": False,
                "error": str(e),
                "processing_time": processing_time,
            }

    def _intelligent_type_detection(
        self, content: str, features: DocumentFeatures, entities: Dict
    ) -> Tuple[str, float]:
        """Интеллектуальное определение типа документа"""

        content_lower = content.lower()

        # Базовые паттерны
        type_scores = {}

        # Должностная инструкция
        job_desc_score = 0
        if "должностн" in content_lower and "инструкци" in content_lower:
            job_desc_score += 20
        if "обязанности" in content_lower:
            job_desc_score += 10
        if "права" in content_lower:
            job_desc_score += 10
        if "ответственность" in content_lower:
            job_desc_score += 10
        if entities.get("positions"):
            job_desc_score += 15

        type_scores["должностная_инструкция"] = job_desc_score

        # Отчет
        report_score = 0
        if "отчет" in content_lower:
            report_score += 20
        if "результат" in content_lower:
            report_score += 10
        if "анализ" in content_lower:
            report_score += 10
        if "вывод" in content_lower:
            report_score += 10
        if entities.get("dates"):
            report_score += 10

        type_scores["отчет"] = report_score

        # Положение
        regulation_score = 0
        if "положени" in content_lower:
            regulation_score += 20
        if "общие положения" in content_lower:
            regulation_score += 15
        if "цели" in content_lower and "задачи" in content_lower:
            regulation_score += 10

        type_scores["положение"] = regulation_score

        # Инструкция
        instruction_score = 0
        if "инструкци" in content_lower and "должностн" not in content_lower:
            instruction_score += 20
        if "порядок" in content_lower:
            instruction_score += 10
        if "алгоритм" in content_lower:
            instruction_score += 10
        if features.list_count > 5:  # Много списков - признак инструкции
            instruction_score += 10

        type_scores["инструкция"] = instruction_score

        # Определяем лучший тип
        if type_scores:
            best_type = max(type_scores.keys(), key=lambda k: type_scores[k])
            max_score = type_scores[best_type]

            if max_score > 0:
                confidence = min(1.0, max_score / 50.0)
                return best_type, confidence

        return "общий_документ", 0.1

    def _extract_structured_data(
        self, content: str, document_type: str
    ) -> Dict[str, Any]:
        """Извлечение структурированных данных с учетом типа документа"""

        extracted = {}
        content_lower = content.lower()

        # Общие данные
        entities = self.nlp_analyzer.extract_entities(content)
        if entities:
            extracted.update(entities)

        # Специфичные для типа данные
        if document_type == "должностная_инструкция":
            # Извлекаем название должности из заголовка
            title_match = re.search(
                r"#\s*(?:должностная\s+инструкция[:\s]*)?(.+)", content, re.IGNORECASE
            )
            if title_match:
                extracted["position"] = title_match.group(1).strip()

            # Извлекаем функции
            functions_match = re.search(
                r"функции[:\s]*(.*?)(?=\n\n|\n##|$)", content_lower, re.DOTALL
            )
            if functions_match:
                extracted["functions"] = functions_match.group(1).strip()

        elif document_type == "отчет":
            # Извлекаем период отчета
            period_patterns = [
                r"за\s+(\d{4})\s+год",
                r"за\s+(\w+\s+\d{4})",
                r"период[:\s]*(.+?)(?=\n|$)",
            ]

            for pattern in period_patterns:
                match = re.search(pattern, content_lower)
                if match:
                    extracted["report_period"] = match.group(1).strip()
                    break

        return extracted

    def _apply_intelligent_improvements(
        self,
        content: str,
        document_type: str,
        quality_assessment: QualityAssessment,
        extracted_data: Dict,
    ) -> str:
        """Применение интеллектуальных улучшений"""

        improved = content

        # Исправляем критические проблемы
        for issue in quality_assessment.critical_issues:
            if "артефакты" in issue.lower():
                improved = self._remove_artifacts(improved)
            elif "заголовки" in issue.lower():
                improved = self._add_missing_headers(improved, document_type)
            elif "незаполненные разделы" in issue.lower():
                improved = self._fill_empty_sections(
                    improved, document_type, extracted_data
                )

        # Применяем рекомендации
        for recommendation in quality_assessment.recommendations:
            if "форматирование" in recommendation.lower():
                improved = self._improve_formatting(improved)
            elif "структуру" in recommendation.lower():
                improved = self._improve_structure(improved, document_type)
            elif "согласованность" in recommendation.lower():
                improved = self._improve_consistency(improved)

        return improved

    def _remove_artifacts(self, content: str) -> str:
        """Удаление артефактов"""

        # Удаляем различные артефакты
        content = re.sub(r"::: \{[^}]*\}", "", content)
        content = re.sub(r":::", "", content)
        content = re.sub(r"_{5,}", "", content)
        content = re.sub(r"\*{3,}", "", content)
        content = re.sub(r"_Toc\d+|_Ref\d+", "", content)

        # Очищаем лишние пустые строки
        content = re.sub(r"\n{3,}", "\n\n", content)

        return content

    def _add_missing_headers(self, content: str, document_type: str) -> str:
        """Добавление недостающих заголовков"""

        if document_type == "должностная_инструкция":
            # Проверяем наличие основных разделов
            required_headers = [
                "## 1. Общие положения",
                "## 2. Функции",
                "## 3. Должностные обязанности",
                "## 4. Права",
                "## 5. Ответственность",
            ]

            for header in required_headers:
                if header.lower() not in content.lower():
                    # Добавляем заголовок в конец
                    content += f"\n\n{header}\n\n_{header[3:]} требует заполнения_"

        return content

    def _fill_empty_sections(
        self, content: str, document_type: str, extracted_data: Dict
    ) -> str:
        """Заполнение пустых разделов"""

        # Заменяем заглушки на основе извлеченных данных
        if "position" in extracted_data:
            position = extracted_data["position"]
            content = content.replace(
                "_Общие положения требует заполнения_",
                f"{position} относится к категории специалистов и подчиняется непосредственному руководителю.",
            )

        if "functions" in extracted_data:
            functions = extracted_data["functions"]
            content = content.replace(
                "_Функции требует заполнения_", f"Основные функции:\n{functions}"
            )

        return content

    def _improve_formatting(self, content: str) -> str:
        """Улучшение форматирования"""

        # Исправляем заголовки
        content = re.sub(r"^##([^\s#])", r"## \1", content, flags=re.MULTILINE)
        content = re.sub(r"^###([^\s#])", r"### \1", content, flags=re.MULTILINE)

        # Исправляем списки
        content = re.sub(r"^(\s*)([•·▪▫])\s*", r"\1- ", content, flags=re.MULTILINE)

        # Удаляем лишние пробелы
        content = re.sub(r" +$", "", content, flags=re.MULTILINE)
        content = re.sub(r" {2,}", " ", content)

        return content

    def _improve_structure(self, content: str, document_type: str) -> str:
        """Улучшение структуры"""

        # Добавляем содержание если его нет
        if "## Содержание" not in content and content.count("##") > 3:
            headers = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
            if headers:
                toc = "## Содержание\n\n"
                for i, header in enumerate(headers, 1):
                    toc += f"{i}. {header}\n"
                toc += "\n"

                # Вставляем после заголовка документа
                content = re.sub(
                    r"(^#\s+.+\n\n)", r"\1" + toc, content, flags=re.MULTILINE
                )

        return content

    def _improve_consistency(self, content: str) -> str:
        """Улучшение согласованности"""

        # Исправляем нумерацию
        lines = content.split("\n")
        in_numbered_section = False
        current_section = 0
        item_counter = 1

        for i, line in enumerate(lines):
            if re.match(r"^##\s+\d+\.", line):
                in_numbered_section = True
                current_section += 1
                item_counter = 1
            elif line.startswith("##"):
                in_numbered_section = False
            elif in_numbered_section and re.match(r"^\d+\.", line.strip()):
                # Исправляем нумерацию
                lines[i] = re.sub(
                    r"^\d+\.", f"{current_section}.{item_counter}.", line.strip()
                )
                item_counter += 1

        return "\n".join(lines)

    def _create_enhanced_metadata(
        self,
        filename: str,
        document_type: str,
        confidence: float,
        features: DocumentFeatures,
        entities: Dict,
        sentiment: Dict,
        quality_assessment: QualityAssessment,
        extracted_data: Dict,
    ) -> str:
        """Создание расширенных метаданных"""

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        metadata = {
            "created_at": now,
            "updated_at": now,
            "author": "intelligent_processor",
            "version": "6.0.0",
            "filename": filename,
            # Анализ документа
            "document_analysis": {
                "type": document_type,
                "type_confidence": round(confidence, 3),
                "features": asdict(features),
                "entities": entities,
                "sentiment": sentiment,
            },
            # Оценка качества
            "quality_assessment": {
                "overall_score": round(quality_assessment.overall_score, 1),
                "structure_score": round(quality_assessment.structure_score, 1),
                "content_score": round(quality_assessment.content_score, 1),
                "formatting_score": round(quality_assessment.formatting_score, 1),
                "completeness_score": round(quality_assessment.completeness_score, 1),
                "consistency_score": round(quality_assessment.consistency_score, 1),
                "recommendations_count": len(quality_assessment.recommendations),
                "critical_issues_count": len(quality_assessment.critical_issues),
            },
            # Извлеченные данные
            "extracted_data": extracted_data,
            # Метаданные обработки
            "processing_metadata": {
                "method": "intelligent_nlp_processing",
                "ai_enhanced": True,
                "quality_assured": True,
                "machine_learning_ready": True,
            },
        }

        return (
            f"<!-- METADATA\n{json.dumps(metadata, indent=2, ensure_ascii=False)}\n-->"
        )

    def process_all_documents(self) -> Dict[str, Any]:
        """Обработка всех документов с интеллектуальным анализом"""

        print("🧠 Интеллектуальная обработка документов")
        print("=" * 60)

        md_files = list(self.conversion_dir.glob("**/*.md"))

        if not md_files:
            print("❌ Файлы MD не найдены")
            return {}

        print(f"📁 Найдено файлов: {len(md_files)}")

        results = []
        total_processing_time = 0

        for md_file in md_files:
            print(f"\n🔄 Интеллектуальная обработка: {md_file.name}")

            result = self.process_document_intelligently(str(md_file))
            results.append(result)

            if result["success"]:
                print(
                    f"   🧠 Тип: {result['document_type']} (уверенность: {result['confidence']:.2f})"
                )
                print(
                    f"   📊 Качество: {result['quality_assessment'].overall_score:.1f}/100"
                )
                print(f"   🔧 Улучшений: {result['improvements_applied']}")
                print(f"   ⏱️  Время: {result['processing_time']:.2f}с")
                total_processing_time += result["processing_time"]
            else:
                print(f"   ❌ Ошибка: {result['error']}")

        # Анализ результатов
        successful_results = [r for r in results if r["success"]]
        avg_quality = 0
        avg_confidence = 0

        if successful_results:
            avg_quality = statistics.mean(
                r["quality_assessment"].overall_score for r in successful_results
            )
            avg_confidence = statistics.mean(
                r["confidence"] for r in successful_results
            )

            print(f"\n📈 ИНТЕЛЛЕКТУАЛЬНАЯ СТАТИСТИКА:")
            print("=" * 60)
            print(f"✅ Успешно обработано: {len(successful_results)}")
            print(f"📊 Средняя оценка качества: {avg_quality:.1f}/100")
            print(f"🎯 Средняя уверенность в типе: {avg_confidence:.2f}")
            print(f"⏱️  Общее время обработки: {total_processing_time:.2f}с")

            # Статистика по типам документов
            type_counts = Counter(r["document_type"] for r in successful_results)
            print(f"\n📋 Распределение по типам:")
            for doc_type, count in type_counts.items():
                print(f"   - {doc_type}: {count}")

            # Анализ качества
            quality_distribution = {
                "excellent": len(
                    [
                        r
                        for r in successful_results
                        if r["quality_assessment"].overall_score >= 90
                    ]
                ),
                "high": len(
                    [
                        r
                        for r in successful_results
                        if 80 <= r["quality_assessment"].overall_score < 90
                    ]
                ),
                "medium": len(
                    [
                        r
                        for r in successful_results
                        if 70 <= r["quality_assessment"].overall_score < 80
                    ]
                ),
                "low": len(
                    [
                        r
                        for r in successful_results
                        if r["quality_assessment"].overall_score < 70
                    ]
                ),
            }

            print(f"\n🏆 Распределение качества:")
            print(f"   🥇 Отличное (90+): {quality_distribution['excellent']}")
            print(f"   🥈 Высокое (80-89): {quality_distribution['high']}")
            print(f"   🥉 Среднее (70-79): {quality_distribution['medium']}")
            print(f"   ⚠️  Низкое (<70): {quality_distribution['low']}")

        # Сохраняем историю обработки
        self._save_processing_history()

        return {
            "total_files": len(md_files),
            "successful": len(successful_results),
            "failed": len(results) - len(successful_results),
            "avg_quality": avg_quality,
            "avg_confidence": avg_confidence,
            "total_time": total_processing_time,
            "results": results,
        }

    def _save_processing_history(self):
        """Сохранение истории обработки для машинного обучения"""

        history_file = self.base_dir / "data" / "processing_history.json"

        try:
            # Загружаем существующую историю
            if history_file.exists():
                with open(history_file, "r", encoding="utf-8") as f:
                    existing_history = json.load(f)
            else:
                existing_history = []

            # Добавляем новые записи
            existing_history.extend(self.processing_history)

            # Сохраняем обновленную историю
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(existing_history, f, indent=2, ensure_ascii=False)

            print(
                f"\n💾 История обработки сохранена: {len(self.processing_history)} новых записей"
            )

        except Exception as e:
            print(f"⚠️  Ошибка сохранения истории: {e}")

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Получение статистики обработки"""

        if not self.processing_history:
            return {"message": "История обработки пуста"}

        total_files = len(self.processing_history)
        avg_processing_time = sum(r['processing_time'] for r in self.processing_history) / total_files
        avg_quality = sum(r['quality_after'] for r in self.processing_history) / total_files

        document_types = {}
        for record in self.processing_history:
            doc_type = record['document_type']
            if doc_type not in document_types:
                document_types[doc_type] = 0
            document_types[doc_type] += 1

        return {
            'total_files_processed': total_files,
            'average_processing_time': avg_processing_time,
            'average_quality_score': avg_quality,
            'document_types_distribution': document_types,
            'last_processed': self.processing_history[-1]['timestamp'] if self.processing_history else None
        }


def main():
    """Основная функция"""
    processor = IntelligentProcessor()
    results = processor.process_all_documents()

    print(f"\n🎉 Интеллектуальная обработка завершена!")
    print(f"📁 Результаты сохранены в: {processor.conversion_dir}")


if __name__ == "__main__":
    main()
