# PawndMe

Run Django and Vite in separate terminals.

```sh
cd pawndme_backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

```sh
cd pawndme
npm ci
npm run dev
```

Open http://localhost:5173. Vite forwards the API to Django on port 8000. To build
against a separately hosted API, set `VITE_API_URL` to its base URL including
`/api` and allow the frontend origin in Django.

To run the production setup locally, build the frontend (`npm run build` in
`pawndme`) and Django serves it at http://localhost:8000 next to the API.
Hosting instructions are in [DEPLOY.md](DEPLOY.md).

Password reset emails print to the Django console locally. To send real email,
set `FRONTEND_URL`, `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`,
`DEFAULT_FROM_EMAIL`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`,
`EMAIL_HOST_PASSWORD` and `EMAIL_USE_TLS` for your mail service.
