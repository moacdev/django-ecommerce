# Image de base légère compatible linux/amd64 : docker build --platform linux/amd64 -t sigida-app:latest .
FROM python:3.10-slim

# Le répertoire de travail
WORKDIR /app

# Copie du fichier de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Build Tailwind CSS
RUN python3 manage.py tailwind build

# Exposer le port d'acces
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

