#!/usr/bin/env python3
"""
Расширенный скрипт для создания релизов в нескольких GitLab проектах.
Поддерживает конфигурационные файлы и аргументы командной строки.
"""

import os
import sys
import argparse
import requests
from typing import List, Dict, Optional
from urllib.parse import quote


class GitLabReleaseManager:
    def __init__(self, token: str, gitlab_url: str = 'https://gitlab.com'):
        """Инициализация менеджера релизов GitLab."""
        self.token = token
        self.gitlab_url = gitlab_url.rstrip('/')
        self.headers = {
            'PRIVATE-TOKEN': token,
            'Content-Type': 'application/json'
        }
        self.api_url = f'{self.gitlab_url}/api/v4'
    
    def get_project_id(self, project_path: str) -> Optional[str]:
        """Получает ID проекта по его пути."""
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
        """Получает последний тег из проекта."""
        url = f'{self.api_url}/projects/{project_id}/repository/tags'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            tags = response.json()
            if not tags:
                print(f"⚠️  Нет тегов в проекте {project_path}")
                return None
            
            latest_tag = tags[0]
            print(f"✓ Найден тег {latest_tag['name']} в {project_path}")
            return latest_tag
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при получении тегов из {project_path}: {e}")
            return None
    
    def check_release_exists(self, project_id: str, tag_name: str) -> bool:
        """Проверяет, существует ли релиз для данного тега."""
        url = f'{self.api_url}/projects/{project_id}/releases/{tag_name}'
        
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_commits_since_previous_tag(self, project_id: str, 
                                       current_tag: str, 
                                       previous_tag: Optional[str]) -> List[Dict]:
        """Получает список коммитов между двумя тегами."""
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
        """Генерирует описание релиза на основе коммитов."""
        if not commits:
            return f"Release {tag_name}"
        
        notes = [f"## What's Changed in {tag_name}\n"]
        
        for commit in commits:
            message = commit['message'].split('\n')[0]
            author = commit['author_name']
            short_id = commit['short_id']
            notes.append(f"- {message} ({short_id}) by {author}")
        
        notes.append(f"\n**Full Changelog**: {self.gitlab_url}/{project_path}/-/compare/{tag_name}?from=&to={tag_name}")
        
        return '\n'.join(notes)
    
    def create_release(self, project_id: str, project_path: str, tag_name: str, 
                      name: Optional[str] = None, description: Optional[str] = None,
                      milestones: Optional[List[str]] = None) -> Optional[Dict]:
        """Создает релиз в проекте GitLab."""
        url = f'{self.api_url}/projects/{project_id}/releases'
        
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
            release_url = f"{self.gitlab_url}/{project_path}/-/releases/{tag_name}"
            print(f"   URL: {release_url}")
            return release
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при создании релиза в {project_path}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Ответ: {e.response.text}")
            return None
    
    def process_repository(self, project_path: str, 
                          auto_notes: bool = True,
                          milestones: Optional[List[str]] = None) -> bool:
        """Обрабатывает один проект."""
        print(f"\n📦 Обработка {project_path}...")
        
        project_id = self.get_project_id(project_path)
        if not project_id:
            return False
        
        latest_tag = self.get_latest_tag(project_id, project_path)
        if not latest_tag:
            return False
        
        tag_name = latest_tag['name']
        
        description = None
        if auto_notes:
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
        
        release = self.create_release(
            project_id, project_path, tag_name,
            name=tag_name,
            description=description,
            milestones=milestones
        )
        
        return release is not None


def load_projects_from_file(file_path: str) -> List[str]:
    """
    Загружает список проектов из файла.
    
    Args:
        file_path: Путь к файлу с проектами
        
    Returns:
        Список путей к проектам
    """
    projects = []
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл {file_path} не найден")
        return projects
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#'):
                continue
            
            # Для GitLab можем иметь: username/project, group/project, group/subgroup/project
            if '/' in line:
                projects.append(line)
            else:
                print(f"⚠️  Строка {line_num}: ожидается формат 'namespace/project' - '{line}'")
    
    return projects


