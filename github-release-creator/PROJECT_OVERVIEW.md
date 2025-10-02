# 📦 GitHub Release Creator - Обзор проекта

## 📁 Структура проекта

```
.
├── create_releases.py              # Простой базовый скрипт
├── create_releases_advanced.py     # Расширенная версия с CLI
├── repositories.txt                # Конфигурационный файл для репозиториев
├── requirements.txt                # Python зависимости
├── README.md                       # Полная документация
├── QUICKSTART.md                   # Руководство быстрого старта
└── .github-workflows-example.yml   # Пример GitHub Action
```

## 🎯 Что делает этот проект?

Автоматически создает GitHub релизы на основе последнего тега в каждом репозитории.

### Основные возможности:
- ✅ Обработка множества репозиториев за один запуск
- ✅ Автоматическая генерация release notes из коммитов
- ✅ Проверка существующих релизов (избегает дубликатов)
- ✅ Поддержка черновиков и пре-релизов
- ✅ Удобный CLI интерфейс
- ✅ Конфигурационные файлы
- ✅ Детальное логирование

## 🚀 Быстрый старт (30 секунд)

### 1. Установка
```bash
pip install requests
```

### 2. Настройка токена
```bash
export GITHUB_TOKEN='ghp_ваш_токен'
```

### 3. Создание файла с репозиториями
```bash
cat > repos.txt << EOF
username/repo1
username/repo2
EOF
```

### 4. Запуск
```bash
python create_releases_advanced.py -f repos.txt
```

## 📊 Два варианта использования

### Вариант 1: Простой (create_releases.py)
- Редактируете список репозиториев прямо в коде
- Просто запускаете: `python create_releases.py`
- Лучше для: разового использования, простых задач

### Вариант 2: Продвинутый (create_releases_advanced.py)
- Использует конфигурационные файлы или аргументы командной строки
- Больше опций: черновики, пре-релизы, подробный вывод
- Лучше для: регулярного использования, CI/CD, больших проектов

## 💡 Популярные команды

```bash
# Создать релизы из файла
python create_releases_advanced.py -f repositories.txt

# Создать релизы для конкретных репозиториев
python create_releases_advanced.py -r owner/repo1 owner/repo2

# Создать черновики для проверки
python create_releases_advanced.py -f repos.txt --draft

# Создать пре-релизы (beta/alpha)
python create_releases_advanced.py -f repos.txt --prerelease

# Подробный вывод
python create_releases_advanced.py -f repos.txt -v

# Помощь
python create_releases_advanced.py --help
```

## 🔧 Настройки

### В простом скрипте (create_releases.py):
```python
repositories = [
    ('owner', 'repo1'),
    ('owner', 'repo2'),
]

auto_notes = True      # Генерировать release notes
draft = False          # Создавать черновики
prerelease = False     # Пометить как пре-релиз
```

### В продвинутом скрипте (create_releases_advanced.py):
Используйте флаги командной строки:
- `--draft` - создать черновики
- `--prerelease` - пометить как пре-релиз
- `--no-auto-notes` - не генерировать автоматические заметки
- `-v` - подробный вывод

## 📝 Формат файла repositories.txt

```
# Комментарии начинаются с #
# Формат: owner/repo (один на строку)

username/project1
username/project2
organization/backend
organization/frontend

# Пустые строки игнорируются
```

## 🔑 Получение GitHub токена

1. Перейдите: https://github.com/settings/tokens
2. Нажмите "Generate new token (classic)"
3. Выберите права: **repo** (полный доступ)
4. Скопируйте токен
5. Установите: `export GITHUB_TOKEN='your_token'`

⚠️ **Важно**: Храните токен в безопасности!

## 📖 Документация

- **README.md** - Полная документация с примерами
- **QUICKSTART.md** - Быстрое руководство для начала работы
- `.github-workflows-example.yml` - Пример автоматизации через GitHub Actions

## 🎭 Примеры сценариев

### 1. Еженедельный релиз микросервисов
```bash
#!/bin/bash
# weekly-release.sh
export GITHUB_TOKEN='your_token'
python create_releases_advanced.py -f microservices.txt
```

### 2. Release Candidate
```bash
# Создаем черновики пре-релизов для проверки
python create_releases_advanced.py -f repos.txt --draft --prerelease
```

### 3. Быстрый релиз одного проекта
```bash
python create_releases_advanced.py -r mycompany/urgent-fix
```

## 🐛 Решение проблем

| Проблема | Решение |
|----------|---------|
| `No module named 'requests'` | `pip install requests` |
| `401 Unauthorized` | Проверьте токен и его права |
| `404 Not Found` | Проверьте имя репозитория и доступ |
| `Нет тегов` | Создайте тег: `git tag v1.0.0 && git push origin v1.0.0` |

## 🔄 GitHub Actions интеграция

Используйте `.github-workflows-example.yml` для автоматического создания релизов при push тегов.

## 📊 Что происходит при запуске?

1. **Проверка токена** - валидация доступа к GitHub API
2. **Загрузка репозиториев** - из файла или аргументов
3. **Для каждого репозитория:**
   - Получение последнего тега
   - Проверка существования релиза
   - Генерация release notes (опционально)
   - Создание релиза
4. **Итоговая статистика** - успешные, пропущенные, ошибки

## 🎨 Пример вывода

```
🚀 Начинаем создание релизов...

============================================================

📦 Обработка username/project1...
✓ Найден тег v1.2.3 в username/project1
✅ Релиз v1.2.3 создан в username/project1
   URL: https://github.com/username/project1/releases/tag/v1.2.3

📦 Обработка username/project2...
⚠️  Релиз для тега v2.0.0 уже существует в username/project2

============================================================

📊 Итоги:
   ✅ Успешно создано: 1
   ⏭️  Пропущено (уже существуют): 1
   ❌ Ошибок: 0
   📦 Всего репозиториев: 2
```

## 🤝 Использование как модуль

```python
from create_releases_advanced import GitHubReleaseManager

manager = GitHubReleaseManager('your_token')
manager.process_repository('owner', 'repo', auto_notes=True)
```

## 📄 Лицензия

MIT License - используйте свободно!

## 🎯 Начните прямо сейчас!

```bash
# 1. Установите зависимости
pip install requests

# 2. Установите токен
export GITHUB_TOKEN='your_token_here'

# 3. Создайте список репозиториев
echo "username/repo1" > repos.txt
echo "username/repo2" >> repos.txt

# 4. Запустите!
python create_releases_advanced.py -f repos.txt -v
```

Готово! 🎉
