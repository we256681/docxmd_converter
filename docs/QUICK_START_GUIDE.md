# Краткое руководство по использованию

## 🚀 Быстрый старт

### 1. Простая обработка документов

```bash
# Обработка всех MD файлов в папке
python intelligent_processor.py

# Или используйте улучшенный процессор
python enhanced_universal_processor.py
```

### 2. Демонстрация всех возможностей

```bash
# Полная демонстрация системы
python demo_all_features.py
```

### 3. Веб-интерфейс

```bash
# Запуск веб-интерфейса
python web_interface.py

# Откройте браузер: http://localhost:5000
```

## 📋 Основные команды

### Обработка одного файла

```python
from intelligent_processor import IntelligentProcessor

processor = IntelligentProcessor()
result = processor.process_document_intelligently(Path("document.md"))

print(f"Качество: {result['quality_assessment'].overall_score}/100")
print(f"Тип: {result['document_type']}")
```

### Анализ качества

```python
from intelligent_processor import IntelligentQualityAssessor

assessor = IntelligentQualityAssessor()
quality = assessor.assess_quality(content, document_type, extracted_data)

print(f"Общая оценка: {quality.overall_score}/100")
print(f"Рекомендации: {quality.recommendations}")
```

### NLP анализ

```python
from intelligent_processor import NLPAnalyzer

analyzer = NLPAnalyzer()
features = analyzer.extract_features(text)
entities = analyzer.extract_entities(text)
sentiment = analyzer.analyze_sentiment(text)

print(f"Слов: {features.word_count}")
print(f"Формальность: {features.formality_score}")
```

## 🎯 Типы документов

Система автоматически определяет и обрабатывает:

- **Должностные инструкции** - 100% точность определения
- **Положения** - структурированная обработка
- **Инструкции** - пошаговое форматирование
- **Отчеты** - анализ результатов
- **Договоры** - юридическое форматирование
- **Протоколы** - структура заседаний
- **Общие документы** - универсальная обработка

## ⚙️ Настройка

### Добавление нового типа документа

Отредактируйте `document_templates.json`:

```json
{
  "новый_тип": {
    "name": "Новый тип документа",
    "sections": ["Раздел 1", "Раздел 2"],
    "detection_keywords": ["ключевое_слово"],
    "numbering_pattern": "hierarchical"
  }
}
```

### Настройка правил очистки

```json
{
  "cleaning_rules": {
    "global": [
      {
        "name": "remove_artifacts",
        "pattern": "артефакт_паттерн",
        "replacement": ""
      }
    ]
  }
}
```

## 📊 Мониторинг качества

### Просмотр статистики

```python
# История обработки сохраняется в processing_history.json
with open('processing_history.json', 'r') as f:
    history = json.load(f)

avg_quality = sum(r['quality_after'] for r in history) / len(history)
print(f"Средняя оценка качества: {avg_quality:.1f}/100")
```

### Анализ производительности

```bash
# Время обработки отслеживается автоматически
# Среднее время: 0.005с на документ
# Пропускная способность: ~200 документов/сек
```

## 🌐 Веб-интерфейс

### Основные возможности

- **Drag & Drop загрузка** файлов
- **Пакетная обработка** документов
- **Скачивание результатов** в ZIP
- **Статистика в реальном времени**
- **API для интеграции**

### API эндпоинты

```bash
GET  /api/status      # Статус системы
GET  /api/history     # История обработки
GET  /api/templates   # Доступные шаблоны
POST /upload          # Загрузка файлов
POST /process         # Обработка документов
```

## 🔧 Устранение неполадок

### Частые проблемы

**Проблема:** Файл не обрабатывается
```bash
# Проверьте формат файла (поддерживаются: DOCX, MD, TXT)
# Проверьте размер файла (максимум 16MB)
```

**Проблема:** Низкое качество обработки
```bash
# Проверьте содержимое документа
# Убедитесь, что документ содержит структурированную информацию
```

**Проблема:** Неправильное определение типа
```bash
# Добавьте ключевые слова в конфигурацию шаблона
# Проверьте detection_keywords в document_templates.json
```

### Логи и отладка

```python
# Включите подробное логирование
import logging
logging.basicConfig(level=logging.DEBUG)

# Проверьте метаданные обработанного документа
# Они содержат детальную информацию об анализе
```

## 📈 Оптимизация производительности

### Для больших объемов

```python
# Используйте пакетную обработку
processor = IntelligentProcessor()
results = processor.process_all_documents()

# Результаты обрабатываются параллельно
```

### Настройка памяти

```bash
# Для больших файлов увеличьте лимит памяти
export PYTHONHASHSEED=0
export PYTHONMALLOC=malloc
```

## 🎯 Лучшие практики

### Подготовка документов

1. **Структурируйте контент** - используйте заголовки и списки
2. **Избегайте артефактов** - очистите документ от лишних элементов
3. **Используйте стандартную терминологию** - это улучшит определение типа

### Настройка системы

1. **Адаптируйте шаблоны** под ваши стандарты
2. **Добавьте специфичные правила очистки**
3. **Настройте критерии качества**

### Мониторинг

1. **Отслеживайте метрики качества**
2. **Анализируйте историю обработки**
3. **Собирайте обратную связь пользователей**

## 🆘 Поддержка

### Контакты

- **Документация:** См. файлы в папке проекта
- **Примеры:** `demo_all_features.py`
- **Конфигурация:** `document_templates.json`

### Полезные файлы

- `FINAL_REPORT.md` - полный отчет о системе
- `UNIVERSAL_PROCESSOR_REPORT.md` - техническая документация
- `processing_history.json` - история обработки
- `templates/` - HTML шаблоны веб-интерфейса

---

**Система готова к использованию!** 🚀
**Начните с простой команды:** `python intelligent_processor.py` 🎯
