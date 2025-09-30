# GitHub Release Creator

Скрипт для автоматического создания релизов в нескольких GitHub репозиториях на основе последнего тега.

## Возможности

- ✅ Создание релизов на основе последнего тега в репозитории
- ✅ Автоматическая генерация описания релиза из коммитов
- ✅ Проверка существующих релизов (не создает дубликаты)
- ✅ Поддержка черновиков и пре-релизов
- ✅ Обработка нескольких репозиториев за один запуск
- ✅ Детальное логирование процесса

## Требования

- Python 3.7+
- GitHub Personal Access Token с правами `repo`

## Установка

1. Клонируйте или скачайте скрипт

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте GitHub Personal Access Token:
   - Перейдите на https://github.com/settings/tokens
   - Нажмите "Generate new token (classic)"
   - Выберите права `repo` (полный доступ к репозиториям)
   - Скопируйте сгенерированный токен

4. Установите токен в переменную окружения:
```bash
export GITHUB_TOKEN='your_token_here'
```

## Использование

### Базовое использование

1. Откройте `create_releases.py` и отредактируйте список репозиториев:

```python
repositories = [
    ('owner1', 'repo1'),
    ('owner2', 'repo2'),
    ('your-username', 'your-repo'),
]
```

2. Запустите скрипт:
```bash
python create_releases.py
```

### Настройки

В функции `main()` можно настроить поведение:

```python
auto_notes = True      # Автоматически генерировать описание из коммитов
draft = False          # Создавать релизы как черновики
prerelease = False     # Отмечать релизы как пре-релизы (beta, alpha)
```

### Примеры

**Создание обычных релизов:**
```python
auto_notes = True
draft = False
prerelease = False
```

**Создание черновиков для проверки:**
```python
auto_notes = True
draft = True          # Релизы будут созданы как черновики
prerelease = False
```

**Создание пре-релизов (beta/alpha):**
```python
auto_notes = True
draft = False
prerelease = True     # Релизы будут отмечены как пре-релизы
```

## Использование как модуль

Вы также можете использовать скрипт как Python модуль:

```python
from create_releases import GitHubReleaseManager

# Инициализация
manager = GitHubReleaseManager('your_github_token')

# Создание релиза в одном репозитории
manager.process_repository(
    owner='username',
    repo='repository',
    auto_notes=True,
    draft=False,
    prerelease=False
)

# Или создание релиза вручную
tag = manager.get_latest_tag('username', 'repository')
if tag:
    manager.create_release(
        owner='username',
        repo='repository',
        tag_name=tag['name'],
        name=f"Release {tag['name']}",
        body="Custom release notes here"
    )
```

## Что делает скрипт

1. **Получает последний тег** из каждого репозитория
2. **Проверяет существование релиза** для этого тега
3. **Генерирует описание** релиза из коммитов между тегами (опционально)
4. **Создает релиз** на GitHub с этим тегом
5. **Выводит статистику** по завершению

## Структура автоматически генерируемого описания

Если включена опция `auto_notes=True`, описание релиза будет содержать:

```markdown
## What's Changed in v1.2.3

- Fix critical bug in authentication (a1b2c3d) by @developer1
- Add new feature for user management (e4f5g6h) by @developer2
- Update dependencies (i7j8k9l) by @developer3

**Full Changelog**: https://github.com/owner/repo/compare/v1.2.3
```

## Обработка ошибок

Скрипт корректно обрабатывает:
- ❌ Отсутствие тегов в репозитории
- ❌ Уже существующие релизы (пропускает их)
- ❌ Ошибки доступа к API GitHub
- ❌ Неверный токен или отсутствие прав

## Логирование

Скрипт выводит детальную информацию о процессе:

```
🚀 Начинаем создание релизов...

============================================================

📦 Обработка owner1/repo1...
✓ Найден тег v1.2.3 в owner1/repo1
✅ Релиз v1.2.3 создан в owner1/repo1
   URL: https://github.com/owner1/repo1/releases/tag/v1.2.3

📦 Обработка owner2/repo2...
⚠️  Релиз для тега v2.0.0 уже существует в owner2/repo2

============================================================

📊 Итоги:
   ✅ Успешно создано: 1
   ❌ Ошибок: 0
   📦 Всего репозиториев: 2
```

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте токен в репозиторий
- Используйте переменные окружения для токена
- Храните токен в безопасном месте
- Регулярно обновляйте токены

## Лицензия

MIT

## Поддержка

Если возникли проблемы:
1. Проверьте, что токен имеет права `repo`
2. Убедитесь, что у вас есть доступ к репозиториям
3. Проверьте, что теги существуют в репозиториях
