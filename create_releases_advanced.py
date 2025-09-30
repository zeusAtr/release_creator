#!/usr/bin/env python3
"""
Расширенный скрипт для создания релизов в нескольких GitHub репозиториях.
Поддерживает конфигурационные файлы и аргументы командной строки.
"""

import os
import sys
import argparse
import requests
from typing import List, Dict, Optional, Tuple


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
        """Получает последний тег из репозитория."""
        url = f'{self.base_url}/repos/{owner}/{repo}/tags'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tags = response.json()
            if not tags:
                print(f"⚠️  Нет тегов в репозитории {owner}/{repo}")
                return None
            
            latest_tag = tags[0]
            print(f"✓ Найден тег {latest_tag['name']} в {owner}/{repo}")
            return latest_tag
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при получении тегов из {owner}/{repo}: {e}")
            return None
    
    def check_release_exists(self, owner: str, repo: str, tag_name: str) -> bool:
        """Проверяет, существует ли релиз для данного тега."""
        url = f'{self.base_url}/repos/{owner}/{repo}/releases/tags/{tag_name}'
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_commits_since_previous_tag(self, owner: str, repo: str, 
                                       current_tag: str, previous_tag: Optional[str]) -> List[Dict]:
        """Получает список коммитов между двумя тегами."""
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
        """Генерирует описание релиза на основе коммитов."""
        if not commits:
            return f"Release {tag_name}"
        
        notes = [f"## What's Changed in {tag_name}\n"]
        
        for commit in commits:
            message = commit['commit']['message'].split('\n')[0]
            author = commit['commit']['author']['name']
            sha = commit['sha'][:7]
            notes.append(f"- {message} ({sha}) by @{author}")
        
        notes.append(f"\n**Full Changelog**: {commits[0]['html_url'].rsplit('/', 1)[0]}/compare/{tag_name}")
        
        return '\n'.join(notes)
    
    def create_release(self, owner: str, repo: str, tag_name: str, 
                      name: Optional[str] = None, body: Optional[str] = None,
                      draft: bool = False, prerelease: bool = False) -> Optional[Dict]:
        """Создает релиз в репозитории."""
        url = f'{self.base_url}/repos/{owner}/{repo}/releases'
        
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
        """Обрабатывает один репозиторий."""
        print(f"\n📦 Обработка {owner}/{repo}...")
        
        latest_tag = self.get_latest_tag(owner, repo)
        if not latest_tag:
            return False
        
        tag_name = latest_tag['name']
        
        body = None
        if auto_notes:
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
        
        release = self.create_release(
            owner, repo, tag_name,
            name=tag_name,
            body=body,
            draft=draft,
            prerelease=prerelease
        )
        
        return release is not None


def load_repositories_from_file(file_path: str) -> List[Tuple[str, str]]:
    """
    Загружает список репозиториев из файла.
    
    Args:
        file_path: Путь к файлу с репозиториями
        
    Returns:
        Список кортежей (owner, repo)
    """
    repositories = []
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл {file_path} не найден")
        return repositories
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            # Ожидаем формат: owner/repo
            if '/' in line:
                parts = line.split('/')
                if len(parts) == 2:
                    owner, repo = parts[0].strip(), parts[1].strip()
                    if owner and repo:
                        repositories.append((owner, repo))
                    else:
                        print(f"⚠️  Строка {line_num}: пустой owner или repo - '{line}'")
                else:
                    print(f"⚠️  Строка {line_num}: неверный формат - '{line}'")
            else:
                print(f"⚠️  Строка {line_num}: ожидается формат 'owner/repo' - '{line}'")
    
    return repositories


