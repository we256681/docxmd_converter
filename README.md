# DocxMD Converter

[![PyPI version](https://badge.fury.io/py/docxmd-converter.svg)](https://badge.fury.io/py/docxmd-converter)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Мощный Python пакет для конвертации между Microsoft Word (.docx) и Markdown (.md) файлами с поддержкой шаблонов, рекурсивной обработкой директорий и **передовой системой пост-обработки документов**.

## ✨ Особенности

### 🔄 Конвертация
- **Двунаправленная конвертация**: `.docx` ⇄ `.md`
- **Поддержка шаблонов**: используйте кастомные .docx шаблоны
- **Рекурсивная обработка**: конвертируйте целые деревья папок
- **Сохранение структуры**: иерархия папок остается неизменной

### 🧠 Финальная интеграция - Enhanced процессор v2.1.0
- **🚀 Единая архитектура**: объединены все лучшие решения
- **📋 Интеллектуальное распознавание**: автоматическое определение должностных инструкций
- **🛡️ Безопасная обработка**: защита документации от случайных изменений
- **🎯 Полная структуризация**: стандартизированный формат документов
- **✨ Комплексная очистка**: удаление всех артефактов КонсультантПлюс
- **📊 Расширенные метаданные**: качественная оценка обработки

### 🖥️ Интерфейсы
- **CLI**: мощный командный интерфейс
- **GUI**: удобное графическое приложение
- **API**: программный доступ ко всем функциям

### 📈 Отчетность и качество
- **Детальные отчеты**: статистика обработки и качества
- **Метрики качества**: high/medium/low оценки
- **Прогресс**: отслеживание выполнения операций

## 🚀 Быстрый старт

### Установка

```bash
# Из PyPI (рекомендуемо)
pip install docxmd-converter

# Обновление существующей установки
pip install docxmd-converter --upgrade

# Или локально для разработки
git clone https://github.com/we256681/docxmd_converter.git
cd docxmd_converter && pip install -e .
```

> **📋 Подробное руководство:** [INSTALLATION_SUMMARY.md](INSTALLATION_SUMMARY.md) - полная информация по установке, обновлению и решению проблем

**Важно**: Требуется установленный [Pandoc](https://pandoc.org/).

#### Установка Pandoc

**Ubuntu/Debian:**
```bash
sudo apt-get install pandoc
```

**macOS:**
```bash
brew install pandoc
```

**Windows:**
```bash
choco install pandoc
# или скачайте с pandoc.org
```

### Примеры использования

#### 🎯 Рекомендуемое использование (Enhanced процессор v2.1.0)

```bash
# Безопасное тестирование в специальной папке
docxmd --src ./docs/Conversion --dst ./docs/Conversion --format docx2md --processor enhanced --post-process

# Полная конвертация с передовой пост-обработкой
docxmd --src ./documents --dst ./markdown --format docx2md --processor enhanced --post-process

# Принудительная переобработка всех файлов (осторожно!)
docxmd --src ./documents --dst ./markdown --format docx2md --processor enhanced --post-process --force-process
```

#### 📋 Базовые операции

```bash
# Простая конвертация без обработки
docxmd --src ./documents --dst ./markdown --format docx2md

# Обратная конвертация с шаблоном
docxmd --src ./markdown --dst ./documents --format md2docx --template ./template.docx

# Подробный вывод
docxmd --src ./input --dst ./output --format docx2md --verbose
```

#### ⚙️ Типы пост-процессоров

```bash
# Enhanced (рекомендуемый) - полная очистка и структурирование
--processor enhanced

# Advanced - продвинутая обработка
--processor advanced

# Basic - базовая очистка
--processor basic
```

## � Что делает Enhanced процессор

### ✅ Очистка артефактов
- Удаляет все следы КонсультантПлюс и других систем
- Очищает обратные слеши и неправильные переносы
- Исправляет сломанную пунктуацию и форматирование

### 🏗️ Структурирование документов
- Создает единый формат для всех должностных инструкций:
  ```markdown
  # Должностная инструкция: Название_должности

  ## Информация о документе
  ## 1. Общие положения
  ## 2. Функции
  ## 3. Должностные обязанности
  ## 4. Права
  ## 5. Ответственность
  ## 6. Заключительные положения
  ## 7. Согласование и утверждение
  ```

### 🎯 Интеллектуальные возможности
- **Распознавание контента**: определяет должностные инструкции по содержимому
- **Пропуск нерелевантных файлов**: не обрабатывает документацию и конфигурации
- **Исправление полей**: унифицирует поля заполнения в формат `` `____________________________` ``
- **Склеивание разбитых строк**: восстанавливает целостность текста

## 🔧 Программное использование

```python
from docxmd_converter import DocxMdConverter
from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor

# Безопасное тестирование
converter = DocxMdConverter()
converter.convert_directory(
    src_dir="./docs/Conversion",
    dst_dir="./docs/Conversion",
    format="docx2md",
    post_process=True,
    processor_type="enhanced"
)

# Продакшн конвертация с полной пост-обработкой
converter.convert_directory(
    src_dir="./documents",
    dst_dir="./markdown",
    format="docx2md",
    post_process=True,
    processor_type="enhanced"
)

# Только пост-обработка существующих файлов
processor = EnhancedDocumentProcessor()
results = processor.process_directory("./docs/Conversion")
print(f"Обработано: {results.processed}/{results.total}")
print(f"Пропущено: {results.skipped}, Ошибок: {results.errors}")
print(f"Качество: {results.quality_stats}")
```

## 📋 GUI Приложение

```bash
# Запуск графического интерфейса
docxmd-gui
```

Или программно:
```python
from docxmd_converter.gui import main
main()
```

## 🔍 Поиск проблем

### Частые проблемы

**Pandoc не найден:**
```bash
# Проверьте установку
pandoc --version

# Ubuntu/Debian
sudo apt-get install pandoc

# Или обновите PATH
```

**Ошибки кодировки:**
```bash
# Используйте параметр verbose для диагностики
docxmd --src ./input --dst ./output --format docx2md --verbose
```

**Пропускаются файлы:**
```bash
# Принудительная обработка
docxmd --src ./input --dst ./output --format docx2md --processor enhanced --post-process --force-process
```

## � Связанные документы

- [CHANGELOG.md](CHANGELOG.md) - история изменений
- [docs/documentation_management/Rules.md](docs/documentation_management/Rules.md) - правила документации
- [examples/](examples/) - примеры использования
- [tests/](tests/) - тесты

## 🤝 Вклад в проект

1. Изучите [правила документации](docs/documentation_management/Rules.md)
2. Создайте форк проекта
3. Создайте ветку для изменений
4. Добавьте тесты для новых функций
5. Убедитесь, что тесты проходят
6. Создайте Pull Request

## 📄 Лицензия

MIT License - подробности в [LICENSE](LICENSE).

## 🚀 Финализация в версии 2.1.0

### ✅ Завершена полная интеграция
- **Единая архитектура**: объединены все лучшие решения из scripts/
- **Enhanced процессор v2.1.0**: финальная версия с комплексной обработкой
- **Безопасность**: защита документации от случайных изменений
- **Тестирование**: папка docs/Conversion/ для безопасных экспериментов
- **Очищенный код**: удалена директория scripts/, все интегрировано

### 🛡️ Безопасная обработка документов
- **Защита системных файлов**: автоматический пропуск .py, .json, .yml файлов
- **Защита документации**: исключение docs/documentation_management/
- **Интеллектуальный анализ**: обработка только должностных инструкций
- **Архивирование**: старые скрипты сохранены в archive/scripts_backup/

---

**Статус проекта**: ✅ Активная разработка
**Поддерживаемые версии Python**: 3.8+
**Платформы**: Windows, macOS, Linux

<!-- METADATA
{
  "created_at": "2025-08-09",
  "updated_at": "2025-08-09",
  "author": "BAS-Core Team",
  "version": "2.1.0",
  "status": "current",
  "category": "guide",
  "integration_status": "completed",
  "scripts_migration": "completed_and_archived"
}
-->
