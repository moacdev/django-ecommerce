# Image de base légère
FROM python:3.10-slim

# Le répertoire de travail
WORKDIR /app

# Copie du fichier de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposer le port d'acces
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

