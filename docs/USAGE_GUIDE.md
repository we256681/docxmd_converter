# 📚 DocxMD Converter v2.1.0 - Полное руководство пользователя

## 🎯 Обзор

DocxMD Converter - мощный инструмент для конвертации между форматами `.docx` и `.md` с расширенными возможностями постобработки документов. Включает Enhanced Processor v2.1.0 для комплексной очистки и структурирования должностных инструкций.

---

## 🚀 Способы установки и запуска

### 🏠 1. Локальная разработка (Development Mode)

**Когда использовать**: Разработка, тестирование, модификация кода

#### Установка зависимостей:

```bash
# Клонировать репозиторий
git clone https://github.com/we256681/docxmd_converter.git
cd docxmd_converter

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Установить в режиме разработки
pip install -e .
```

#### Запуск:

```bash
# Активировать окружение
source venv/bin/activate

# CLI интерфейс
docxmd --help
docxmd --src ./docs/Conversion --dst ./output --format docx2md --processor enhanced

# GUI интерфейс
docxmd-gui

# Прямой Python запуск
python -m docxmd_converter.cli --help
python -m docxmd_converter.gui
```

---

### 📦 2. Установка из PyPI (Рекомендуемо)

**Когда использовать**: Продакшн использование, простая установка

#### Установка:

```bash
# Установить из PyPI
pip install docxmd-converter

# Или с дополнительными зависимостями для разработки
pip install docxmd-converter[dev]

# Обновить до последней версии
pip install --upgrade docxmd-converter
```

#### Запуск:

```bash
# CLI интерфейс (доступен глобально)
docxmd --help
docxmd --src ./documents --dst ./markdown --format docx2md --processor enhanced

# GUI интерфейс
docxmd-gui

# Python модуль
python -m docxmd_converter.cli --help
```

---

### 🏗️ 3. Установка из локальных пакетов

**Когда использовать**: Тестирование собранных пакетов, оффлайн установка

#### Сборка пакетов:

```bash
# Установить build инструменты
pip install build twine

# Собрать пакеты
python -m build

# Проверить созданные пакеты
ls dist/
# docxmd_converter-2.0.1-py3-none-any.whl
# docxmd_converter-2.0.1.tar.gz
```

#### Установка из локальных файлов:

```bash
# Установить из wheel файла
pip install dist/docxmd_converter-2.0.1-py3-none-any.whl

# Или из tar.gz архива
pip install dist/docxmd_converter-2.0.1.tar.gz

# Установить напрямую из текущей директории
pip install .
```

---

## ⚙️ Варианты использования

### 🖥️ CLI интерфейс (Основной)

#### Базовая конвертация:

```bash
# DOCX → Markdown
docxmd --src input.docx --dst output.md --format docx2md

# Markdown → DOCX
docxmd --src input.md --dst output.docx --format md2docx

# Массовая конвертация директории
docxmd --src ./documents --dst ./markdown --format docx2md
```

#### С Enhanced постобработкой:

```bash
# Рекомендуемый режим - полная обработка
docxmd --src ./docs/Conversion --dst ./output \
       --format docx2md \
       --processor enhanced \
       --post-process

# Только постобработка существующих MD файлов
docxmd --src ./markdown --dst ./cleaned \
       --format md2md \
       --processor enhanced \
       --post-process

# Форсированная перезапись уже обработанных файлов
docxmd --src ./docs --dst ./output \
       --format docx2md \
       --processor enhanced \
       --post-process \
       --force-process
```

#### Дополнительные опции:

```bash
# Режим сухого прогона (без изменений)
docxmd --src ./test --dst ./output \
       --format docx2md \
       --processor enhanced \
       --dry-run-process

# Подробная отчетность
docxmd --src ./docs --dst ./output \
       --format docx2md \
       --processor enhanced \
       --post-process \
       --verbose

# Помощь и информация
docxmd --help
docxmd --version
```

### 🖼️ GUI интерфейс

```bash
# Запуск графического интерфейса
docxmd-gui

# Или через Python модуль
python -m docxmd_converter.gui
```

**Возможности GUI:**
- Перетаскивание файлов
- Выбор процессоров
- Предпросмотр результатов
- Прогресс-бар конвертации

### 🐍 Python API

#### Базовое использование:

```python
from docxmd_converter.core import DocxMdConverter
from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor

# Создать конвертер
converter = DocxMdConverter()

# Простая конвертация
converter.convert_file('input.docx', 'output.md', 'docx2md')

# Массовая конвертация
converter.convert_directory('./docs', './markdown', 'docx2md')

# С Enhanced постобработкой
processor = EnhancedDocumentProcessor()
results = processor.process_directory('./docs/Conversion/')

print(f"Обработано: {results.processed}/{results.total}")
print(f"Качество: {results.quality_stats}")
```