def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Создание релизов в GitHub репозиториях на основе последнего тега',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Создать релизы для репозиториев из файла
  %(prog)s -f repositories.txt

  # Создать релизы для конкретных репозиториев
  %(prog)s -r owner1/repo1 owner2/repo2

  # Создать черновики релизов
  %(prog)s -f repositories.txt --draft

  # Создать пре-релизы без автоматических заметок
  %(prog)s -r owner/repo --prerelease --no-auto-notes

  # Использовать свой токен
  %(prog)s -f repos.txt -t ghp_yourtoken123
        """
    )
    
    # Источник репозиториев
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '-f', '--file',
        help='Путь к файлу со списком репозиториев (формат: owner/repo)'
    )
    source_group.add_argument(
        '-r', '--repos',
        nargs='+',
        help='Список репозиториев (формат: owner/repo owner2/repo2)'
    )
    
    # Настройки токена
    parser.add_argument(
        '-t', '--token',
        help='GitHub Personal Access Token (по умолчанию из GITHUB_TOKEN)'
    )
    
    # Настройки релиза
    parser.add_argument(
        '--draft',
        action='store_true',
        help='Создать релизы как черновики'
    )
    parser.add_argument(
        '--prerelease',
        action='store_true',
        help='Отметить релизы как пре-релизы'
    )
    parser.add_argument(
        '--no-auto-notes',
        action='store_true',
        help='Не генерировать автоматические заметки из коммитов'
    )
    
    # Дополнительные опции
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод'
    )
    
    return parser.parse_args()


def main():
    """Основная функция скрипта."""
    args = parse_arguments()
    
    # Получаем токен
    github_token = args.token or os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ Ошибка: Не найден GitHub токен")
        print("   Укажите токен через -t или установите переменную GITHUB_TOKEN")
        print("   Создайте токен на https://github.com/settings/tokens")
        sys.exit(1)
    
    # Получаем список репозиториев
    repositories = []
    
    if args.file:
        print(f"📂 Загрузка репозиториев из файла: {args.file}")
        repositories = load_repositories_from_file(args.file)
    elif args.repos:
        for repo_str in args.repos:
            if '/' in repo_str:
                parts = repo_str.split('/')
                if len(parts) == 2:
                    repositories.append((parts[0].strip(), parts[1].strip()))
                else:
                    print(f"⚠️  Пропущен неверный формат: {repo_str}")
            else:
                print(f"⚠️  Пропущен неверный формат: {repo_str}")
    
    if not repositories:
        print("❌ Ошибка: Не найдено ни одного репозитория для обработки")
        sys.exit(1)
    
    print(f"✓ Загружено {len(repositories)} репозитори{'й' if len(repositories) == 1 else 'ев/я'}")
    
    # Настройки
    auto_notes = not args.no_auto_notes
    draft = args.draft
    prerelease = args.prerelease
    
    if args.verbose:
        print(f"\n⚙️  Настройки:")
        print(f"   - Автоматические заметки: {'✓' if auto_notes else '✗'}")
        print(f"   - Черновики: {'✓' if draft else '✗'}")
        print(f"   - Пре-релизы: {'✓' if prerelease else '✗'}")
    
    # Создаем менеджер релизов
    manager = GitHubReleaseManager(github_token)
    
    # Статистика
    successful = 0
    failed = 0
    skipped = 0
    
    print("\n🚀 Начинаем создание релизов...")
    print("=" * 60)
    
    # Обрабатываем каждый репозиторий
    for owner, repo in repositories:
        try:
            result = manager.process_repository(owner, repo, auto_notes, draft, prerelease)
            if result:
                successful += 1
            else:
                # Проверяем, был ли релиз пропущен (уже существует)
                tag = manager.get_latest_tag(owner, repo)
                if tag and manager.check_release_exists(owner, repo, tag['name']):
                    skipped += 1
                else:
                    failed += 1
        except Exception as e:
            print(f"❌ Непредвиденная ошибка при обработке {owner}/{repo}: {e}")
            failed += 1
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print(f"\n📊 Итоги:")
    print(f"   ✅ Успешно создано: {successful}")
    if skipped > 0:
        print(f"   ⏭️  Пропущено (уже существуют): {skipped}")
    print(f"   ❌ Ошибок: {failed}")
    print(f"   📦 Всего репозиториев: {len(repositories)}")
    
    # Код возврата
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
