# ✅ Чеклист релиза DocxMD Converter

## 🎯 Перед релизом

### 📋 Подготовка кода

- [ ] Все изменения зафиксированы и протестированы
- [ ] Обновлен `CHANGELOG.md` с описанием изменений
- [ ] Обновлена документация (README.md, USAGE_GUIDE.md)
- [ ] Проверены и обновлены зависимости в `pyproject.toml`
- [ ] Все тесты проходят: `python -m pytest`

### 🔍 Проверка Enhanced Processor

- [ ] Enhanced Processor v2.1.0 работает корректно
- [ ] Тест импорта: `python -c "from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor; print('OK')"`
- [ ] Тест обработки: безопасный тест в `docs/Conversion/`
- [ ] Защита документации работает (пропуск системных файлов)

### 📦 Версионирование

- [ ] Обновлена версия в `pyproject.toml`
- [ ] Создан git tag с новой версией
- [ ] Версия соответствует семантическому версионированию (MAJOR.MINOR.PATCH)

---

## 🚀 Процесс релиза

### Вариант 1: Автоматический (через GitHub)

1. **Создать релиз на GitHub:**
   ```bash
   # Обновить версию
   bump2version minor  # или patch/major

   # Push изменений
   git push origin main

   # Создать и push тег
   git tag v$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
   git push origin --tags

   # Создать релиз через GitHub UI или CLI
   gh release create v2.1.0 --title "Release v2.1.0" --notes-file CHANGELOG.md
   ```

2. **GitHub Actions автоматически:**
   - [ ] Запустит тесты
   - [ ] Соберет пакет
   - [ ] Опубликует на PyPI
   - [ ] Создаст комментарий к релизу

### Вариант 2: Полуавтоматический (скрипт)

```bash
# Использовать готовый скрипт
./scripts/publish.sh
```

Скрипт интерактивно:
- [ ] Предложит обновить версию
- [ ] Соберет пакет
- [ ] Проверит пакет
- [ ] Предложит выбрать репозиторий (Test PyPI/PyPI)

### Вариант 3: Ручной

```bash
# 1. Обновить версию
bump2version minor

# 2. Собрать пакет
rm -rf dist/
python -m build

# 3. Проверить пакет
twine check dist/*

# 4. Тестовая публикация
twine upload --repository testpypi dist/*

# 5. Проверить установку из Test PyPI
pip install --index-url https://test.pypi.org/simple/ docxmd-converter

# 6. Продакшн публикация
twine upload dist/*
```

---

## 🧪 После релиза - проверки

### Проверка PyPI

- [ ] Пакет появился на https://pypi.org/project/docxmd-converter/
- [ ] Версия корректная
- [ ] Описание отображается правильно
- [ ] Все файлы загружены (wheel + tar.gz)

### Проверка установки

```bash
# Проверить установку из PyPI
pip install docxmd-converter --upgrade
docxmd --version

# Проверить Enhanced Processor
python -c "from docxmd_converter.enhanced_processor import EnhancedDocumentProcessor; print('✅ v' + EnhancedDocumentProcessor().version)"

# Проверить CLI
docxmd --help

# Проверить GUI
docxmd-gui --help
```

### Функциональное тестирование

- [ ] Конвертация DOCX → MD работает
- [ ] Enhanced постобработка работает
- [ ] GUI запускается
- [ ] Python API доступен

---

## 📊 Мониторинг

### В первые часы после релиза

- [ ] Проверить статистику загрузок: https://pypistats.org/packages/docxmd-converter
- [ ] Мониторить GitHub Issues на предмет новых багрепортов
- [ ] Проверить работу зависимостей

### В первые дни

- [ ] Собрать фидбек пользователей
- [ ] Проверить совместимость с разными версиями Python
- [ ] Мониторить производительность

---

## 🛠️ Горячие исправления

Если найдена критическая ошибка:

```bash
# 1. Исправить ошибку
git checkout main
# внести исправления

# 2. Создать patch релиз
bump2version patch

# 3. Быстрая публикация
python -m build
twine upload dist/*

# 4. Создать hotfix релиз на GitHub
gh release create v2.1.1 --title "Hotfix v2.1.1" --notes "Critical bug fixes"
```

---

## 📋 Коммуникация

### Анонсы релиза

После успешного релиза:

- [ ] Обновить README.md с новой версией
- [ ] Анонсировать в социальных сетях (если применимо)
- [ ] Уведомить активных пользователей
- [ ] Обновить документацию на внешних ресурсах

### Шаблон анонса

```markdown
🎉 DocxMD Converter v2.1.0 Released!

## Что нового:
- ✅ Enhanced Processor v2.1.0 - единое решение для обработки документов
- ✅ Улучшенная безопасность и защита документации
- ✅ Полная система документации и руководств

## Установка:
pip install docxmd-converter --upgrade

## Ссылки:
- PyPI: https://pypi.org/project/docxmd-converter/
- GitHub: https://github.com/we256681/docxmd_converter
- Документация: USAGE_GUIDE.md
```

---

## 🔄 Планирование следующего релиза

После каждого релиза:

- [ ] Создать milestone для следующего релиза
- [ ] Собрать запросы функций от пользователей
- [ ] Запланировать рефакторинг и технический долг
- [ ] Обновить roadmap проекта

---

## 📚 Полезные команды

```bash
# Проверить текущую версию
grep '^version = ' pyproject.toml

# Проверить последний тег
git describe --tags --abbrev=0

# Проверить статус сборки
python -m build --check

# Проверить зависимости
pip-audit

# Проверить качество кода
flake8 docxmd_converter/
black --check docxmd_converter/
mypy docxmd_converter/
```

---

**✅ Следуя этому чеклисту, вы обеспечите качественный и безопасный релиз DocxMD Converter!**
