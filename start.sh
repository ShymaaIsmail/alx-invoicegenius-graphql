#!/bin/sh
set -e

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "👤 Creating admin user if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='root').exists():
    User.objects.create_superuser('root', 'root@example.com', '123456')
END

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔥 Starting Celery worker in background..."
celery -A invoicesgenius worker --loglevel=info --concurrency=1


echo "🔥 Starting server..."
exec gunicorn invoicesgenius.wsgi:application --bind 0.0.0.0:$PORT --workers 1
echo "🚀 Server started successfully!"