# GitLab Release Creator

Скрипт для автоматического создания релизов в нескольких GitLab проектах на основе последнего тега.

## 🎯 Поддержка GitLab

✅ **GitLab.com** (облачная версия)  
✅ **Self-hosted GitLab** (ваш собственный инстанс)  
✅ **GitLab Community Edition**  
✅ **GitLab Enterprise Edition**

## Основные отличия от GitHub версии

### GitLab использует:
- **Personal Access Token** вместо GitHub Token
- **Project ID** для идентификации проектов
- **API endpoint**: `/api/v4`
- **Формат пути**: `namespace/project` или `group/subgroup/project`
- **Поддержка milestones** для связи с релизами

### Дополнительные возможности GitLab:
- Поддержка вложенных групп (`group/subgroup/project`)
- Связывание релизов с milestones
- Поддержка self-hosted инстансов

## 🚀 Быстрый старт

### Шаг 1: Создание токена

1. Перейдите в GitLab: **Settings → Access Tokens**
   - GitLab.com: https://gitlab.com/-/profile/personal_access_tokens
   - Self-hosted: `https://gitlab.your-company.com/-/profile/personal_access_tokens`

2. Создайте новый токен с правами:
   - ✅ **api** (полный доступ к API)

3. Скопируйте токен (начинается с `glpat-`)

### Шаг 2: Установка зависимостей

```bash
pip install requests
```

### Шаг 3: Настройка переменных окружения

#### Для GitLab.com:
```bash
export GITLAB_TOKEN='glpat-your_token_here'
```

#### Для Self-hosted GitLab:
```bash
export GITLAB_TOKEN='glpat-your_token_here'
export GITLAB_URL='https://gitlab.your-company.com'
```

### Шаг 4: Настройка проектов

Создайте файл `gitlab_projects.txt`:
```
username/project1
username/project2
mygroup/backend-api
mygroup/subgroup/frontend
```

### Шаг 5: Запуск

```bash
# Базовая версия (редактируйте список в коде)
python create_releases_gitlab.py

# Продвинутая версия (используйте CLI)
python create_releases_gitlab_advanced.py -f gitlab_projects.txt
```

## 📖 Использование

### Простой скрипт (create_releases_gitlab.py)

Отредактируйте список проектов в коде:

```python
projects = [
    'username/project1',
    'username/project2',
    'mygroup/backend',
]
```

Затем запустите:
```bash
python create_releases_gitlab.py
```

### Продвинутый скрипт (create_releases_gitlab_advanced.py)

#### Из файла конфигурации:
```bash
python create_releases_gitlab_advanced.py -f gitlab_projects.txt
```

#### Указание проектов напрямую:
```bash
python create_releases_gitlab_advanced.py -p username/proj1 group/proj2
```

#### Self-hosted GitLab:
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.company.com
```

#### С milestones:
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -m "v1.0" "MVP"
```

#### Без автоматических заметок:
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  --no-auto-notes
```

#### Подробный вывод:
```bash
python create_releases_gitlab_advanced.py -f projects.txt -v
```

## 🔧 Параметры командной строки

```
-f, --file FILE           Файл со списком проектов
-p, --projects PROJ...    Список проектов напрямую
-u, --url URL             URL GitLab инстанса (по умолчанию: gitlab.com)
-t, --token TOKEN         GitLab токен (по умолчанию: из GITLAB_TOKEN)
-m, --milestones M...     Список milestones для связи
--no-auto-notes           Не генерировать автоматические заметки
-v, --verbose             Подробный вывод
```

## 📋 Формат файла проектов

```
# Комментарии начинаются с #
# Формат: namespace/project

# Простые проекты
username/project1
username/project2

# Групповые проекты
mycompany/backend
mycompany/frontend

# Вложенные группы
myorg/team1/service-a
myorg/team2/service-b
```

## 🎯 Примеры использования

### 1. Релизы для микросервисов компании

```bash
# projects.txt
company/backend-auth
company/backend-api
company/frontend-web
company/mobile-app

# Запуск
python create_releases_gitlab_advanced.py -f projects.txt
```

### 2. Self-hosted GitLab с milestones

```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.mycompany.com \
  -m "Q4 2024" "Release 1.0"
