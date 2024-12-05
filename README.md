# django-ecommerce

[![eDango](https://i.postimg.cc/7hd2bK8S/Screen-Shot-2022-08-26-at-17-40-00.png)](https://postimg.cc/ZvPRMFqq)

## Pré-requis:\

| Git\
| Python3.10+

## Deploiemnt

    git clone git@github.com:moacdev\django-ecommerce.git
    python -m venv env
    source env/Scripts/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    python manage.py tailwind start // pour lancer le compilatur tailwind

Aller sur http://127.0.0.1:8000/

## Structure

base => Application principal \
| settings.py => Fichier de configuration principal \
| url.py => Fichier de configuration des urls \
store => Application pour la partie boutique \
| template => Dossier contenant les page html pour la partie UI \
| | store => Dossier contenant UI de l'application store \
| | | layouts => Dosier contenant les layouts \
| models.py => Fichier contenant les models des table dans la DB \
| views.py => Fichier contenant les fonctions retournant les vue html de l'UI \
account => Application pour la partie Compte utilisateur \
| models.py => Fichier contenant les models des table dans la DB \
| views.py => Fichier contenant les fonctions retournant les vue html de l'UI \
theme => Application contenant les styles pour le design \
static => Dossier contenant les fichiers static accessible directement depuis l'url \

## Deployement step by step

|> eksctl create cluster -f cluster-config.yml # Création du cluster EKS
|> kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.13.1/cert-manager.yaml # Certificat Let's Encrypt
|> kubectl apply -f cluster-issuer.yml # Certificat Let's Encrypt
|> kubectl create namespace staging # Création du namespace staging
|> kubectl create namespace prod # Création du namespace prod
|> kubectl create namespace ingress-nginx # Création du namespace ingress-nginx
|> kubectl apply -f ingress-nginx-nlb-service.yml # Service Ingress Nginx
|> kubectl apply -f staging-ingress.yml -n staging # Ingress pour le staging
|> kubectl apply -f prod-ingress.yml -n prod # Ingress pour le prod
|> kubectl apply -f service.yml -n staging # Service pour le staging
|> kubectl apply -f service.yml -n prod # Service pour le prod
|> kubectl apply -f deployment-staging.yml -n staging # Deployment pour le staging
|> kubectl apply -f deployment-prod.yml -n prod # Deployment pour le prod
