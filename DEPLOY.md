# Деплой PawndMe

Код хранится на GitHub, а работающий сайт — на **PythonAnywhere** (бесплатный тариф).

Почему не только GitHub: GitHub Pages умеет показывать только статические файлы, но не
запускает Django и базу данных. Бесплатные хостинги вроде Render или Vercel удаляют
файл SQLite и загруженные фото при каждом перезапуске. На PythonAnywhere у сайта есть
постоянный диск, поэтому SQLite и фото животных сохраняются.

Как это устроено:

```
GitHub (main) ──CI──► тесты + сборка React ──► ветка frontend-build
                                                     │
PythonAnywhere: deploy.sh ── git pull + забирает сборку ┘
   Django отдаёт React по адресу /, API по /api, админку по /admin
   ~/pawndme-data/db.sqlite3  ← база (вне репозитория, git pull её не трогает)
   ~/pawndme-data/media/      ← загруженные фото
```

Фронтенд и API работают на одном адресе, поэтому CORS настраивать не нужно.

## 1. GitHub

1. Слейте ветку `deploy/production` в `main` (через Pull Request).
2. Откройте вкладку **Actions** в репозитории и дождитесь зелёного запуска **CI**.
   После него появится ветка `frontend-build` с собранным React.
   Если запуск упал на шаге `publish-frontend` с ошибкой прав доступа, откройте
   **Settings → Actions → General → Workflow permissions**, выберите
   **Read and write permissions** и перезапустите workflow.

## 2. Аккаунт PythonAnywhere

Зарегистрируйтесь на https://www.pythonanywhere.com (тариф **Beginner**, бесплатный).
Дальше вместо `yourname` подставляйте своё имя пользователя. Сайт будет доступен по
адресу `https://yourname.pythonanywhere.com`.

## 3. Первая установка (вкладка Consoles → Bash)

```bash
git clone https://github.com/KazykhanMukhamedali/PawndMe.git ~/PawndMe
mkvirtualenv pawndme --python=python3.11
pip install -r ~/PawndMe/pawndme_backend/requirements.txt
mkdir -p ~/pawndme-data/media

cp ~/PawndMe/pawndme_backend/.env.example ~/PawndMe/pawndme_backend/.env
python -c "import secrets; print(secrets.token_urlsafe(50))"   # скопируйте ключ
nano ~/PawndMe/pawndme_backend/.env
```

В `.env` вставьте ключ в `DJANGO_SECRET_KEY` и везде замените `yourname` на своё имя
(Ctrl+O, Enter, Ctrl+X — сохранить и выйти). Затем:

```bash
cd ~/PawndMe && bash deploy.sh
cd pawndme_backend && python manage.py createsuperuser
```

`deploy.sh` применит миграции и создаст пустую базу `~/pawndme-data/db.sqlite3`.

**Перенести текущие локальные данные (необязательно).** На вкладке **Files** загрузите
свой `pawndme_backend/db.sqlite3` в папку `/home/yourname/pawndme-data/`, а фото из
`pawndme_backend/media/animals/` — в `/home/yourname/pawndme-data/media/animals/`.
После этого снова запустите `bash deploy.sh`, чтобы применить новые миграции.

## 4. Веб-приложение (вкладка Web)

1. **Add a new web app** → **Manual configuration** → **Python 3.11**.
2. **Virtualenv:** `/home/yourname/.virtualenvs/pawndme`
3. **Source code:** `/home/yourname/PawndMe/pawndme_backend`
4. Откройте ссылку **WSGI configuration file**, удалите всё содержимое и вставьте:

   ```python
   import os
   import sys

   path = '/home/yourname/PawndMe/pawndme_backend'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

5. **Static files** — добавьте два маршрута:

   | URL        | Directory                                          |
   |------------|----------------------------------------------------|
   | `/static/` | `/home/yourname/PawndMe/pawndme_backend/staticfiles` |
   | `/media/`  | `/home/yourname/pawndme-data/media`                |

6. **Security → Force HTTPS:** включить.
7. Нажмите зелёную кнопку **Reload** и откройте `https://yourname.pythonanywhere.com`.

## 5. Обновление сайта

После каждого слияния в `main` (и зелёного CI) выполните в Bash-консоли PythonAnywhere:

```bash
cd ~/PawndMe && bash deploy.sh yourname.pythonanywhere.com
```

Скрипт подтянет код и свежую сборку React, обновит зависимости, применит миграции,
соберёт статику и перезапустит сайт. База и фото при этом не меняются.

## Полезно знать

- **Бесплатный тариф:** раз в 3 месяца на вкладке Web нужно нажать
  **Run until 3 months from today**, иначе сайт остановится (PythonAnywhere пришлёт письмо).
- **Резервная копия базы:** скачайте `~/pawndme-data/db.sqlite3` на вкладке Files или
  выполните `sqlite3 ~/pawndme-data/db.sqlite3 ".backup ~/pawndme-data/backup.sqlite3"`.
- **Ошибки:** на вкладке Web есть ссылки на **error log** и **server log**.
- **Если браузер пишет «слишком много перенаправлений»,** добавьте в `.env`
  `DJANGO_SECURE_SSL_REDIRECT=false` и нажмите Reload.
- **Письма для сброса пароля** по умолчанию попадают в server log. Чтобы отправлять
  настоящие письма, задайте в `.env` переменные `EMAIL_*` из README.
- Все настройки сервера лежат в `pawndme_backend/.env`; список — в `.env.example`.
