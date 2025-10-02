# GitLab Release Creator - Быстрый старт 🚀

## ⚡ За 60 секунд

### 1. Получите токен (15 сек)
Перейдите: https://gitlab.com/-/profile/personal_access_tokens
- Создайте токен с правами **api**
- Скопируйте токен (начинается с `glpat-`)

### 2. Установите зависимости (10 сек)
```bash
pip install requests
```

### 3. Настройте токен (5 сек)
```bash
export GITLAB_TOKEN='glpat-ваш_токен_здесь'
```

### 4. Создайте список проектов (15 сек)
```bash
cat > projects.txt << EOF
username/project1
username/project2
EOF
```

### 5. Запустите! (15 сек)
```bash
python create_releases_gitlab_advanced.py -f projects.txt
```

Готово! 🎉

---

## 🎯 Два варианта использования

### Вариант A: Простой скрипт

**Когда использовать:** Разовая задача, мало проектов

```python
# Откройте create_releases_gitlab.py
# Измените список:
projects = [
    'username/my-project',
    'mygroup/backend',
]

# Запустите:
python create_releases_gitlab.py
```

### Вариант B: Продвинутый скрипт

**Когда использовать:** Регулярное использование, много проектов, CI/CD

```bash
# 1. Создайте projects.txt
echo "username/project1" > projects.txt
echo "username/project2" >> projects.txt

# 2. Запустите
python create_releases_gitlab_advanced.py -f projects.txt
```

---

## 🏢 Self-hosted GitLab?

Если у вас свой инстанс GitLab:

```bash
# Установите URL вашего GitLab
export GITLAB_URL='https://gitlab.your-company.com'
export GITLAB_TOKEN='glpat-your_token'

# Запустите
python create_releases_gitlab_advanced.py -f projects.txt
```

Или через параметр:
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.your-company.com
```

---

## 💡 Популярные команды

```bash
# Базовое использование
python create_releases_gitlab_advanced.py -f projects.txt

# Конкретные проекты
python create_releases_gitlab_advanced.py -p user/proj1 group/proj2

# Self-hosted GitLab
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.company.com

# С milestones
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -m "v1.0" "Q4 Release"

# Без автоматических заметок
python create_releases_gitlab_advanced.py -f projects.txt --no-auto-notes

# Подробный вывод
python create_releases_gitlab_advanced.py -f projects.txt -v

# Справка
python create_releases_gitlab_advanced.py --help
```

---

## 📁 Формат файла projects.txt

```
# Простые проекты
username/project1
username/project2

# Групповые проекты
mycompany/backend
mycompany/frontend

# Вложенные группы (GitLab поддерживает!)
myorg/team1/microservice-a
myorg/team2/microservice-b
```

---

## 🆚 GitLab vs GitHub

| Что | GitHub | GitLab |
|-----|--------|--------|
| **Токен** | `export GITHUB_TOKEN='ghp_xxx'` | `export GITLAB_TOKEN='glpat-xxx'` |
| **Скрипт** | `create_releases_advanced.py` | `create_releases_gitlab_advanced.py` |
| **Файл** | `repositories.txt` | `gitlab_projects.txt` |
| **Self-hosted** | ❌ Нет | ✅ Да |
| **Вложенные группы** | ❌ Нет | ✅ Да |
| **Milestones** | ❌ Нет | ✅ Да |

---

## 🎭 Примеры для разных ситуаций

### Релиз всех микросервисов компании
```bash
# projects.txt
company/auth-service
company/payment-service
company/notification-service
company/analytics-service

python create_releases_gitlab_advanced.py -f projects.txt
```

### Релиз проектов одной команды
```bash
python create_releases_gitlab_advanced.py \
  -p myorg/team-alpha/service1 myorg/team-alpha/service2
```

### Релиз с привязкой к milestone
```bash
# Связываем релизы с milestone "v2.0"
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -m "v2.0"
```

### Корпоративный GitLab с подробным выводом
```bash
python create_releases_gitlab_advanced.py \
  -f projects.txt \
  -u https://gitlab.company.com \
  -v
```

---

## 🐛 Частые проблемы и решения

### ❌ "401 Unauthorized"
**Проблема:** Неверный токен или нет прав

**Решение:**
1. Проверьте токен: должен начинаться с `glpat-`
2. Убедитесь, что выбраны права **api**
3. Токен не истек

### ❌ "404 Project Not Found"
**Проблема:** Неправильный путь или нет доступа

**Решение:**
1. Проверьте путь: `username/project` (без пробелов)
2. Убедитесь, что у вас есть доступ к проекту
3. Для вложенных групп: `group/subgroup/project`

### ❌ "No module named 'requests'"
**Решение:**
```bash
pip install requests
```

### ❌ "Нет тегов в проекте"
**Решение:**
```bash
# Создайте тег
git tag v1.0.0
git push origin v1.0.0

# Или через GitLab UI: Repository → Tags → New tag
```

---

## 🔧 Настройки в скриптах

### Простой скрипт (create_releases_gitlab.py):
```python
# Список проектов
projects = [
    'username/project1',
    'mygroup/project2',
]

# Настройки
auto_notes = True      # Генерировать release notes
milestones = None      # Или ['v1.0', 'MVP']
```

### Продвинутый скрипт (CLI):
```bash
# Все настройки через параметры командной строки
python create_releases_gitlab_advanced.py -f projects.txt [опции]
```

---

## 🎓 Что дальше?

1. ✅ **Начните с простого:** Запустите базовый скрипт для 1-2 проектов
2. 📖 **Изучите документацию:** Прочитайте README_GITLAB.md
3. 🔄 **Автоматизируйте:** Настройте GitLab CI/CD (см. пример ниже)
4. 🚀 **Масштабируйте:** Используйте для всех проектов компании

---

## 🔄 Автоматизация через GitLab CI/CD

Создайте `.gitlab-ci.yml`:

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

---

## 📞 Нужна помощь?

```bash
# Справка по скрипту
python create_releases_gitlab_advanced.py --help

# Проверка версии Python
python --version  # Нужен Python 3.7+

# Проверка установки requests
python -c "import requests; print(requests.__version__)"
```

---

## ✨ Совет профессионалам

Создайте алиас для быстрого запуска:

```bash
# Добавьте в ~/.bashrc или ~/.zshrc
alias gitlab-release='python /path/to/create_releases_gitlab_advanced.py'

# Теперь можно использовать:
gitlab-release -f projects.txt
gitlab-release -p username/project
```

---

**Начните прямо сейчас!** 🎯

1. Получите токен
2. `pip install requests`
3. `export GITLAB_TOKEN='your_token'`
4. Создайте `projects.txt`
5. `python create_releases_gitlab_advanced.py -f projects.txt`

Готово! 🚀
