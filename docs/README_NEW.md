# 🚀 DocxMD Converter v3.0.0

> Интеллектуальная система конвертации и обработки документов с NLP-анализом

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
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

## 🏗️ Архитектура

```
src/
├── docxmd_converter/           # Основной пакет
│   ├── intelligent_processor.py   # Главный процессор
│   ├── nlp_analyzer.py            # NLP анализ
│   ├── quality_assessor.py        # Оценка качества
│   ├── models.py                  # Модели данных
│   ├── core.py                    # Базовая логика
│   ├── cli.py                     # CLI интерфейс
│   ├── gui.py                     # GUI интерфейс
│   └── web_interface.py           # Веб интерфейс
└── utils/                      # Утилиты
    ├── content_analyzers.py       # Анализаторы контента
    └── reporting.py               # Генерация отчетов
```

## 🚀 Быстрый старт

### Установка

```bash
git clone <repository>
cd docxmd_converter
pip install -r requirements.txt
```

### Запуск

```bash
# Главное меню
python3 main.py

# Прямой запуск интеллектуального процессора
python3 -m src.docxmd_converter.intelligent_processor

# CLI интерфейс
python3 -m src.docxmd_converter.cli --help
```

## 📋 Интерфейсы

### 1. 🧠 Интеллектуальный процессор
Основной компонент с полным набором возможностей:
- Автоматическое определение типа документа
- NLP-анализ и извлечение сущностей
- Оценка качества с рекомендациями
- Машинное обучение на истории обработки

### 2. 🌐 Веб-интерфейс
```bash
python3 -m src.docxmd_converter.web_interface
# Доступен по адресу: http://localhost:5000
```

### 3. 🖥️ GUI интерфейс
```bash
python3 -m src.docxmd_converter.gui
```

### 4. ⚙️ CLI интерфейс
```bash
python3 -m src.docxmd_converter.cli convert input.docx output.md
```

## 🔧 API

### Базовое использование

```python
from src.docxmd_converter import IntelligentProcessor

# Создание процессора
processor = IntelligentProcessor()

# Обработка документа
result = processor.process_document_intelligently("document.docx")

print(f"Качество: {result['quality']['overall_score']:.1f}/100")
print(f"Тип документа: {result['document_type']}")
```

### NLP анализ

```python
from src.docxmd_converter import NLPAnalyzer

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
from src.docxmd_converter import IntelligentQualityAssessor

assessor = IntelligentQualityAssessor()

# Оценка качества
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

## 🧪 Тестирование

```bash
# Запуск тестов через главное меню
python3 main.py
# Выберите опцию 6

# Прямой запуск тестов
python3 -m pytest tests/
```

## 📊 Статистика

Система ведет статистику обработки:
- Количество обработанных файлов
- Среднее время обработки
- Средняя оценка качества
- Распределение по типам документов

## 🔧 Конфигурация

Настройки хранятся в `config/document_templates.json`:

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

## 📝 История изменений

### v3.0.0 (Текущая)
- ✅ Полная реорганизация кодовой базы
- ✅ Модульная архитектура
- ✅ Улучшенный NLP анализ
- ✅ Интеллектуальная оценка качества
- ✅ Множественные интерфейсы

### v2.x
- Базовая конвертация документов
- Простой анализ структуры

## 🤝 Участие в разработке

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 🆘 Поддержка

- 📧 Email: support@docxmd-converter.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 Документация: [Wiki](https://github.com/your-repo/wiki)

---

**DocxMD Converter** - Превращаем документы в интеллектуальные данные! 🚀