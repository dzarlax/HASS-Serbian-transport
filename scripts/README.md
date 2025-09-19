# Version Management Scripts

Эта папка содержит скрипты для автоматического управления версиями Serbian Transport integration.

## 🚀 Автоматическое версионирование

### Использование скрипта

```bash
# Показать текущую версию
python3 scripts/version_manager.py show

# Автоматический bump версии на основе коммитов
python3 scripts/version_manager.py bump

# Принудительный bump определенного типа
python3 scripts/version_manager.py bump --type patch
python3 scripts/version_manager.py bump --type minor
python3 scripts/version_manager.py bump --type major

# Создать git tag после bump'а
python3 scripts/version_manager.py bump --create-tag

# Создать только git tag для текущей версии
python3 scripts/version_manager.py tag
```

### 📋 Что обновляется автоматически:

1. **manifest.json** - версия интеграции
2. **transport-card.js** - версия в комментарии
3. **CHANGELOG.md** - автогенерируемый changelog
4. **Git tags** - с описанием изменений

### 🎯 Conventional Commits

Скрипт автоматически определяет тип версии на основе коммитов:

- **MAJOR** (x.0.0): `BREAKING:`, `breaking:`
- **MINOR** (0.x.0): `feat:`, `feature:`, `add`, `enhance`, `implement`
- **PATCH** (0.0.x): `fix:`, `bugfix:`, остальные коммиты

### Примеры коммитов:

```bash
# Увеличит patch версию
git commit -m "fix: resolve station selection dropdown issue"

# Увеличит minor версию
git commit -m "feat: add station filtering functionality"

# Увеличит major версию
git commit -m "BREAKING: change API endpoint structure"
```

## 🤖 GitHub Actions

### Автоматические релизы

Workflow `.github/workflows/release.yml` автоматически:

1. **Отслеживает push в main** ветку
2. **Анализирует коммиты** с последнего тега
3. **Обновляет версию** если есть новые коммиты
4. **Создает changelog** на основе коммитов
5. **Создает git tag** с описанием
6. **Публикует GitHub Release** с release notes

### Ручное создание релиза

Можно запустить вручную через GitHub Actions:

1. Идите в **Actions** → **Release Management**
2. Нажмите **"Run workflow"**
3. Выберите тип версии:
   - `auto` - автоматическое определение
   - `patch` - 0.0.x
   - `minor` - 0.x.0  
   - `major` - x.0.0

## 📁 Структура файлов

```
scripts/
├── version_manager.py  # Основной скрипт управления версиями
└── README.md          # Документация (этот файл)

.github/workflows/
├── hacs.yml          # HACS валидация
└── release.yml       # Автоматические релизы
```

## 🔧 Настройка

### Требования

- Python 3.11+
- Git

### Права доступа

Для GitHub Actions нужны права:
- `contents: write` - для создания коммитов и тегов
- `issues: write` - для создания релизов

## 📝 Changelog Format

Автогенерируемый CHANGELOG.md включает:

```markdown
## [v2.1.0] - 2023-09-19

### ✨ Features
- feat: add station selection dropdown
- enhance: improve UI animations

### 🐛 Bug Fixes  
- fix: resolve dropdown positioning issue
- fix: station filtering logic

### ⚠️ BREAKING CHANGES
- BREAKING: change configuration format
```

## 🎯 Интеграция с HACS

После создания релиза:

1. **HACS автоматически** обнаружит новую версию
2. **Пользователи увидят** уведомление об обновлении
3. **Changelog будет** доступен в GitHub Releases

## 🚀 Workflow для разработки

1. Делайте изменения в коде
2. Коммитьте с conventional commit messages
3. Push в main ветку
4. GitHub Actions автоматически создаст релиз
5. HACS обновит интеграцию для пользователей

## 🔍 Отладка

Если что-то пошло не так:

```bash
# Проверить текущее состояние
python3 scripts/version_manager.py show

# Проверить последние коммиты
git log --oneline -10

# Проверить теги
git tag --list | tail -5

# 📊 Анализ истории версий
python3 scripts/version_manager.py history

# 📝 Создание полного CHANGELOG для всех тегов
python3 scripts/version_manager.py changelog

# 🔍 Предварительный просмотр версии (без изменений)
python3 scripts/version_manager.py bump --dry-run
```

## 📊 Новые возможности

### Анализ истории версий
```bash
python3 scripts/version_manager.py history
```
Показывает статистику по всем релизам с количеством features, fixes и breaking changes.

### Создание ретроспективного changelog
```bash
python3 scripts/version_manager.py changelog
```
Создает полный CHANGELOG.md для всех существующих тегов в репозитории.

### Предварительный просмотр версии
```bash
python3 scripts/version_manager.py bump --dry-run
python3 scripts/version_manager.py bump --type minor --dry-run
```
Показывает, какая версия будет установлена, без фактических изменений файлов.
```
