# 🚀 Release Creator - Автоматизация релизов

Автоматическое создание релизов на основе последнего тега для **GitHub** и **GitLab**.

---

## ⚡ Начните здесь!

### 🐙 У вас проекты в **GitHub**?

**[→ INDEX.md - GitHub версия](computer:///mnt/user-data/outputs/INDEX.md)**

📦 Скачать: [github-release-creator.zip](computer:///mnt/user-data/outputs/github-release-creator.zip) (15 KB)

### 🦊 У вас проекты в **GitLab**?

**[→ INDEX_GITLAB.md - GitLab версия](computer:///mnt/user-data/outputs/INDEX_GITLAB.md)**

📦 Скачать: [gitlab-release-creator.zip](computer:///mnt/user-data/outputs/gitlab-release-creator.zip) (24 KB)

### 🔀 У вас проекты в обеих платформах?

**[→ COMPLETE_GUIDE.md - Полное руководство](computer:///mnt/user-data/outputs/COMPLETE_GUIDE.md)**

---

## 📁 Структура проекта

### GitHub версия
- `create_releases.py` - Простой скрипт
- `create_releases_advanced.py` - CLI версия
- `repositories.txt` - Конфиг для репозиториев
- `README.md` - Документация
- `QUICKSTART.md` - Быстрый старт

### GitLab версия
- `create_releases_gitlab.py` - Простой скрипт
- `create_releases_gitlab_advanced.py` - CLI версия
- `gitlab_projects.txt` - Конфиг для проектов
- `README_GITLAB.md` - Документация
- `QUICKSTART_GITLAB.md` - Быстрый старт

### Общие файлы
- `requirements.txt` - Python зависимости
- `INDEX.md` - GitHub главная страница
- `INDEX_GITLAB.md` - GitLab главная страница
- `COMPLETE_GUIDE.md` - Полное руководство
- `PROJECT_OVERVIEW.md` - Обзор проекта

---

## 🚀 Быстрый старт

### GitHub (30 секунд)

```bash
# 1. Токен с https://github.com/settings/tokens (права: repo)
export GITHUB_TOKEN='ghp_your_token'

# 2. Установка
pip install requests

# 3. Создайте repositories.txt
echo "username/repo1" > repositories.txt

# 4. Запуск
python create_releases_advanced.py -f repositories.txt
```

### GitLab (60 секунд)

```bash
# 1. Токен с https://gitlab.com/-/profile/personal_access_tokens (права: api)
export GITLAB_TOKEN='glpat-your_token'

# Для self-hosted:
# export GITLAB_URL='https://gitlab.company.com'

# 2. Установка
pip install requests

# 3. Создайте gitlab_projects.txt
echo "username/project1" > gitlab_projects.txt

# 4. Запуск
python create_releases_gitlab_advanced.py -f gitlab_projects.txt
```

---

## 📊 Сравнение платформ

| | GitHub 🐙 | GitLab 🦊 |
|---|---|---|
| **Токен** | `GITHUB_TOKEN` | `GITLAB_TOKEN` |
| **URL** | github.com/settings/tokens | gitlab.com/-/profile/personal_access_tokens |
| **Права** | `repo` | `api` |
| **Скрипт** | `create_releases_advanced.py` | `create_releases_gitlab_advanced.py` |
| **Self-hosted** | ❌ | ✅ |
| **Вложенные группы** | ❌ | ✅ |
| **Черновики** | ✅ | ❌ |
| **Milestones** | ❌ | ✅ |

---

## ✨ Возможности

- ✅ Автоматическое создание релизов на основе последнего тега
- ✅ Генерация release notes из коммитов
- ✅ Проверка существующих релизов (избегает дубликатов)
- ✅ Обработка множества репозиториев/проектов
- ✅ CLI интерфейс с гибкими опциями
- ✅ Конфигурационные файлы
- ✅ Поддержка GitHub и GitLab
- ✅ Self-hosted GitLab
- ✅ Детальное логирование

---

## 📖 Документация

### Для начинающих
1. **INDEX.md** (GitHub) или **INDEX_GITLAB.md** (GitLab) - начните здесь
2. **QUICKSTART.md** / **QUICKSTART_GITLAB.md** - быстрый старт
3. Создайте первый релиз!

### Для опытных
1. **README.md** / **README_GITLAB.md** - полная документация
2. **COMPLETE_GUIDE.md** - работа с обеими платформами
3. **PROJECT_OVERVIEW.md** - обзор архитектуры

---

## 💡 Примеры использования

### GitHub: Релиз всех микросервисов

```bash
# repositories.txt
company/auth-service
company/payment-service
company/notification-service

python create_releases_advanced.py -f repositories.txt
```

### GitLab: Корпоративный инстанс

```bash
# gitlab_projects.txt
engineering/backend/auth
engineering/backend/api
engineering/frontend/web

python create_releases_gitlab_advanced.py \
  -f gitlab_projects.txt \
  -u https://gitlab.company.com
```

### Обе платформы одновременно

```bash
#!/bin/bash
export GITHUB_TOKEN='ghp_xxx'
export GITLAB_TOKEN='glpat-xxx'

python create_releases_advanced.py -f repositories.txt
python create_releases_gitlab_advanced.py -f gitlab_projects.txt
```

---

## 🎯 Выбор варианта

### Простые скрипты
**Когда использовать:** Разовые задачи, мало репозиториев

- GitHub: `create_releases.py`
- GitLab: `create_releases_gitlab.py`

Редактируете список в коде и запускаете.

### Продвинутые скрипты (рекомендуется)
**Когда использовать:** Регулярное использование, много репозиториев, CI/CD

- GitHub: `create_releases_advanced.py`
- GitLab: `create_releases_gitlab_advanced.py`

CLI интерфейс, конфигурационные файлы, больше опций.

---

## 📥 Что скачать?

### Только GitHub
[github-release-creator.zip](computer:///mnt/user-data/outputs/github-release-creator.zip) (15 KB)

### Только GitLab
[gitlab-release-creator.zip](computer:///mnt/user-data/outputs/gitlab-release-creator.zip) (24 KB)

### Всё вместе
Скачайте оба архива или все отдельные файлы из этой директории.

---

## 🔧 Требования

- Python 3.7+
- Пакет `requests`
- GitHub Personal Access Token (для GitHub)
- GitLab Personal Access Token (для GitLab)

---

## 🐛 Решение проблем

### "No module named 'requests'"
```bash
pip install requests
```

### "401 Unauthorized"
Проверьте токен и его права:
- GitHub: `repo`
- GitLab: `api`

### "404 Not Found"
Проверьте пути к репозиториям/проектам и доступ к ним.

### "Нет тегов"
Создайте тег:
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## 🔐 Безопасность

⚠️ **Важно:**
- Не коммитьте токены в репозиторий
- Используйте переменные окружения
- Регулярно обновляйте токены
- Храните токены в безопасном месте

---

## 📞 Навигация

### GitHub
- [INDEX.md](computer:///mnt/user-data/outputs/INDEX.md) - Главная страница GitHub
- [README.md](computer:///mnt/user-data/outputs/README.md) - Документация
- [QUICKSTART.md](computer:///mnt/user-data/outputs/QUICKSTART.md) - Быстрый старт
- [create_releases.py](computer:///mnt/user-data/outputs/create_releases.py) - Простой скрипт
- [create_releases_advanced.py](computer:///mnt/user-data/outputs/create_releases_advanced.py) - CLI скрипт

### GitLab
- [INDEX_GITLAB.md](computer:///mnt/user-data/outputs/INDEX_GITLAB.md) - Главная страница GitLab
- [README_GITLAB.md](computer:///mnt/user-data/outputs/README_GITLAB.md) - Документация
- [QUICKSTART_GITLAB.md](computer:///mnt/user-data/outputs/QUICKSTART_GITLAB.md) - Быстрый старт
- [create_releases_gitlab.py](computer:///mnt/user-data/outputs/create_releases_gitlab.py) - Простой скрипт
- [create_releases_gitlab_advanced.py](computer:///mnt/user-data/outputs/create_releases_gitlab_advanced.py) - CLI скрипт

### Общее
- [COMPLETE_GUIDE.md](computer:///mnt/user-data/outputs/COMPLETE_GUIDE.md) - Полное руководство
- [PROJECT_OVERVIEW.md](computer:///mnt/user-data/outputs/PROJECT_OVERVIEW.md) - Обзор проекта
- [requirements.txt](computer:///mnt/user-data/outputs/requirements.txt) - Зависимости

---

## 📊 Статистика проекта

- **Всего файлов:** 19
- **Скрипты:** 4 (2 для GitHub, 2 для GitLab)
- **Документация:** 8 файлов
- **Архивы:** 4 (zip + tar.gz для каждой платформы)
- **Размер:** ~176 KB

---

## 🎓 Следующие шаги

1. ✅ **Выберите платформу** (GitHub или GitLab)
2. 📥 **Скачайте** соответствующий архив
3. 📖 **Прочитайте** QUICKSTART
4. 🚀 **Создайте** первый релиз
5. 🔄 **Автоматизируйте** через CI/CD
6. 📊 **Масштабируйте** на все проекты

---

## 📄 Лицензия

MIT License - используйте свободно!

---

**🚀 Начните прямо сейчас!**

Выберите вашу платформу и перейдите к соответствующей документации.

**GitHub:** [INDEX.md](computer:///mnt/user-data/outputs/INDEX.md)  
**GitLab:** [INDEX_GITLAB.md](computer:///mnt/user-data/outputs/INDEX_GITLAB.md)  
**Обе платформы:** [COMPLETE_GUIDE.md](computer:///mnt/user-data/outputs/COMPLETE_GUIDE.md)
