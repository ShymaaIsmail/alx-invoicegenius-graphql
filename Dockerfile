# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and create superuser
RUN python manage.py migrate --noinput && \
    echo "from django.contrib.auth import get_user_model; \
user = get_user_model(); \
user.objects.filter(username='root').exists() or \
user.objects.create_superuser('root', 'root@example.com', '123456')" \
| python manage.py shell

# Expose port (Django default or your custom one)
EXPOSE 8000

# Start the Django app using Gunicorn
CMD ["gunicorn", "invoicesgenius.wsgi:application", "--bind", "0.0.0.0:8000"]
