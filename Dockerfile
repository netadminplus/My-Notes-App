FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### `.dockerignore`
```
__pycache__
*.pyc
*.pyo
*.db
.git
.gitignore
tests/
.pytest_cache
venv/
*.md
```

### `.gitignore`
```
__pycache__/
*.pyc
*.pyo
*.db
venv/
.pytest_cache/
.env