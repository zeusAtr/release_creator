#!/usr/bin/env python3
"""
Скрипт для создания релизов в нескольких GitLab репозиториях
на основе последнего тега в каждом репозитории.
"""

import os
import sys
import requests
from typing import List, Dict, Optional
from urllib.parse import quote


class GitLabReleaseManager:
    def __init__(self, token: str, gitlab_url: str = 'https://gitlab.com'):
        """
        Инициализация менеджера релизов.
        
        Args:
            token: GitLab Personal Access Token с правами api
            gitlab_url: URL GitLab инстанса (по умолчанию gitlab.com)
        """
        self.token = token
        self.gitlab_url = gitlab_url.rstrip('/')
        self.headers = {
            'PRIVATE-TOKEN': token,
            'Content-Type': 'application/json'
        }
        self.api_url = f'{self.gitlab_url}/api/v4'
    
    def get_project_id(self, project_path: str) -> Optional[str]:
        """
        Получает ID проекта по его пути.
        
        Args:
            project_path: Путь к проекту (namespace/project)
            
        Returns:
            ID проекта или None
        """
        # URL-encode путь проекта
        encoded_path = quote(project_path, safe='')
        url = f'{self.api_url}/projects/{encoded_path}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            project = response.json()
            return str(project['id'])
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при получении ID проекта {project_path}: {e}")
            return None
    
    def get_latest_tag(self, project_id: str, project_path: str) -> Optional[Dict]:
        """
        Получает последний тег из проекта.
        
        Args:
            project_id: ID проекта
            project_path: Путь к проекту (для отображения)
            
        Returns:
            Словарь с информацией о теге или None
        """
        url = f'{self.api_url}/projects/{project_id}/repository/tags'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tags = response.json()
            if not tags:
                print(f"⚠️  Нет тегов в проекте {project_path}")
                return None
            
            # Возвращаем первый тег (самый последний)
            latest_tag = tags[0]
            print(f"✓ Найден тег {latest_tag['name']} в {project_path}")
            return latest_tag
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при получении тегов из {project_path}: {e}")
            return None
    
    def check_release_exists(self, project_id: str, tag_name: str) -> bool:
        """
        Проверяет, существует ли релиз для данного тега.
        
        Args:
            project_id: ID проекта
            tag_name: Название тега
            
        Returns:
            True если релиз существует, False если нет
        """
        url = f'{self.api_url}/projects/{project_id}/releases/{tag_name}'
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_commits_since_previous_tag(self, project_id: str, 
                                       current_tag: str, 
                                       previous_tag: Optional[str]) -> List[Dict]:
        """
        Получает список коммитов между двумя тегами.
        
        Args:
            project_id: ID проекта
            current_tag: Текущий тег
            previous_tag: Предыдущий тег (если есть)
            
        Returns:
            Список коммитов
        """
        if not previous_tag:
            return []
        
        url = f'{self.api_url}/projects/{project_id}/repository/compare'
        params = {
            'from': previous_tag,
            'to': current_tag
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('commits', [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Не удалось получить коммиты: {e}")
            return []
    
    def generate_release_notes(self, commits: List[Dict], tag_name: str, 
                              project_path: str) -> str:
        """
        Генерирует описание релиза на основе коммитов.
        
        Args:
            commits: Список коммитов
            tag_name: Название тега
            project_path: Путь к проекту
            
        Returns:
            Текст описания релиза
        """
        if not commits:
            return f"Release {tag_name}"
        
        notes = [f"## What's Changed in {tag_name}\n"]
        
        for commit in commits:
            message = commit['message'].split('\n')[0]  # Первая строка
            author = commit['author_name']
            short_id = commit['short_id']
            notes.append(f"- {message} ({short_id}) by {author}")
        
        notes.append(f"\n**Full Changelog**: {self.gitlab_url}/{project_path}/-/compare/{tag_name}?from=&to={tag_name}")
        
        return '\n'.join(notes)
    
    def create_release(self, project_id: str, project_path: str, tag_name: str, 
                      name: Optional[str] = None, description: Optional[str] = None,
                      milestones: Optional[List[str]] = None) -> Optional[Dict]:
        """
        Создает релиз в проекте GitLab.
        
        Args:
            project_id: ID проекта
            project_path: Путь к проекту (для отображения)
            tag_name: Название тега для релиза
            name: Название релиза (по умолчанию = tag_name)
            description: Описание релиза
            milestones: Список названий milestone для связи с релизом
            
        Returns:
            Словарь с информацией о созданном релизе или None
        """
        url = f'{self.api_url}/projects/{project_id}/releases'
        
        # Проверяем, существует ли уже релиз
        if self.check_release_exists(project_id, tag_name):
            print(f"⚠️  Релиз для тега {tag_name} уже существует в {project_path}")
            return None
        
        payload = {
            'tag_name': tag_name,
            'name': name or tag_name,
            'description': description or f'Release {tag_name}'
        }
        
        if milestones:
            payload['milestones'] = milestones
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            release = response.json()
            print(f"✅ Релиз {tag_name} создан в {project_path}")
            print(f"   URL: {release['_links']['self']}")
            return release
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при создании релиза в {project_path}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Ответ: {e.response.text}")
            return None
    
    def process_repository(self, project_path: str, 
                          auto_notes: bool = True,
                          milestones: Optional[List[str]] = None) -> bool:
        """
        Обрабатывает один проект: находит последний тег и создает релиз.
        
        Args:
            project_path: Путь к проекту (namespace/project)
            auto_notes: Автоматически генерировать описание релиза
            milestones: Список milestone для связи с релизом
            
        Returns:
            True если релиз создан успешно, False если нет
        """
        print(f"\n📦 Обработка {project_path}...")
        
        # Получаем ID проекта
        project_id = self.get_project_id(project_path)
        if not project_id:
            return False
        
        # Получаем последний тег
        latest_tag = self.get_latest_tag(project_id, project_path)
        if not latest_tag:
            return False
        
        tag_name = latest_tag['name']
        
        # Генерируем описание релиза если нужно
        description = None
        if auto_notes:
            # Получаем все теги для поиска предыдущего
            url = f'{self.api_url}/projects/{project_id}/repository/tags'
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                tags = response.json()
                
                previous_tag = tags[1]['name'] if len(tags) > 1 else None
                commits = self.get_commits_since_previous_tag(project_id, tag_name, previous_tag)
                description = self.generate_release_notes(commits, tag_name, project_path)
            except Exception as e:
                print(f"⚠️  Не удалось сгенерировать автоматические заметки: {e}")
        
        # Создаем релиз
        release = self.create_release(
            project_id, project_path, tag_name,
            name=tag_name,
            description=description,
            milestones=milestones
        )
        
        return release is not None


def main():
    """Основная функция скрипта."""
    
    # Получаем токен и URL из переменных окружения
    gitlab_token = os.getenv('GITLAB_TOKEN')
    gitlab_url = os.getenv('GITLAB_URL', 'https://gitlab.com')
    
    if not gitlab_token:
        print("❌ Ошибка: Не найдена переменная окружения GITLAB_TOKEN")
        print("   Создайте токен на https://gitlab.com/-/profile/personal_access_tokens")
        print("   Токен должен иметь права: api")
        print("   и установите переменную: export GITLAB_TOKEN='your_token'")
        print("\n   Для self-hosted GitLab также установите:")
        print("   export GITLAB_URL='https://gitlab.your-company.com'")
        sys.exit(1)
    
    # Список проектов для обработки
    # Формат: 'namespace/project' или 'group/subgroup/project'
    projects = [
        'username/project1',
        'username/project2',
        'group/project3',
        # Добавьте свои проекты здесь
    ]
    
    # Настройки
    auto_notes = True      # Автоматически генерировать описание релиза
    milestones = None      # Список milestone для связи (например: ['v1.0', 'MVP'])
    
    # Создаем менеджер релизов
    manager = GitLabReleaseManager(gitlab_token, gitlab_url)
    
    # Статистика
    successful = 0
    failed = 0
    
    print(f"🚀 Начинаем создание релизов в GitLab ({gitlab_url})...\n")
    print("=" * 60)
    
    # Обрабатываем каждый проект
    for project_path in projects:
        if manager.process_repository(project_path, auto_notes, milestones):
            successful += 1
        else:
            failed += 1
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print(f"\n📊 Итоги:")
    print(f"   ✅ Успешно создано: {successful}")
    print(f"   ❌ Ошибок: {failed}")
    print(f"   📦 Всего проектов: {len(projects)}")


if __name__ == '__main__':
    main()
