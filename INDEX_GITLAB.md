# 🦊 GitLab Release Creator - Все файлы

## 🎯 Главное

Автоматическое создание релизов в нескольких **GitLab** проектах на основе последнего тега.

✅ **GitLab.com** (облачная версия)  
✅ **Self-hosted GitLab** (корпоративный инстанс)  
✅ **Community & Enterprise Edition**

## 📥 Скачать всё сразу

- **[gitlab-release-creator.zip](computer:///mnt/user-data/outputs/gitlab-release-creator.zip)** - Архив для Windows (24 KB)
- **[gitlab-release-creator.tar.gz](computer:///mnt/user-data/outputs/gitlab-release-creator.tar.gz)** - Архив для Linux/Mac (9.4 KB)

## 📄 Отдельные файлы GitLab

### Основные скрипты
- **[create_releases_gitlab.py](computer:///mnt/user-data/outputs/create_releases_gitlab.py)** - Простой базовый скрипт
- **[create_releases_gitlab_advanced.py](computer:///mnt/user-data/outputs/create_releases_gitlab_advanced.py)** - Расширенная версия с CLI

### Конфигурация
- **[gitlab_projects.txt](computer:///mnt/user-data/outputs/gitlab_projects.txt)** - Пример файла с проектами
- **[requirements.txt](computer:///mnt/user-data/outputs/requirements.txt)** - Python зависимости (общий)

### Документация GitLab
- **[QUICKSTART_GITLAB.md](computer:///mnt/user-data/outputs/QUICKSTART_GITLAB.md)** - Быстрый старт за 60 секунд
- **[README_GITLAB.md](computer:///mnt/user-data/outputs/README_GITLAB.md)** - Полная документация для GitLab

## 🚀 Быстрый старт (60 секунд!)

```bash
# 1. Скачайте и распакуйте архив
unzip gitlab-release-creator.zip

# 2. Установите зависимости
pip install requests

# 3. Получите токен на https://gitlab.com/-/profile/personal_access_tokens
#    Выберите права: api

# 4. Настройте токен
export GITLAB_TOKEN='glpat-ваш_токен'

# 5. Создайте список проектов
cat > projects.txt << EOF
username/project1
username/project2
EOF

# 6. Запустите!
python create_releases_gitlab_advanced.py -f projects.txt
```

## 🏢 Self-hosted GitLab

Для корпоративного GitLab:

```bash
export GITLAB_TOKEN='glpat-ваш_токен'
export GITLAB_URL='https://gitlab.your-company.com'

python create_releases_gitlab_advanced.py -f projects.txt
```

Или через параметры:
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.your-company.com
```

## ✨ Основные команды

```bash
# Базовое использование
python create_releases_gitlab_advanced.py -f projects.txt

# Конкретные проекты
python create_releases_gitlab_advanced.py -p user/proj1 group/proj2

# Self-hosted GitLab
python create_releases_gitlab_advanced.py -f projects.txt -u https://gitlab.company.com

# С milestones
python create_releases_gitlab_advanced.py -f projects.txt -m "v1.0" "Q4"

# Без автозаметок
python create_releases_gitlab_advanced.py -f projects.txt --no-auto-notes

# Подробный вывод
python create_releases_gitlab_advanced.py -f projects.txt -v

# Справка
python create_releases_gitlab_advanced.py --help
```

## 🆚 Отличия от GitHub версии

| Параметр | GitHub | GitLab |
|----------|--------|--------|
| **Токен** | `GITHUB_TOKEN` | `GITLAB_TOKEN` |
| **Префикс** | `ghp_` | `glpat-` |
| **URL токена** | github.com/settings/tokens | gitlab.com/-/profile/personal_access_tokens |
| **Права токена** | `repo` | `api` |
| **Self-hosted** | ❌ Нет | ✅ Да |
| **Вложенные группы** | ❌ Нет | ✅ Да (`group/subgroup/project`) |
| **Milestones** | ❌ Нет | ✅ Да |
| **Черновики** | ✅ Да | ❌ Нет |

## 📁 Формат файла projects.txt

```
# Простые проекты
username/project1
username/project2

# Групповые проекты
mycompany/backend-api
mycompany/frontend-web

# Вложенные группы (только в GitLab!)
myorg/team1/microservice-a
myorg/team2/microservice-b
myorg/platform/services/auth
```

## 🎯 Что выбрать?

### Простой скрипт (create_releases_gitlab.py)
✅ Минимальная настройка  
✅ Редактируете список проектов в коде  
✅ Подходит для разового использования  

```python
# Откройте файл и измените:
projects = [
    'username/project1',
    'mygroup/backend',
]
```

### Продвинутый скрипт (create_releases_gitlab_advanced.py)
✅ CLI интерфейс  
✅ Конфигурационные файлы  
✅ Больше опций  
✅ Подходит для регулярного использования и CI/CD  

```bash
python create_releases_gitlab_advanced.py -f projects.txt
```

## 🎭 Примеры использования

### 1. Релизы микросервисов
```bash
# projects.txt
company/auth-service
company/payment-service
company/notification-service

python create_releases_gitlab_advanced.py -f projects.txt
```

### 2. Корпоративный GitLab с milestone
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.company.com \
  -m "Release 2.0" "Q4 2024"
```

### 3. Быстрый релиз одного проекта
```bash
python create_releases_gitlab_advanced.py -p username/urgent-fix
```

## 🐛 Решение проблем

| Проблема | Решение |
|----------|---------|
| `401 Unauthorized` | Проверьте токен (должен быть `glpat-xxx`) и права `api` |
| `404 Not Found` | Проверьте путь проекта: `namespace/project` |
| `No module named 'requests'` | `pip install requests` |
| `Нет тегов` | Создайте тег: `git tag v1.0.0 && git push origin v1.0.0` |
| SSL ошибки (self-hosted) | См. документацию README_GITLAB.md |

## 📖 Документация

1. **QUICKSTART_GITLAB.md** - начните здесь! Запуск за 60 секунд
2. **README_GITLAB.md** - полная документация со всеми деталями
3. **gitlab_projects.txt** - пример конфигурационного файла

## 🔐 Безопасность

⚠️ **Важно:**
- Никогда не коммитьте токен в репозиторий
- Используйте переменные окружения
- Регулярно обновляйте токены
- Для CI/CD используйте Project Access Tokens

## 🔄 GitLab CI/CD

Пример автоматизации в `.gitlab-ci.yml`:

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
    GITLAB_TOKEN: $CI_JOB_TOKEN
```

## 🎓 Дополнительные возможности GitLab

- ✅ Поддержка вложенных групп (`group/subgroup/project`)
- ✅ Связывание релизов с milestones
- ✅ Self-hosted инстансы
- ✅ Community и Enterprise Edition

## 🚀 GitHub версия тоже доступна!

Если у вас проекты в GitHub, используйте:
- **[INDEX.md](computer:///mnt/user-data/outputs/INDEX.md)** - GitHub версия скриптов

---

**Создано для автоматизации GitLab релизов** 🦊🚀

Начните с **QUICKSTART_GITLAB.md** прямо сейчас!