```

### 3. Быстрый релиз одного проекта

```bash
python create_releases_gitlab_advanced.py -p myusername/urgent-fix
```

### 4. Релизы для команды

```bash
# team_projects.txt
engineering/team-alpha/service1
engineering/team-alpha/service2
engineering/team-beta/service3

python create_releases_gitlab_advanced.py -f team_projects.txt -v
```

## 🔐 Безопасность токенов

### ✅ Правильно:
```bash
# Используйте переменные окружения
export GITLAB_TOKEN='glpat-xxx'
python create_releases_gitlab_advanced.py -f projects.txt

# Или указывайте токен через CLI
python create_releases_gitlab_advanced.py -f projects.txt -t glpat-xxx
```

### ❌ Неправильно:
```bash
# НЕ коммитьте токен в код!
# НЕ сохраняйте токен в открытом виде в файлах!
```

## 🔄 GitLab CI/CD интеграция

Пример `.gitlab-ci.yml`:

```yaml
create-releases:
  stage: deploy
  image: python:3.10
  script:
    - pip install requests
    - python create_releases_gitlab_advanced.py -f projects.txt
  only:
    - tags
  variables:
    GITLAB_TOKEN: $CI_JOB_TOKEN  # или используйте Project Access Token
```

## 🆚 Сравнение с GitHub версией

| Параметр | GitHub | GitLab |
|----------|--------|--------|
| Токен | `GITHUB_TOKEN` | `GITLAB_TOKEN` |
| Префикс токена | `ghp_` | `glpat-` |
| Формат пути | `owner/repo` | `namespace/project` |
| API версия | v3 | v4 |
| Черновики | ✅ Да | ❌ Нет |
| Пре-релизы | ✅ Да | ❌ Нет |
| Milestones | ❌ Нет | ✅ Да |
| Вложенные группы | ❌ Нет | ✅ Да |
| Self-hosted | ❌ Нет | ✅ Да |

## 🐛 Решение проблем

### "401 Unauthorized"
- Проверьте, что токен правильный и не истек
- Убедитесь, что токен имеет права `api`
- Для self-hosted: проверьте URL инстанса

### "404 Project Not Found"
- Проверьте правильность пути к проекту
- Убедитесь, что у вас есть доступ к проекту
- Для вложенных групп используйте полный путь: `group/subgroup/project`

### "Нет тегов в проекте"
```bash
# Создайте тег
git tag v1.0.0
git push origin v1.0.0

# Или через GitLab UI: Repository → Tags → New tag
```

### "SSL Certificate Verify Failed" (self-hosted)
Если используете самоподписанный сертификат:
```python
# В начале скрипта добавьте:
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## 📊 Пример вывода

```
🚀 Начинаем создание релизов в GitLab (https://gitlab.com)...

============================================================

📦 Обработка username/project1...
✓ Найден тег v1.2.3 в username/project1
✅ Релиз v1.2.3 создан в username/project1
   URL: https://gitlab.com/username/project1/-/releases/v1.2.3

📦 Обработка mygroup/backend...
⚠️  Релиз для тега v2.0.0 уже существует в mygroup/backend

============================================================

📊 Итоги:
   ✅ Успешно создано: 1
   ⏭️  Пропущено (уже существуют): 1
   ❌ Ошибок: 0
   📦 Всего проектов: 2
```

## 🤝 Использование как модуль

```python
from create_releases_gitlab_advanced import GitLabReleaseManager

# GitLab.com
manager = GitLabReleaseManager('glpat-your_token')

# Self-hosted GitLab
manager = GitLabReleaseManager(
    'glpat-your_token',
    gitlab_url='https://gitlab.company.com'
)

# Создание релиза
manager.process_repository(
    'username/project',
    auto_notes=True,
    milestones=['v1.0', 'Q4']
)
```

## 📝 Структура проекта GitLab

```
namespace/
├── project1/           # Простой проект
├── project2/
└── group/              # Группа проектов
    ├── subgroup1/      # Подгруппа
    │   └── service-a/
    └── subgroup2/
        └── service-b/
```

Все эти проекты можно обрабатывать:
```
namespace/project1
namespace/project2
namespace/group/subgroup1/service-a
namespace/group/subgroup2/service-b
```

## 🎓 Дополнительная информация

- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [GitLab Releases API](https://docs.gitlab.com/ee/api/releases/)
- [Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

## 📄 Лицензия

MIT License
