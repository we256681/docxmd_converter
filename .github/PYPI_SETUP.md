# 🔐 Настройка PyPI токенов для GitHub Actions

## 🎯 Быстрая настройка

### 1. Создание API токенов на PyPI

#### PyPI (продакшн):
1. Перейти на https://pypi.org/manage/account/token/
2. Нажать **"Add API token"**
3. **Token name**: `github-actions-docxmd-converter`
4. **Scope**: `Project: docxmd-converter` (или "Entire account" если проект еще не создан)
5. Скопировать токен (начинается с `pypi-`)

#### Test PyPI (тестирование):
1. Перейти на https://test.pypi.org/manage/account/token/
2. Нажать **"Add API token"**
3. **Token name**: `github-actions-docxmd-converter-test`
4. **Scope**: `Project: docxmd-converter` или "Entire account"
5. Скопировать токен

### 2. Добавление токенов в GitHub

1. Перейти в репозиторий на GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Нажать **"New repository secret"**

#### Добавить секреты:
- **Name**: `PYPI_API_TOKEN`
  **Value**: `pypi-ваш_токен_для_pypi`

- **Name**: `TEST_PYPI_API_TOKEN`
  **Value**: `pypi-ваш_токен_для_test_pypi`

### 3. Проверка настройки

После настройки токенов, попробуйте:

1. **Ручной запуск workflow:**
   - Actions → Publish to PyPI → Run workflow
   - Выберите "Publish to Test PyPI only" = true
   - Запустите

2. **Автоматическая публикация:**
   - Создайте новый релиз в GitHub
   - Workflow запустится автоматически

---

## 📋 Пошаговая инструкция с скриншотами

### Шаг 1: Регистрация на PyPI

**PyPI (продакшн):**
```
1. https://pypi.org/account/register/
2. Подтвердить email
3. Включить 2FA (рекомендуется)
```

**Test PyPI (тестирование):**
```
1. https://test.pypi.org/account/register/
2. Подтвердить email
3. Включить 2FA (рекомендуется)
```

### Шаг 2: Создание API токенов

**На PyPI:**
```
1. Войти в аккаунт → Account settings
2. Scroll down → API tokens
3. Add API token
4. Token name: github-actions-docxmd-converter
5. Scope:
   - "Entire account" (если проект еще не создан)
   - "Project: docxmd-converter" (если проект уже существует)
6. Create token
7. ВАЖНО: Скопировать токен сразу! (показывается только один раз)
```

**На Test PyPI (аналогично):**
```
1. test.pypi.org → Account settings → API tokens
2. Add API token
3. Token name: github-actions-docxmd-converter-test
4. Scope: как выше
5. Скопировать токен
```

### Шаг 3: Добавление в GitHub Secrets

**В репозитории GitHub:**
```
1. Settings (вкладка репозитория)
2. Security → Secrets and variables → Actions
3. New repository secret

Секрет 1:
- Name: PYPI_API_TOKEN
- Secret: pypi-AgENdGVzdC5weXBpLm9yZ... (ваш токен PyPI)

Секрет 2:
- Name: TEST_PYPI_API_TOKEN
- Secret: pypi-AgENdGVzdC5weXBpLm9yZ... (ваш токен Test PyPI)
```

---

## 🧪 Тестирование настройки

### Вариант 1: Ручной запуск

```bash
# В GitHub: Actions → Publish to PyPI → Run workflow
# Установить: "Publish to Test PyPI only" = true
# Нажать: Run workflow
```

Ожидаемый результат:
- ✅ Workflow успешно выполнился
- ✅ Пакет появился на https://test.pypi.org/project/docxmd-converter/

### Вариант 2: Локальная проверка токенов

Создать временный `.pypirc`:
```bash
cat > ~/.pypirc << EOF
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-ваш_токен_test_pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-ваш_токен_pypi
EOF

chmod 600 ~/.pypirc
```

Проверить:
```bash
# Собрать пакет
python -m build

# Попробовать загрузить в Test PyPI
twine upload --repository testpypi dist/* --verbose
```

### Вариант 3: Создание тестового релиза

```bash
# Обновить версию
bump2version patch

# Создать git tag
git tag v$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

# Push с тегом
git push origin main --tags

# Создать релиз на GitHub (через UI или CLI)
gh release create v2.0.2 --title "Release v2.0.2" --notes "Test release"
```

---

## 🔧 Устранение проблем

### Ошибка: "Invalid or non-existent authentication information"

**Проблема**: Неверный токен или токен истек

**Решение**:
1. Проверить, что токен скопирован полностью (включая `pypi-` в начале)
2. Создать новый токен на PyPI
3. Обновить секрет в GitHub

### Ошибка: "Repository not found"

**Проблема**: Токен создан для конкретного проекта, но проект еще не существует на PyPI

**Решения**:
1. Создать токен с scope "Entire account"
2. Или сначала вручную загрузить первую версию пакета

### Ошибка: "File already exists"

**Проблема**: Версия пакета уже существует на PyPI

**Решение**:
1. Обновить версию в `pyproject.toml`
2. Пересобрать пакет: `python -m build`

### Workflow не запускается

**Проблема**: Файл `publish.yml` не в правильном месте или содержит ошибки

**Решение**:
1. Проверить путь: `.github/workflows/publish.yml`
2. Проверить YAML синтаксис
3. Проверить, что секреты добавлены в правильном репозитории

---

## 🛡️ Безопасность

### Рекомендации:

1. **Ограниченные права токенов**: Создавайте токены только для нужного проекта
2. **Регулярная ротация**: Обновляйте токены каждые 6-12 месяцев
3. **2FA**: Включите двухфакторную аутентификацию на PyPI
4. **Мониторинг**: Следите за активностью токенов в PyPI

### Что НЕ делать:

❌ Не коммитить токены в код
❌ Не создавать токены с избыточными правами
❌ Не использовать одни токены для разных проектов
❌ Не храните токены в незащищенных местах

---

## 📋 Чеклист настройки

- [ ] Зарегистрирован аккаунт на PyPI
- [ ] Зарегистрирован аккаунт на Test PyPI
- [ ] Включена 2FA на обеих платформах
- [ ] Создан API токен для PyPI
- [ ] Создан API токен для Test PyPI
- [ ] Токены добавлены в GitHub Secrets
- [ ] Workflow файл создан в `.github/workflows/`
- [ ] Протестирована публикация в Test PyPI
- [ ] Протестирована автоматическая публикация через релиз

---

**✅ После выполнения всех шагов, ваш пакет будет автоматически публиковаться на PyPI при создании новых релизов!**
