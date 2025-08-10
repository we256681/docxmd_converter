# 🚀 DocxMD Converter v3.1.0

> Интеллектуальная система конвертации и обработки документов с NLP-анализом

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/docxmd-converter.svg)](https://pypi.org/project/docxmd-converter/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

## ✨ Особенности

- 🧠 **Интеллектуальная обработка** с машинным обучением
- 📊 **NLP-анализ** текста и структуры документов
- 🎯 **Автоматическое определение** типа документа
- 📈 **Оценка качества** с детальными рекомендациями
- 🌐 **Множественные интерфейсы**: CLI, GUI, Web
- 📁 **Пакетная обработка** документов
- 📊 **Статистика и отчеты** обработки

## 🚀 Установка

```bash
pip install docxmd-converter
```

### Дополнительные возможности

```bash
# С поддержкой NLP
pip install docxmd-converter[nlp]

# Для разработки
pip install docxmd-converter[dev]

# Все возможности
pip install docxmd-converter[all]
```

## 🎯 Быстрый старт

### CLI интерфейс

```bash
# Конвертация с интеллектуальным анализом
docxmd-converter input.docx output.md

# Запуск GUI
docxmd-gui

# Запуск веб-интерфейса
docxmd-web
```

### Python API

```python
from docxmd_converter import IntelligentProcessor

# Создание процессора
processor = IntelligentProcessor()

# Интеллектуальная обработка документа
result = processor.process_document_intelligently("document.docx")

print(f"Качество: {result['quality']['overall_score']:.1f}/100")
print(f"Тип документа: {result['document_type']}")
print("Рекомендации:", result['quality']['recommendations'])
```

### NLP анализ

```python
from docxmd_converter import NLPAnalyzer

analyzer = NLPAnalyzer()

# Извлечение признаков
features = analyzer.extract_features(text)
print(f"Слов: {features.word_count}")
print(f"Формальность: {features.formality_score:.2f}")

# Ключевые фразы
phrases = analyzer.extract_key_phrases(text, top_n=5)
```

### Оценка качества

```python
from docxmd_converter import IntelligentQualityAssessor

assessor = IntelligentQualityAssessor()

# Комплексная оценка
quality = assessor.assess_quality(text, features, "должностная_инструкция")
print(f"Общая оценка: {quality.overall_score:.1f}")
print("Рекомендации:", quality.recommendations)
```

## 📊 Поддерживаемые типы документов

- 📋 **Должностные инструкции**
- 📄 **Положения и регламенты**
- 📈 **Отчеты и аналитика**
- 📝 **Технические документы**
- 📚 **Общие текстовые документы**

## 🎯 Возможности NLP

- **Извлечение сущностей**: даты, организации, должности
- **Анализ тональности**: позитивная/негативная/нейтральная
- **Определение языка**: русский/английский/смешанный
- **Ключевые фразы**: автоматическое извлечение
- **Согласованность терминологии**: проверка вариаций

## 📈 Метрики качества

- **Структура** (25%): заголовки, списки, таблицы
- **Содержание** (35%): объем, словарь, формальность
- **Согласованность** (20%): терминология, нумерация
- **Полнота** (20%): обязательные разделы

## 🌐 Интерфейсы

### 1. 🧠 Интеллектуальный процессор
```python
from docxmd_converter import IntelligentProcessor
processor = IntelligentProcessor()
result = processor.process_document_intelligently("doc.docx")
```

### 2. 🌐 Веб-интерфейс
```bash
docxmd-web
# Доступен по адресу: http://localhost:5000
```

### 3. 🖥️ GUI интерфейс
```bash
docxmd-gui
```

## 🔧 Конфигурация

Настройки в `config/document_templates.json`:

```json
{
  "templates": {
    "должностная_инструкция": {
      "required_sections": ["общие положения", "обязанности", "права"],
      "formality_threshold": 0.7
    }
  }
}
```

## 📊 Статистика

Система ведет статистику обработки:
- Количество обработанных файлов
- Среднее время обработки
- Средняя оценка качества
- Распределение по типам документов

## 🧪 Тестирование

```bash
# Установка с dev зависимостями
pip install docxmd-converter[dev]

# Запуск тестов
pytest

# Покрытие кода
pytest --cov=docxmd_converter
```

## 📝 История изменений

### v3.1.0 (Текущая)
- ✅ Полная реорганизация кодовой базы
- ✅ Модульная архитектура
- ✅ Улучшенный NLP анализ
- ✅ Интеллектуальная оценка качества
- ✅ Множественные интерфейсы

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 🆘 Поддержка

- 📧 Email: team@docxmd-converter.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/docxmd-converter/issues)
- 📖 Документация: [GitHub Wiki](https://github.com/your-repo/docxmd-converter/wiki)

---

**DocxMD Converter** - Превращаем документы в интеллектуальные данные! 🚀