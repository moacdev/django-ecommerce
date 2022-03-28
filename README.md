# django-ecommerce

Pré-requis:\
--- Git\
--- Python3.10+
## Deploiemnt
    git clone git@github.com:moacdev\django-ecommerce.git
    python -m venv env
    source env/Scripts/activate
    pip install -r requirements.txt
    python manage.py runserver
    python manage.py tailwind start // pour lancer le compilatur tailwind
Aller sur http://127.0.0.1:8000/
## Structure
base => Application principal \
--- settings.py => Fichier de configuration principal \
--- url.py => Fichier de configuration des urls \
store => Application pour la partie boutique \
--- template => Dossier contenant les page html pour la partie UI \
--- --- store => Dossier contenant UI de l'application store  \
--- --- --- layouts => Dosier contenant les layouts \
--- models.py => Fichier contenant les models des table dans la DB \
--- views.py => Fichier contenant les fonctions retournant les vue html de l'UI \
account => Application pour la partie Compte utilisateur \
--- models.py => Fichier contenant les models des table dans la DB \
--- views.py => Fichier contenant les fonctions retournant les vue html de l'UI \
theme => Application contenant les styles pour le design \
static => Dossier contenant les fichiers static accessible directement depuis l'url \



