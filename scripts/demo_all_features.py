#!/usr/bin/env python3
"""
Демонстрация всех возможностей универсального процессора документов
Показывает работу всех созданных компонентов
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Добавляем путь к src для импортов
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.content_analyzers import ContentProcessor, SmartContentExtractor
from docxmd_converter.intelligent_processor import (
    IntelligentProcessor,
    IntelligentQualityAssessor,
    NLPAnalyzer,
)


class FeatureDemo:
    """Демонстрация возможностей системы"""

    def __init__(self):
        self.base_dir = Path("/home/uduntu33/Документы/PROJECT/docxmd_converter")
        self.conversion_dir = self.base_dir / "docs" / "Conversion"

        # Инициализируем все процессоры
        self.intelligent_processor = IntelligentProcessor()
        self.content_processor = ContentProcessor()
        self.nlp_analyzer = NLPAnalyzer()
        self.quality_assessor = IntelligentQualityAssessor()
        self.content_extractor = SmartContentExtractor()

        print("🚀 Инициализация демонстрации возможностей")
        print("=" * 60)

    def demo_nlp_analysis(self):
        """Демонстрация NLP анализа"""

        print("\n🧠 ДЕМОНСТРАЦИЯ NLP АНАЛИЗА")
        print("-" * 40)

        # Берем один из файлов для анализа
        sample_file = self.conversion_dir / "Архивист.md"

        if not sample_file.exists():
            print("❌ Файл для демонстрации не найден")
            return

        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Отделяем основной контент от метаданных
        if "<!-- METADATA" in content:
            main_content = content.split("<!-- METADATA")[0]
        else:
            main_content = content

        print(f"📄 Анализируем файл: {sample_file.name}")

        # 1. Извлечение признаков
        print("\n1️⃣ Извлечение признаков документа:")
        features = self.nlp_analyzer.extract_features(main_content)

        print(f"   📊 Количество слов: {features.word_count}")
        print(f"   📝 Количество предложений: {features.sentence_count}")
        print(f"   📋 Количество параграфов: {features.paragraph_count}")
        print(f"   🏷️  Количество заголовков: {features.heading_count}")
        print(f"   📃 Количество списков: {features.list_count}")
        print(f"   📊 Средняя длина предложения: {features.avg_sentence_length:.1f}")
        print(f"   🎯 Богатство словаря: {features.vocabulary_richness:.3f}")
        print(f"   🏗️  Сложность структуры: {features.structure_complexity:.2f}")
        print(f"   🎩 Формальность: {features.formality_score:.3f}")

        # 2. Извлечение сущностей
        print("\n2️⃣ Извлечение именованных сущностей:")
        entities = self.nlp_analyzer.extract_entities(main_content)

        for entity_type, entity_list in entities.items():
            if entity_list:
                print(
                    f"   {entity_type}: {', '.join(entity_list[:3])}{'...' if len(entity_list) > 3 else ''}"
                )

        # 3. Анализ тональности
        print("\n3️⃣ Анализ тональности:")
        sentiment = self.nlp_analyzer.analyze_sentiment(main_content)

        print(f"   😊 Позитивная: {sentiment['positive']:.3f}")
        print(f"   😐 Нейтральная: {sentiment['neutral']:.3f}")
        print(f"   😞 Негативная: {sentiment['negative']:.3f}")

    def demo_quality_assessment(self):
        """Демонстрация оценки качества"""

        print("\n📊 ДЕМОНСТРАЦИЯ ОЦЕНКИ КАЧЕСТВА")
        print("-" * 40)

        sample_file = self.conversion_dir / "Архивист.md"

        if not sample_file.exists():
            print("❌ Файл для демонстрации не найден")
            return

        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "<!-- METADATA" in content:
            main_content = content.split("<!-- METADATA")[0]
        else:
            main_content = content

        print(f"📄 Оцениваем качество: {sample_file.name}")

        # Оценка качества
        quality = self.quality_assessor.assess_quality(
            main_content, "должностная_инструкция", {}
        )

        print(f"\n🏆 ОБЩАЯ ОЦЕНКА: {quality.overall_score:.1f}/100")
        print(f"   🏗️  Структура: {quality.structure_score:.1f}/100")
        print(f"   📝 Содержание: {quality.content_score:.1f}/100")
        print(f"   🎨 Форматирование: {quality.formatting_score:.1f}/100")
        print(f"   ✅ Полнота: {quality.completeness_score:.1f}/100")
        print(f"   🔄 Согласованность: {quality.consistency_score:.1f}/100")

        if quality.recommendations:
            print(f"\n💡 Рекомендации по улучшению:")
            for i, rec in enumerate(quality.recommendations, 1):
                print(f"   {i}. {rec}")

        if quality.critical_issues:
            print(f"\n⚠️  Критические проблемы:")
            for i, issue in enumerate(quality.critical_issues, 1):
                print(f"   {i}. {issue}")

    def demo_content_analysis(self):
        """Демонстрация анализа контента"""

        print("\n🔍 ДЕМОНСТРАЦИЯ АНАЛИЗА КОНТЕНТА")
        print("-" * 40)

        sample_file = self.conversion_dir / "Архивист.md"

        if not sample_file.exists():
            print("❌ Файл для демонстрации не найден")
            return

        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "<!-- METADATA" in content:
            main_content = content.split("<!-- METADATA")[0]
        else:
            main_content = content

        print(f"📄 Анализируем контент: {sample_file.name}")

        # Обработка контента
        cleaned_content, analysis_results = self.content_processor.process_content(
            main_content
        )

        print(f"\n📋 Результаты анализа:")
        for analyzer_name, elements in analysis_results.items():
            if elements:
                print(f"   {analyzer_name.title()}: найдено {len(elements)} элементов")

                # Показываем первые несколько элементов
                for i, element in enumerate(elements[:2]):
                    print(
                        f"     - {element.type} (уровень {element.level}): {element.content[:50]}..."
                    )

        # Умное извлечение контента
        print(f"\n🧠 Умное извлечение структурированного контента:")
        structured = self.content_extractor.extract_structured_content(main_content)

        for section_name, section_content in list(structured.items())[:3]:
            print(f"   📑 {section_name}: {len(section_content)} символов")

    def demo_document_processing(self):
        """Демонстрация обработки документов"""

        print("\n⚙️  ДЕМОНСТРАЦИЯ ОБРАБОТКИ ДОКУМЕНТОВ")
        print("-" * 40)

        # Получаем список файлов
        md_files = list(self.conversion_dir.glob("*.md"))

        if not md_files:
            print("❌ Файлы для демонстрации не найдены")
            return

        print(f"📁 Найдено файлов для обработки: {len(md_files)}")

        # Обрабатываем первые 3 файла для демонстрации
        demo_files = md_files[:3]

        results = []

        for md_file in demo_files:
            print(f"\n🔄 Обработка: {md_file.name}")

            start_time = time.time()

            # Интеллектуальная обработка
            result = self.intelligent_processor.process_document_intelligently(md_file)

            processing_time = time.time() - start_time

            if result["success"]:
                print(f"   ✅ Успешно обработан")
                print(f"   🧠 Тип: {result['document_type']}")
                print(f"   🎯 Уверенность: {result['confidence']:.2f}")
                print(
                    f"   📊 Качество: {result['quality_assessment'].overall_score:.1f}/100"
                )
                print(f"   🔧 Улучшений: {result['improvements_applied']}")
                print(f"   ⏱️  Время: {processing_time:.3f}с")

                results.append(result)
            else:
                print(f"   ❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")

        # Статистика
        if results:
            avg_quality = sum(
                r["quality_assessment"].overall_score for r in results
            ) / len(results)
            avg_confidence = sum(r["confidence"] for r in results) / len(results)
            total_improvements = sum(r["improvements_applied"] for r in results)

            print(f"\n📈 СТАТИСТИКА ДЕМОНСТРАЦИИ:")
            print(f"   ✅ Успешно обработано: {len(results)}")
            print(f"   📊 Средняя оценка качества: {avg_quality:.1f}/100")
            print(f"   🎯 Средняя уверенность: {avg_confidence:.2f}")
            print(f"   🔧 Всего улучшений: {total_improvements}")

    def demo_template_system(self):
        """Демонстрация системы шаблонов"""

        print("\n📋 ДЕМОНСТРАЦИЯ СИСТЕМЫ ШАБЛОНОВ")
        print("-" * 40)

        # Загружаем конфигурацию шаблонов
        config_path = self.base_dir / "document_templates.json"

        if not config_path.exists():
            print("❌ Конфигурация шаблонов не найдена")
            return

        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        templates = config.get("templates", {})

        print(f"📚 Доступно шаблонов: {len(templates)}")

        for template_id, template_data in templates.items():
            print(f"\n📄 {template_data['name']} ({template_id})")
            print(f"   📝 Описание: {template_data.get('description', 'Нет описания')}")
            print(f"   📋 Разделов: {len(template_data.get('sections', []))}")
            print(
                f"   ✅ Обязательных: {len(template_data.get('required_sections', []))}"
            )
            print(
                f"   🔍 Ключевых слов: {len(template_data.get('detection_keywords', []))}"
            )
            print(
                f"   🎨 Нумерация: {template_data.get('numbering_pattern', 'не указана')}"
            )

        # Демонстрация правил очистки
        cleaning_rules = config.get("cleaning_rules", {})
        global_rules = cleaning_rules.get("global", [])
        specific_rules = cleaning_rules.get("document_specific", {})

        print(f"\n🧹 ПРАВИЛА ОЧИСТКИ:")
        print(f"   🌐 Глобальных правил: {len(global_rules)}")
        print(f"   🎯 Специфичных правил: {len(specific_rules)}")

        for rule in global_rules[:3]:  # Показываем первые 3
            print(f"     - {rule['name']}: {rule['description']}")

    def demo_performance_metrics(self):
        """Демонстрация метрик производительности"""

        print("\n⚡ ДЕМОНСТРАЦИЯ МЕТРИК ПРОИЗВОДИТЕЛЬНОСТИ")
        print("-" * 40)

        # Загружаем историю обработки
        history_file = self.base_dir / "processing_history.json"

        if not history_file.exists():
            print("❌ История обработки не найдена")
            return

        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)

        if not history:
            print("❌ История обработки пуста")
            return

        print(f"📊 Записей в истории: {len(history)}")

        # Анализ производительности
        processing_times = [record["processing_time"] for record in history]
        quality_scores = [record["quality_after"] for record in history]

        avg_time = sum(processing_times) / len(processing_times)
        min_time = min(processing_times)
        max_time = max(processing_times)

        avg_quality = sum(quality_scores) / len(quality_scores)
        min_quality = min(quality_scores)
        max_quality = max(quality_scores)

        print(f"\n⏱️  ВРЕМЯ ОБРАБОТКИ:")
        print(f"   Среднее: {avg_time:.3f}с")
        print(f"   Минимальное: {min_time:.3f}с")
        print(f"   Максимальное: {max_time:.3f}с")

        print(f"\n📊 КАЧЕСТВО ОБРАБОТКИ:")
        print(f"   Среднее: {avg_quality:.1f}/100")
        print(f"   Минимальное: {min_quality:.1f}/100")
        print(f"   Максимальное: {max_quality:.1f}/100")

        # Статистика по типам документов
        doc_types = {}
        for record in history:
            doc_type = record["document_type"]
            if doc_type not in doc_types:
                doc_types[doc_type] = {"count": 0, "avg_quality": 0, "avg_time": 0}

            doc_types[doc_type]["count"] += 1
            doc_types[doc_type]["avg_quality"] += record["quality_after"]
            doc_types[doc_type]["avg_time"] += record["processing_time"]

        # Вычисляем средние значения
        for doc_type, stats in doc_types.items():
            stats["avg_quality"] /= stats["count"]
            stats["avg_time"] /= stats["count"]

        print(f"\n📋 СТАТИСТИКА ПО ТИПАМ ДОКУМЕНТОВ:")
        for doc_type, stats in doc_types.items():
            print(f"   {doc_type}:")
            print(f"     Количество: {stats['count']}")
            print(f"     Ср. качество: {stats['avg_quality']:.1f}/100")
            print(f"     Ср. время: {stats['avg_time']:.3f}с")

    def demo_comparison(self):
        """Демонстрация сравнения разных процессоров"""

        print("\n🔄 ДЕМОНСТРАЦИЯ СРАВНЕНИЯ ПРОЦЕССОРОВ")
        print("-" * 40)

        sample_file = self.conversion_dir / "Архивист.md"

        if not sample_file.exists():
            print("❌ Файл для демонстрации не найден")
            return

        print(f"📄 Сравниваем обработку файла: {sample_file.name}")

        # Создаем копию файла для тестирования
        test_file = self.base_dir / "temp_test.md"

        with open(sample_file, "r", encoding="utf-8") as src:
            with open(test_file, "w", encoding="utf-8") as dst:
                dst.write(src.read())

        processors = [
            ("Улучшенный процессор", self.enhanced_processor),
            ("Интеллектуальный процессор", self.intelligent_processor),
        ]

        results = {}

        for name, processor in processors:
            print(f"\n🔄 Тестируем: {name}")

            start_time = time.time()

            try:
                if name == "Улучшенный процессор":
                    result = processor.process_single_document(test_file)
                    processing_time = time.time() - start_time

                    results[name] = {
                        "success": result.success,
                        "quality_score": result.quality_score,
                        "document_type": result.document_type,
                        "processing_time": processing_time,
                        "issues": len(result.issues),
                        "improvements": len(result.improvements),
                    }
                else:
                    result = processor.process_document_intelligently(test_file)
                    processing_time = time.time() - start_time

                    results[name] = {
                        "success": result["success"],
                        "quality_score": (
                            result["quality_assessment"].overall_score
                            if result["success"]
                            else 0
                        ),
                        "document_type": (
                            result["document_type"] if result["success"] else "unknown"
                        ),
                        "processing_time": processing_time,
                        "issues": (
                            len(result["quality_assessment"].critical_issues)
                            if result["success"]
                            else 0
                        ),
                        "improvements": (
                            result["improvements_applied"] if result["success"] else 0
                        ),
                    }

                print(f"   ✅ Успешно")
                print(f"   📊 Качество: {results[name]['quality_score']:.1f}/100")
                print(f"   ⏱️  Время: {results[name]['processing_time']:.3f}с")

            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                results[name] = {"success": False, "error": str(e)}

        # Сравнение результатов
        print(f"\n📊 СРАВНЕНИЕ РЕЗУЛЬТАТОВ:")
        print(f"{'Процессор':<25} {'Качество':<10} {'Время':<10} {'Улучшения':<12}")
        print("-" * 60)

        for name, result in results.items():
            if result["success"]:
                print(
                    f"{name:<25} {result['quality_score']:<10.1f} {result['processing_time']:<10.3f} {result['improvements']:<12}"
                )
            else:
                print(f"{name:<25} {'ОШИБКА':<10} {'-':<10} {'-':<12}")

        # Удаляем временный файл
        if test_file.exists():
            test_file.unlink()

    def run_full_demo(self):
        """Запуск полной демонстрации"""

        print("🎭 ПОЛНАЯ ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ")
        print("=" * 60)
        print("Демонстрируем все возможности универсального процессора документов")

        demos = [
            ("NLP Анализ", self.demo_nlp_analysis),
            ("Оценка качества", self.demo_quality_assessment),
            ("Анализ контента", self.demo_content_analysis),
            ("Обработка документов", self.demo_document_processing),
            ("Система шаблонов", self.demo_template_system),
            ("Метрики производительности", self.demo_performance_metrics),
            ("Сравнение процессоров", self.demo_comparison),
        ]

        for demo_name, demo_func in demos:
            try:
                demo_func()
                time.sleep(1)  # Небольшая пауза между демонстрациями
            except Exception as e:
                print(f"\n❌ Ошибка в демонстрации '{demo_name}': {e}")

        print(f"\n🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
        print("=" * 60)
        print("Все возможности системы продемонстрированы.")
        print("Система готова к использованию в производственной среде.")


def main():
    """Основная функция"""

    demo = FeatureDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
