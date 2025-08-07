# 🚀 Руководство по публикации на PyPI и автоматизации через GitHub

## 📋 Содержание
1. [Первичная настройка PyPI](#первичная-настройка-pypi)
2. [Ручная публикация](#ручная-публикация)
3. [Настройка GitHub Actions](#настройка-github-actions)
4. [Автоматическая публикация по тегам](#автоматическая-публикация-по-тегам)
5. [Workflow для разработки](#workflow-для-разработки)

---

## 🔐 Первичная настройка PyPI

### 1. Регистрация на PyPI

1. **Создайте аккаунты:**
   - [TestPyPI](https://test.pypi.org/account/register/) (для тестирования)
   - [PyPI](https://pypi.org/account/register/) (для продакшена)

2. **Включите 2FA** (двухфакторную аутентификацию) в настройках аккаунта

### 2. Создание API токенов

1. **TestPyPI токен:**
   - Перейдите: https://test.pypi.org/manage/account/#api-tokens
   - Нажмите "Add API token"
   - Name: `docxmd-converter-test`
   - Scope: "Entire account" (позже можно ограничить до проекта)
   - **Сохраните токен** (он показывается только один раз!)

2. **PyPI токен:**
   - Перейдите: https://pypi.org/manage/account/#api-tokens
   - Нажмите "Add API token"
   - Name: `docxmd-converter-prod`
   - Scope: "Entire account"
   - **Сохраните токен**

### 3. Локальная настройка

Создайте файл `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

---

## 📦 Ручная публикация

### 1. Установка инструментов

```bash
pip install build twine
```

### 2. Проверка версии

Убедитесь что версия в `pyproject.toml` корректна:

```toml
[project]
name = "docxmd-converter"
version = "0.1.0"  # Увеличьте для новых релизов
```

### 3. Сборка пакета

```bash
# Очистка предыдущих сборок
rm -rf dist/ build/

# Сборка
python -m build

# Проверка содержимого
ls -la dist/
```

Должны появиться файлы:
- `docxmd_converter-0.1.0-py3-none-any.whl`
- `docxmd_converter-0.1.0.tar.gz`

### 4. Проверка пакета

```bash
# Проверка метаданных
twine check dist/*

# Тест установки локально
pip install dist/docxmd_converter-0.1.0-py3-none-any.whl --force-reinstall
```

### 5. Публикация на TestPyPI

```bash
# Загрузка на TestPyPI для тестирования
twine upload --repository testpypi dist/*

# Проверка установки с TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ docxmd-converter
```

### 6. Публикация на PyPI

```bash
# Окончательная загрузка на PyPI
twine upload dist/*

# Проверка установки
pip install docxmd-converter
```

---

## ⚙️ Настройка GitHub Actions

### 1. Создание секретов в GitHub

1. **Перейдите в настройки репозитория:**
   `Settings` → `Secrets and variables` → `Actions`

2. **Добавьте секреты:**
   - `PYPI_API_TOKEN` = ваш PyPI токен
   - `TEST_PYPI_API_TOKEN` = ваш TestPyPI токен

### 2. Структура директорий GitHub Actions

```bash
mkdir -p .github/workflows
```

### 3. Создание основного workflow

Создайте файл `.github/workflows/ci.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [published]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11, 3.12]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y pandoc

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Run linting
      run: |
        black --check .
        isort --check-only .
        flake8 .

    - name: Run type checking
      run: |
        mypy docxmd_converter

    - name: Run tests
      run: |
        pytest tests/ -v --cov=docxmd_converter --cov-report=xml

    - name: Run functional tests
      run: |
        python test_conversion.py

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'release' || (github.event_name == 'push' && github.ref == 'refs/heads/main')

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Check package
      run: twine check dist/*

    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  test-publish:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/

    - name: Publish to TestPyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.TEST_PYPI_API_TOKEN }}
        repository-url: https://test.pypi.org/legacy/

  publish:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'release'

    steps:
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

### 4. Workflow для автоматического версионирования

Создайте файл `.github/workflows/version-bump.yml`:

```yaml
name: Version Bump

on:
  pull_request:
    types: [closed]
    branches: [main]

jobs:
  bump-version:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        token: ${{ secrets.GITHUB_TOKEN }}

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install bump2version
      run: pip install bump2version

    - name: Configure git
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"

    - name: Determine version bump type
      id: version-type
      run: |
        PR_TITLE="${{ github.event.pull_request.title }}"
        PR_LABELS="${{ join(github.event.pull_request.labels.*.name, ' ') }}"

        if [[ "$PR_TITLE" == *"BREAKING CHANGE"* ]] || [[ "$PR_LABELS" == *"breaking"* ]]; then
          echo "type=major" >> $GITHUB_OUTPUT
        elif [[ "$PR_TITLE" == *"feat"* ]] || [[ "$PR_LABELS" == *"feature"* ]]; then
          echo "type=minor" >> $GITHUB_OUTPUT
        else
          echo "type=patch" >> $GITHUB_OUTPUT
        fi

    - name: Bump version
      run: |
        bump2version ${{ steps.version-type.outputs.type }}
        git push origin main --tags
```

### 5. Конфигурация bump2version

Создайте файл `.bumpversion.cfg`:

```ini
[bumpversion]
current_version = 0.1.0
commit = True
tag = True
tag_name = v{new_version}
message = Bump version: {current_version} → {new_version}

[bumpversion:file:pyproject.toml]
search = version = "{current_version}"
replace = version = "{new_version}"

[bumpversion:file:docxmd_converter/__init__.py]
search = __version__ = "{current_version}"
replace = __version__ = "{new_version}"
```

---

## 🏷️ Автоматическая публикация по тегам

### 1. Создание релиза через GitHub

1. **Через веб-интерфейс:**
   - Идите в раздел "Releases" вашего репозитория
   - Нажмите "Create a new release"
   - Тег: `v0.1.1`
   - Заголовок: `Release v0.1.1`
   - Описание: изменения в релизе
   - Нажмите "Publish release"

2. **Через командную строку:**
   ```bash
   # Создание и отправка тега
   git tag v0.1.1
   git push origin v0.1.1

   # Создание релиза через GitHub CLI
   gh release create v0.1.1 --title "Release v0.1.1" --notes "Bug fixes and improvements"
   ```

### 2. Автоматический workflow релиза

Создайте файл `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        sudo apt-get install -y pandoc
        python -m pip install --upgrade pip
        pip install build twine pytest
        pip install -e .[dev]

    - name: Run tests
      run: |
        pytest tests/ -v
        python test_conversion.py

    - name: Build package
      run: python -m build

    - name: Check package
      run: twine check dist/*

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}

    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
        generate_release_notes: true
```

---

## 🔄 Workflow для разработки

### Рекомендуемый процесс разработки:

1. **Создание ветки для функции:**
   ```bash
   git checkout -b feature/new-feature
   # Разработка...
   git commit -m "feat: добавлена новая функция"
   git push origin feature/new-feature
   ```

2. **Создание Pull Request:**
   - Используйте шаблон PR с описанием изменений
   - Добавьте лейблы: `feature`, `bugfix`, `breaking`, etc.
   - CI автоматически запустит тесты

3. **Мерж в main:**
   - После прохождения тестов и ревью
   - Автоматически создастся билд и загрузится на TestPyPI
   - Версия автоматически обновится (опционально)

4. **Создание релиза:**
   ```bash
   # Создание тега запустит автоматическую публикацию
   git tag v0.1.2
   git push origin v0.1.2
   ```

### Шаблон Pull Request

Создайте файл `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## 📋 Описание изменений

Кратко опишите что изменилось и почему.

## 🔄 Тип изменений

- [ ] 🐛 Bug fix (исправление бага)
- [ ] ✨ New feature (новая функция)
- [ ] 💥 Breaking change (ломающие изменения)
- [ ] 📚 Documentation (только документация)
- [ ] 🎨 Style (форматирование, отсутствие изменений в коде)
- [ ] ♻️ Refactoring (рефакторинг без изменения функционала)
- [ ] ⚡ Performance (улучшение производительности)
- [ ] 🧪 Tests (добавление/изменение тестов)

## 🧪 Как тестировалось?

Опишите как вы тестировали изменения.

- [ ] Юнит-тесты проходят
- [ ] Функциональные тесты проходят
- [ ] Протестировано вручную

## 📋 Чек-лист

- [ ] Код следует стандартам проекта
- [ ] Саморевью выполнено
- [ ] Тесты добавлены/обновлены
- [ ] Документация обновлена
- [ ] Нет конфликтов с main ветвой
```

---

## 🔧 Дополнительные настройки

### 1. Обновление `pyproject.toml`

Добавьте дополнительные зависимости для разработки:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=22.0",
    "isort>=5.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "bump2version>=1.0",
    "twine>=4.0",
    "build>=0.10",
]
```

### 2. Конфигурация pre-commit

Создайте файл `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
```

### 3. Установка pre-commit

```bash
pip install pre-commit
pre-commit install
```

---

## 🎯 Резюме команд

### Первая публикация:
```bash
# 1. Подготовка
python -m build
twine check dist/*

# 2. Тест на TestPyPI
twine upload --repository testpypi dist/*

# 3. Публикация на PyPI
twine upload dist/*

# 4. Создание тега для автоматизации
git tag v0.1.0
git push origin v0.1.0
```

### Последующие релизы:
```bash
# Просто создание тега - всё остальное автоматически
git tag v0.1.1
git push origin v0.1.1
```

### Статус пакета:
- 🔍 **TestPyPI**: https://test.pypi.org/project/docxmd-converter/
- 📦 **PyPI**: https://pypi.org/project/docxmd-converter/
- 📊 **GitHub Actions**: во вкладке "Actions" репозитория

---

**🎉 Поздравляем! Ваш пакет готов к автоматической публикации!**