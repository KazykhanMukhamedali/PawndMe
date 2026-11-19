#!/usr/bin/env bash
# Update the live site on PythonAnywhere. Run from a PythonAnywhere Bash console:
#   cd ~/PawndMe && bash deploy.sh yourname.pythonanywhere.com
set -euo pipefail
cd "$(dirname "$0")"

git pull --ff-only

# React build made by GitHub Actions (see .github/workflows/ci.yml)
git fetch origin frontend-build
rm -rf pawndme/dist && mkdir -p pawndme/dist
git archive origin/frontend-build | tar -x -C pawndme/dist

source ~/.virtualenvs/pawndme/bin/activate
pip install -q -r pawndme_backend/requirements.txt

cd pawndme_backend
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check --deploy --fail-level ERROR

if [ -n "${1:-}" ]; then
  touch "/var/www/${1//./_}_wsgi.py"   # reloads the web app
  echo "Deployed and reloaded https://$1"
else
  echo "Deployed. Press Reload on the PythonAnywhere Web tab."
fi
