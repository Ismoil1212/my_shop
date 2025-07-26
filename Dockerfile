FROM python:3.12.2

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn my_shop.wsgi:application --bind 0.0.0.0:8000"]