def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Создание релизов в GitLab проектах на основе последнего тега',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Создать релизы для проектов из файла
  %(prog)s -f projects.txt

  # Создать релизы для конкретных проектов
  %(prog)s -p username/project1 group/project2

  # Использовать self-hosted GitLab
  %(prog)s -f projects.txt -u https://gitlab.company.com

  # Создать релизы без автоматических заметок
  %(prog)s -p username/project --no-auto-notes

  # Использовать свой токен
  %(prog)s -f projects.txt -t glpat-yourtoken123

  # Связать релизы с milestone
  %(prog)s -f projects.txt -m "v1.0" "MVP"
        """
    )
    
    # Источник проектов
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '-f', '--file',
        help='Путь к файлу со списком проектов (формат: namespace/project)'
    )
    source_group.add_argument(
        '-p', '--projects',
        nargs='+',
        help='Список проектов (формат: namespace/project group/project)'
    )
    
    # Настройки GitLab
    parser.add_argument(
        '-u', '--url',
        default='https://gitlab.com',
        help='URL GitLab инстанса (по умолчанию: https://gitlab.com)'
    )
    parser.add_argument(
        '-t', '--token',
        help='GitLab Personal Access Token (по умолчанию из GITLAB_TOKEN)'
    )
    
    # Настройки релиза
    parser.add_argument(
        '--no-auto-notes',
        action='store_true',
        help='Не генерировать автоматические заметки из коммитов'
    )
    parser.add_argument(
        '-m', '--milestones',
        nargs='+',
        help='Список milestone для связи с релизом'
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
    gitlab_token = args.token or os.getenv('GITLAB_TOKEN')
    if not gitlab_token:
        print("❌ Ошибка: Не найден GitLab токен")
        print("   Укажите токен через -t или установите переменную GITLAB_TOKEN")
        print("   Создайте токен на https://gitlab.com/-/profile/personal_access_tokens")
        print("   Токен должен иметь права: api")
        sys.exit(1)
    
    # Получаем URL GitLab
    gitlab_url = args.url or os.getenv('GITLAB_URL', 'https://gitlab.com')
    
    # Получаем список проектов
    projects = []
    
    if args.file:
        print(f"📂 Загрузка проектов из файла: {args.file}")
        projects = load_projects_from_file(args.file)
    elif args.projects:
        projects = [p.strip() for p in args.projects]
    
    if not projects:
        print("❌ Ошибка: Не найдено ни одного проекта для обработки")
        sys.exit(1)
    
    print(f"✓ Загружено {len(projects)} проект{'ов' if len(projects) != 1 else ''}")
    
    # Настройки
    auto_notes = not args.no_auto_notes
    milestones = args.milestones
    
    if args.verbose:
        print(f"\n⚙️  Настройки:")
        print(f"   - GitLab URL: {gitlab_url}")
        print(f"   - Автоматические заметки: {'✓' if auto_notes else '✗'}")
        if milestones:
            print(f"   - Milestones: {', '.join(milestones)}")
    
    # Создаем менеджер релизов
    manager = GitLabReleaseManager(gitlab_token, gitlab_url)
    
    # Статистика
    successful = 0
    failed = 0
    skipped = 0
    
    print(f"\n🚀 Начинаем создание релизов в GitLab ({gitlab_url})...")
    print("=" * 60)
    
    # Обрабатываем каждый проект
    for project_path in projects:
        try:
            result = manager.process_repository(project_path, auto_notes, milestones)
            if result:
                successful += 1
            else:
                # Проверяем, был ли релиз пропущен
                project_id = manager.get_project_id(project_path)
                if project_id:
                    tag = manager.get_latest_tag(project_id, project_path)
                    if tag and manager.check_release_exists(project_id, tag['name']):
                        skipped += 1
                    else:
                        failed += 1
                else:
                    failed += 1
        except Exception as e:
            print(f"❌ Непредвиденная ошибка при обработке {project_path}: {e}")
            failed += 1
    
    # Выводим итоги
    print("\n" + "=" * 60)
    print(f"\n📊 Итоги:")
    print(f"   ✅ Успешно создано: {successful}")
    if skipped > 0:
        print(f"   ⏭️  Пропущено (уже существуют): {skipped}")
    print(f"   ❌ Ошибок: {failed}")
    print(f"   📦 Всего проектов: {len(projects)}")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
