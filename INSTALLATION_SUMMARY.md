# 📋 DocxMD Converter v2.1.0 - Сводка по установке и запуску

## 🎯 Краткая сводка

**DocxMD Converter v2.1.0** - мощный инструмент для конвертации DOCX ↔ MD с расширенными возможностями постобработки должностных инструкций через Enhanced Processor.

---

## 🚀 Способы установки

### 1️⃣ Из PyPI (Рекомендуемо для пользователей)
```bash
pip install docxmd-converter
docxmd --version  # Проверка установки
```

### 2️⃣ Локальная разработка (Для разработчиков)
```bash
git clone https://github.com/we256681/docxmd_converter.git
cd docxmd_converter
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -e .
```

### 3️⃣ Из локального пакета (Для тестирования)
```bash
cd docxmd_converter
python -m build
pip install dist/docxmd_converter-2.0.1-py3-none-any.whl
```

---

## ⚡ Основные команды

### Быстрый старт (1 минута):
```bash
# Установка
pip install docxmd-converter

# Простая конвертация с Enhanced обработкой
docxmd --src input.docx --dst output.md --format docx2md --processor enhanced --post-process

# GUI интерфейс
docxmd-gui
```

### Типичные сценарии:
```bash
# Массовая обработка документов
docxmd --src ./documents --dst ./markdown --format docx2md --processor enhanced --post-process

# Безопасное тестирование
docxmd --src ./docs/Conversion --dst ./docs/Conversion --format docx2md --processor enhanced --post-process

# Только постобработка MD файлов
docxmd --src ./markdown --dst ./improved --format md2md --processor enhanced --post-process
```

---

## 📖 Подробная документация

| Файл | Описание | Аудитория |
|------|----------|-----------|
| **[QUICK_START.md](QUICK_START.md)** | Быстрый старт за 1 минуту | 👤 Новые пользователи |
| **[USAGE_GUIDE.md](USAGE_GUIDE.md)** | Полное руководство со всеми возможностями | 👥 Все пользователи |
| **[INTEGRATION_COMPLETED.md](INTEGRATION_COMPLETED.md)** | Отчет об интеграции Enhanced процессора | 🔧 Разработчики |
| **[README.md](README.md)** | Общая информация о проекте | 🌐 Все |
| **[CHANGELOG.md](CHANGELOG.md)** | История изменений | 🔧 Разработчики |

---

## 🎯 Enhanced Processor v2.1.0 - Ключевая особенность

### Что это?
- **Единый процессор**: Объединены все лучшие решения из scripts/
- **Интеллектуальный анализ**: Автоматическое распознавание должностных инструкций
- **Комплексная очистка**: Полное удаление артефактов КонсультантПлюс
- **Безопасность**: Защита документации от случайных изменений
- **Структуризация**: Автоматическое форматирование в стандартный вид

### Как использовать?
```bash
# Добавьте флаги к любой команде конвертации:
--processor enhanced --post-process
```

---

## 🛡️ Безопасность

### Защищенные области (автоматически пропускаются):
- `docs/documentation_management/` - документация проекта
- `*.py`, `*.json`, `*.yml` - системные файлы
- `README.*`, `CHANGELOG.*` - важные файлы проекта

### Безопасная зона для тестирования:
- `docs/Conversion/` - рекомендуемая папка для экспериментов

---

## ❗ Требования

- **Python**: >= 3.8
- **Pandoc**: Обязательно для конвертации
  ```bash
  # Ubuntu/Debian
  sudo apt install pandoc

  # macOS
  brew install pandoc

  # Windows
  choco install pandoc
  ```

---

## 🎯 Быстрая проверка работоспособности

```bash
# 1. Проверить установку
docxmd --version

# 2. Проверить Enhanced процессор
python -c "from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor; print('✅ Enhanced Processor готов')"

# 3. Тест на примере (если есть docx файлы в docs/Conversion/)
docxmd --src ./docs/Conversion --dst ./docs/Conversion --format docx2md --processor enhanced --post-process
```

---

## 🔗 Быстрые ссылки

- **GitHub**: https://github.com/we256681/docxmd_converter
- **PyPI**: https://pypi.org/project/docxmd-converter/
- **Баг-репорты**: GitHub Issues

---

## 🎯 После обновления

### Быстрая проверка новой версии:
```bash
# 1. Проверить версию
docxmd --version  # Должно показать: docxmd 3.0.0

# 2. Проверить Enhanced Processor v2.1.0
python -c "from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor; processor = EnhancedDocumentProcessor(); print(f'✅ Enhanced Processor v{processor.version} готов')"

# 3. Проверить GUI (если используете)
docxmd-gui --help

# 4. Тестовая конвертация
echo "# Test v3.0.0" > test.md
docxmd --src . --dst . --format md2docx
```

### 🆕 Новое в версии 3.0.0:
- ✅ Enhanced Processor v2.1.0 полностью интегрирован
- ✅ Улучшенный GUI интерфейс с полной функциональностью
- ✅ Расширенный Python API с новыми методами
- ✅ Богатые CLI опции (dry-run, force-process, verbose)
- ✅ Улучшенная система отчетов (файловые и консольные)
- ✅ Профессиональная работа с шаблонами

---

## 📚 Связанные документы

- **[QUICK_START.md](QUICK_START.md)** - Быстрый старт для новых пользователей
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Полное руководство пользователя
- **[TESTING_RESULTS.md](TESTING_RESULTS.md)** - Результаты тестирования v3.0.0
- **[FINAL_TESTING_SUMMARY.md](FINAL_TESTING_SUMMARY.md)** - Финальная сводка тестирования
- **[README.md](README.md)** - Основная документация проекта
- **[CHANGELOG.md](CHANGELOG.md)** - История изменений

---

**✅ Готово к использованию! DocxMD Converter v3.0.0 с Enhanced Processor v2.1.0 - ваш надежный инструмент для профессиональной работы с документами.**

<!-- METADATA
{
  "created_at": "2025-08-09",
  "updated_at": "2025-08-09",
  "author": "BAS-Core Team",
  "version": "3.0.0",
  "status": "current",
  "category": "guide",
  "topics": ["installation", "upgrade", "setup"],
  "audience": "all_users",
  "priority": "high"
}
-->
