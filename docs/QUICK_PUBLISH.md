# ⚡ Быстрая публикация на PyPI

## 🚀 Готов к публикации!

Пакет **DocxMD Converter v3.1.0** собран и готов к публикации.

## 📋 Быстрый старт

### 1. Подготовка аккаунтов (5 минут)

```bash
# Создайте аккаунты:
# 1. https://test.pypi.org/account/register/
# 2. https://pypi.org/account/register/

# Получите API токены:
# TestPyPI: https://test.pypi.org/manage/account/
# PyPI: https://pypi.org/manage/account/
```

### 2. Тестовая публикация (2 минуты)

```bash
cd /home/uduntu33/Документы/PROJECT/docxmd_converter
source venv/bin/activate
python scripts/publish_test.py
```

**Введите при запросе:**
- Username: `__token__`
- Password: `ваш-testpypi-токен`

### 3. Проверка тестовой установки (1 минута)

```bash
# Создайте новое окружение
python -m venv test_install
source test_install/bin/activate

# Установите с TestPyPI
pip install -i https://test.pypi.org/simple/ docxmd-converter

# Проверьте
python -c "from docxmd_converter import IntelligentProcessor; print('✅ Работает!')"
```

### 4. Публикация на PyPI (2 минуты)

```bash
cd /home/uduntu33/Документы/PROJECT/docxmd_converter
source venv/bin/activate
python scripts/publish_pypi.py
```

**Введите при запросе:**
- Username: `__token__`
- Password: `ваш-pypi-токен`
- Подтверждение: `YES`

## 🎉 Готово!

После публикации пакет будет доступен:

```bash
pip install docxmd-converter
```

## 📊 Что получат пользователи

### CLI интерфейс
```bash
docxmd-converter input.docx output.md
docxmd-gui
docxmd-web
```

### Python API
```python
from docxmd_converter import IntelligentProcessor

processor = IntelligentProcessor()
result = processor.process_document_intelligently("doc.docx")
print(f"Качество: {result['quality']['overall_score']:.1f}/100")
```

## 🔧 Если что-то пошло не так

### Ошибка "File already exists"
```bash
# Увеличьте версию в pyproject.toml и setup.py
# Пересоберите пакет
python scripts/build_package.py
```

### Ошибка "Invalid credentials"
```bash
# Проверьте:
# - Username должен быть __token__
# - Password - ваш API токен (начинается с pypi-)
```

### Ошибка сборки
```bash
# Проверьте структуру
python scripts/build_package.py
```

---

**Удачной публикации! 🚀**