#### Расширенное использование:

```python
from pathlib import Path
from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor

# Создать процессор
processor = EnhancedDocumentProcessor()

# Обработать один файл
success = processor.process_file('./document.md')

# Получить статистику
results = processor.process_directory('./documents/')
print(f"Всего файлов: {results.total}")
print(f"Успешно: {results.processed}")
print(f"Пропущено: {results.skipped}")
print(f"Ошибок: {results.errors}")
print(f"Качество: {results.quality_stats}")

# Принудительная обработка
results = processor.process_directory('./docs/', force=True)
```

---

## 🛡️ Безопасность и защита документации

### Защищенные директории (автопропуск):
- `docs/documentation_management/`
- `.git/`, `.zencoder/`, `__pycache__/`
- `venv/`, `node_modules/`

### Защищенные файлы (автопропуск):
- `*.py`, `*.json`, `*.yml`, `*.yaml`
- `README.*`, `CHANGELOG.*`, `LICENSE*`

### Безопасная зона для тестирования:
- `docs/Conversion/` - рекомендуемая папка для экспериментов
- `test/`, `temp/`, `converted/` - также безопасны

---

## 📊 Процессоры и качество обработки

### Enhanced Processor v2.1.0 (Рекомендуемый):
- ✅ Комплексная очистка артефактов КонсультантПлюс
- ✅ Интеллектуальное распознавание должностных инструкций
- ✅ Полная структуризация документов
- ✅ Оценка качества и метаданные
- ✅ Безопасная обработка с защитой документации

### Legacy процессоры:
- `basic` - Базовая очистка
- `advanced` - Расширенная очистка (устарел)

### Качественные метрики:
- **Высокое качество**: 4+ секций, полная структура
- **Среднее качество**: 2-3 секции
- **Низкое качество**: <2 секций

---

## 🔧 Устранение неполадок

### Проблемы установки:

```bash
# Обновить pip
pip install --upgrade pip

# Установить Pandoc (требуется для конвертации)
# Ubuntu/Debian:
sudo apt install pandoc

# macOS:
brew install pandoc

# Windows: скачать с https://pandoc.org/installing.html
```

### Проблемы с зависимостями:

```bash
# Переустановить зависимости
pip uninstall docxmd-converter
pip install docxmd-converter

# Или с принудительной переустановкой
pip install --force-reinstall docxmd-converter
```

### Проблемы с правами доступа:

```bash
# Linux/Mac - установка в пользовательскую директорию
pip install --user docxmd-converter

# Или через виртуальное окружение
python -m venv env
source env/bin/activate
pip install docxmd-converter
```

---

## 📈 Примеры использования

### Пример 1: Быстрая конвертация

```bash
# Конвертировать один файл с постобработкой
docxmd --src "Должностная инструкция архивиста.docx" \
       --dst "архивист.md" \
       --format docx2md \
       --processor enhanced \
       --post-process
```

### Пример 2: Массовая обработка

```bash
# Обработать всю директорию с документами
docxmd --src ./HR_documents \
       --dst ./markdown_docs \
       --format docx2md \
       --processor enhanced \
       --post-process \
       --verbose
```

### Пример 3: Только постобработка

```bash
# Улучшить уже конвертированные MD файлы
docxmd --src ./converted_docs \
       --dst ./improved_docs \
       --format md2md \
       --processor enhanced \
       --post-process
```

### Пример 4: Безопасное тестирование

```bash
# Тестировать в безопасной директории
cp documents/*.docx docs/Conversion/
docxmd --src ./docs/Conversion \
       --dst ./docs/Conversion \
       --format docx2md \
       --processor enhanced \
       --post-process
```

---

## 🏷️ Версии и обновления

### Текущие версии:
- **Пакет**: v2.0.1
- **Enhanced Processor**: v2.1.0
- **Python**: >=3.8

### Проверка версий:

```bash
# Версия пакета
docxmd --version

# Версия Enhanced процессора
python -c "from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor; print(EnhancedDocumentProcessor().version)"
```

### Обновление:

```bash
# Обновить до последней версии
pip install --upgrade docxmd-converter

# Принудительная переустановка
pip install --force-reinstall docxmd-converter
```

---

## 🔗 Полезные ссылки

- **GitHub**: https://github.com/we256681/docxmd_converter
- **PyPI**: https://pypi.org/project/docxmd-converter/
- **Документация**: README.md в репозитории
- **Changelog**: CHANGELOG.md
- **Issues**: GitHub Issues для багрепортов

---

**🎯 DocxMD Converter v2.1.0 - Ваш надежный инструмент для работы с документами!**
