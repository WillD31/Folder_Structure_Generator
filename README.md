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
- `GET /feedback/` - Statistiques d'utilisation

## Statistiques

L'application inclut un tableau de bord des statistiques d'utilisation accessible via `/feedback/`.

### Principes de comptage

- **Connexions au site** : Comptabilisées comme **visiteurs uniques par jour**. Pour respecter la vie privée, un hash anonyme de l'adresse IP est utilisé pour identifier les sessions uniques quotidiennes sur la page d'accueil sans stocker de données personnelles.
- **Structures générées** : Chaque téléchargement de structure est comptabilisé individuellement.
- **Langues** : Répartition des types de structures générées par langue choisie (FR/EN).

Les données sont stockées localement dans une base de données SQLite (`stats.db`).

#### Exemple d'utilisation de l'API

```bash
curl "http://localhost/get_folder_structure?project_name=mon_projet&full_structure=1&include_git_ignore=1&templates=python_file,python_notebook"
```

## Structure de projet générée

### Structure complète (`full_structure=1`)

```
mon_projet/
├── 01_Administratif/
    ├── 01_RH/
    ├── 02_Budget/
    ├── 03_PGD/
├── 02_Donnees_brutes/
├── 03_Traitement_donnees/
│   ├── 01_Code/
│   │   └── 01_Templates/
│   └── 02_Donnees_traitees/
│       ├── data/
│       └── results/
└── 04_Publication/
    ├── 01_Bibliographie/
    └── 02_Texte_publication/
```

### Structure simplifiée (`full_structure=0`)

```
mon_projet/
├── 02_Donnees_brutes/
├── 03_Traitement_donnees/
│   ├── 01_Code/
│   │   └── 01_Templates/
│   └── 02_Donnees_traitees/
│       ├── data/
│       └── results/
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