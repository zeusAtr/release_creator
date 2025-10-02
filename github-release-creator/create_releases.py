#!/usr/bin/env python3
"""
Скрипт для создания релизов в нескольких GitHub репозиториях
на основе последнего тега в каждом репозитории.
"""

import os
import sys
import requests
from typing import List, Dict, Optional


class GitHubReleaseManager:
    def __init__(self, token: str):
        """
        Инициализация менеджера релизов.
        
        Args:
            token: GitHub Personal Access Token с правами repo
        """
        self.token = token
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def get_latest_tag(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Получает последний тег из репозитория.
        
        Args:
            owner: Владелец репозитория
            repo: Название репозитория
            
        Returns:
            Словарь с информацией о теге или None
        """
        url = f'{self.base_url}/repos/{owner}/{repo}/tags'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tags = response.json()
            if not tags:
                print(f"⚠️  Нет тегов в репозитории {owner}/{repo}")
                return None
            
            # Возвращаем первый тег (самый последний)
            latest_tag = tags[0]
            print(f"✓ Найден тег {latest_tag['name']} в {owner}/{repo}")
            return latest_tag
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при получении тегов из {owner}/{repo}: {e}")
            return None
    
    def check_release_exists(self, owner: str, repo: str, tag_name: str) -> bool:
        """
        Проверяет, существует ли релиз для данного тега.
        
        Args:
            owner: Владелец репозитория
            repo: Название репозитория
            tag_name: Название тега
            
        Returns:
            True если релиз существует, False если нет
        """
        url = f'{self.base_url}/repos/{owner}/{repo}/releases/tags/{tag_name}'
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_commits_since_previous_tag(self, owner: str, repo: str, 
                                       current_tag: str, previous_tag: Optional[str]) -> List[Dict]:
        """
        Получает список коммитов между двумя тегами.
        
        Args:
            owner: Владелец репозитория
            repo: Название репозитория
            current_tag: Текущий тег
            previous_tag: Предыдущий тег (если есть)
            
        Returns:
            Список коммитов
        """
        if not previous_tag:
            return []
        
        url = f'{self.base_url}/repos/{owner}/{repo}/compare/{previous_tag}...{current_tag}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('commits', [])
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Не удалось получить коммиты: {e}")
            return []
    
    def generate_release_notes(self, commits: List[Dict], tag_name: str) -> str:
        """
        Генерирует описание релиза на основе коммитов.
        
        Args:
            commits: Список коммитов
            tag_name: Название тега
            
        Returns:
            Текст описания релиза
        """
        if not commits:
            return f"Release {tag_name}"
        
        notes = [f"## What's Changed in {tag_name}\n"]
        
        for commit in commits:
            message = commit['commit']['message'].split('\n')[0]  # Первая строка
            author = commit['commit']['author']['name']
            sha = commit['sha'][:7]
            notes.append(f"- {message} ({sha}) by @{author}")
        
        notes.append(f"\n**Full Changelog**: {commits[0]['html_url'].rsplit('/', 1)[0]}/compare/{tag_name}")
        
        return '\n'.join(notes)
    
    def create_release(self, owner: str, repo: str, tag_name: str, 
                      name: Optional[str] = None, body: Optional[str] = None,
                      draft: bool = False, prerelease: bool = False) -> Optional[Dict]:
        """
        Создает релиз в репозитории.
        
        Args:
            owner: Владелец репозитория
            repo: Название репозитория
            tag_name: Название тега для релиза
            name: Название релиза (по умолчанию = tag_name)
            body: Описание релиза
            draft: Создать как черновик
            prerelease: Отметить как пре-релиз
            
        Returns:
            Словарь с информацией о созданном релизе или None
        """
        url = f'{self.base_url}/repos/{owner}/{repo}/releases'
        
        # Проверяем, существует ли уже релиз
        if self.check_release_exists(owner, repo, tag_name):
            print(f"⚠️  Релиз для тега {tag_name} уже существует в {owner}/{repo}")
            return None
        
        payload = {
            'tag_name': tag_name,
            'name': name or tag_name,
            'body': body or f'Release {tag_name}',
            'draft': draft,
            'prerelease': prerelease
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            release = response.json()
            print(f"✅ Релиз {tag_name} создан в {owner}/{repo}")
            print(f"   URL: {release['html_url']}")
            return release
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при создании релиза в {owner}/{repo}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Ответ: {e.response.text}")
            return None
    
    def process_repository(self, owner: str, repo: str, 
                          auto_notes: bool = True,
                          draft: bool = False,
                          prerelease: bool = False) -> bool:
        """
        Обрабатывает один репозиторий: находит последний тег и создает релиз.
        
        Args:
            owner: Владелец репозитория
            repo: Название репозитория
            auto_notes: Автоматически генерировать описание релиза
            draft: Создать как черновик
            prerelease: Отметить как пре-релиз
            
        Returns:
            True если релиз создан успешно, False если нет
        """
        print(f"\n📦 Обработка {owner}/{repo}...")
        
        # Получаем последний тег
        latest_tag = self.get_latest_tag(owner, repo)
        if not latest_tag:
            return False
        
        tag_name = latest_tag['name']
        
        # Генерируем описание релиза если нужно
        body = None
        if auto_notes:
            # Получаем все теги для поиска предыдущего
            url = f'{self.base_url}/repos/{owner}/{repo}/tags'
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                tags = response.json()
                
                previous_tag = tags[1]['name'] if len(tags) > 1 else None
                commits = self.get_commits_since_previous_tag(owner, repo, tag_name, previous_tag)
                body = self.generate_release_notes(commits, tag_name)
            except Exception as e:
                print(f"⚠️  Не удалось сгенерировать автоматические заметки: {e}")
        
        # Создаем релиз
        release = self.create_release(
            owner, repo, tag_name,
            name=tag_name,
            body=body,
            draft=draft,
            prerelease=prerelease
        )
        
        return release is not None


def main():
    """Основная функция скрипта."""
    
    # Получаем токен из переменной окружения
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Ошибка: Не найдена переменная окружения GITHUB_TOKEN")
        print("   Создайте токен на https://github.com/settings/tokens")
        print("   и установите переменную: export GITHUB_TOKEN='your_token'")
        sys.exit(1)
    
    # Список репозиториев для обработки
    # Формат: ('owner', 'repo')
    repositories = [
        ('owner1', 'repo1'),
        ('owner2', 'repo2'),
        ('owner3', 'repo3'),
        # Добавьте свои репозитории здесь
    ]
    
    # Настройки
    auto_notes = True      # Автоматически генерировать описание релиза
    draft = False          # Создавать как черновик
    prerelease = False     # Отмечать как пре-релиз
    
    # Создаем менеджер релизов
    manager = GitHubReleaseManager(github_token)
    
    # Статистика
    successful = 0
    failed = 0
    
    print("🚀 Начинаем создание релизов...\n")
    print("=" * 60)
    
    # Обрабатываем каждый репозиторий
    for owner, repo in repositories:
        if manager.process_repository(owner, repo, auto_notes, draft, prerelease):
            successful += 1
        else:
            failed += 1
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print(f"\n📊 Итоги:")
    print(f"   ✅ Успешно создано: {successful}")
    print(f"   ❌ Ошибок: {failed}")
    print(f"   📦 Всего репозиториев: {len(repositories)}")


if __name__ == '__main__':
    main()
