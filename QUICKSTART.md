# Быстрый старт 🚀

## Вариант 1: Простой скрипт (create_releases.py)

### Шаг 1: Установка
```bash
pip install requests
```

### Шаг 2: Настройка токена
```bash
export GITHUB_TOKEN='ghp_your_token_here'
```

### Шаг 3: Редактирование списка репозиториев
Откройте `create_releases.py` и измените:
```python
repositories = [
    ('your-username', 'repo1'),
    ('your-username', 'repo2'),
    ('organization', 'repo3'),
]
```

### Шаг 4: Запуск
```bash
python create_releases.py
```

---

## Вариант 2: Продвинутый скрипт (create_releases_advanced.py)

### Способ A: Использование файла конфигурации

#### 1. Создайте файл repositories.txt
```
username/project1
username/project2
organization/backend-api
organization/frontend-app
```

#### 2. Запустите скрипт
```bash
python create_releases_advanced.py -f repositories.txt
```

### Способ B: Указание репозиториев напрямую

```bash
python create_releases_advanced.py -r username/repo1 username/repo2 org/repo3
```

### Дополнительные опции

**Создать черновики (для проверки перед публикацией):**
```bash
python create_releases_advanced.py -f repositories.txt --draft
```

**Создать пре-релизы (beta/alpha):**
```bash
python create_releases_advanced.py -f repositories.txt --prerelease
```

**Без автоматических заметок:**
```bash
python create_releases_advanced.py -f repositories.txt --no-auto-notes
```

**Указать токен явно:**
```bash
python create_releases_advanced.py -f repositories.txt -t ghp_yourtoken
```

**Подробный вывод:**
```bash
python create_releases_advanced.py -f repositories.txt -v
```

**Комбинирование опций:**
```bash
python create_releases_advanced.py -r owner/repo --draft --prerelease -v
```

---

## Примеры использования

### Создание релизов для всех проектов компании
```bash
# repositories.txt
mycompany/backend
mycompany/frontend
mycompany/mobile-app
mycompany/api-gateway

# Запуск
python create_releases_advanced.py -f repositories.txt
```

### Создание beta-релизов
```bash
python create_releases_advanced.py \
  -r myproject/core myproject/plugins \
  --prerelease
```

### Быстрое создание для одного проекта
```bash
python create_releases_advanced.py -r username/my-project
```

---

## Частые сценарии

### 1. Еженедельный релиз всех микросервисов
```bash
#!/bin/bash
# weekly-release.sh

export GITHUB_TOKEN='your_token'
python create_releases_advanced.py -f microservices.txt -v
```

### 2. Создание release candidate
```bash
python create_releases_advanced.py \
  -f repositories.txt \
  --prerelease \
  --draft
# Проверьте черновики, затем опубликуйте вручную
```

### 3. Релиз только для определенных проектов
```bash
python create_releases_advanced.py \
  -r company/project-a company/project-b \
  --no-auto-notes
```

---

## Проверка перед запуском

✅ Убедитесь, что:
1. GitHub токен имеет права `repo`
2. У вас есть доступ ко всем репозиториям
3. В репозиториях есть теги
4. Python 3.7+ установлен
5. Установлен пакет `requests`

---

## Что делать если возникла ошибка?

### "No module named 'requests'"
```bash
pip install requests
```

### "401 Unauthorized"
- Проверьте токен
- Убедитесь, что токен не истек
- Проверьте права токена

### "404 Not Found"
- Проверьте правильность имени репозитория
- Убедитесь, что у вас есть доступ к репозиторию

### "Нет тегов в репозитории"
- Сначала создайте тег в репозитории:
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## Помощь

Справка по расширенному скрипту:
```bash
python create_releases_advanced.py --help
```
