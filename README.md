# 📁 Folder Structure Generator

<img src="https://i.imgur.com/KZGIDj0.png" alt="Get started with Python for Research" title="Get started with Python for Research" />

## Description

Générateur de structure de répertoires pour projets de recherche. Cet outil permet de créer rapidement une organisation cohérente de dossiers pour vos projets de recherche, avec support pour différents langages (Python, R, Stata, Jupyter).

## Fonctionnalités

- 🗂️ Interface web moderne et intuitive
- 🌐 Support bilingue (Français/English)
- 📦 Génération de structure complète ou simplifiée
- 🐍 Templates de démarrage pour Python, Jupyter, R, et Stata
- 📝 Fichiers .gitignore pré-configurés
- 🔌 API REST pour intégration

## Installation

### Prérequis

- Python 3.x
- pip

### Installation des dépendances

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### En ligne de commande (développement)

```bash
gunicorn --bind 0.0.0.0:8000 app:api
```

### Avec systemd (production)

Le service est configuré pour démarrer automatiquement sur le port 80 :

```bash
sudo systemctl start folder-structure.service
sudo systemctl enable folder-structure.service
```

### Interface Web

Accédez à `http://localhost` (ou `http://localhost:8000` en mode dev)

### API

#### Endpoints disponibles

- `GET /` - Interface web
- `GET /alive` - Health check
- `GET /get_folder_structure` - Génération de structure

#### Exemple d'utilisation de l'API

```bash
curl "http://localhost/get_folder_structure?project_name=mon_projet&full_structure=1&include_git_ignore=1&templates=python_file,python_notebook"
```

## Structure de projet générée

### Structure complète (`full_structure=1`)

```
mon_projet/
├── administrative/
├── empirical/
│   ├── 0_data/
│   │   ├── credentials/
│   │   ├── external/
│   │   └── manual/
│   ├── 1_code/
│   │   └── templates/
│   ├── 2_pipeline/
│   └── 3_output/
│       ├── data/
│       └── results/
├── explorative/
└── paper/
    ├── literature/
    └── main_text/
```

### Structure simplifiée (`full_structure=0`)

```
mon_projet/
├── 0_data/
│   ├── credentials/
│   ├── external/
│   └── manual/
├── 1_code/
│   └── templates/
├── 2_pipeline/
└── 3_output/
    ├── data/
    └── results/
```

## Technologies

- **Backend**: Python, Falcon 4.x, Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Déploiement**: systemd

## Crédits

- **Projet initial** : [Ties de Kok](https://www.tiesdekok.com/)
- **Code source original** : https://www.tiesdekok.com/folder-structure-generator/
- **Modification et adaptation** : Virgile Jarrige (virgile.jarrige@unistra.fr)

## Licence

<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.