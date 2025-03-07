# Projet de Prédiction de Sentiment sur les Tweets - Air Paradis

Ce projet a pour objectif de prédire les sentiments des tweets d'Air Paradis en utilisant plusieurs modèles de machine learning, allant des modèles simples (comme la régression logistique) aux modèles plus avancés comme LSTM avec GloVe et LSTM avec Word2Vec, et BERT. Bien que plusieurs modèles aient été explorés, la régression logistique a été retenue en raison de sa simplicité et de sa portabilité.

## Description

Le modèle de régression logistique a été choisi pour la prédiction des sentiments des tweets, car il est plus léger et facilement déployable, ce qui garantit une portabilité maximale. Cependant, des modèles plus avancés ont également été testés dans le cadre du projet :

- **Régression Logistique** (modèle simple et rapide)
- **LSTM avec embeddings GloVe**
- **LSTM avec embeddings Word2Vec**
- **BERT** (modèle pré-entrainé plus puissant mais plus lourd)

Tous ces modèles ont été évalués et comparés pour déterminer lequel offre les meilleures performances pour le cas d'usage.

## Fonctionnalités

- Prédiction des sentiments (positif/négatif) des tweets via une API **FastAPI**.
- Suivi des expériences avec **MLflow**.
- Déploiement sur **Azure** pour une API en production.
- Évaluation des performances de différents modèles (régression logistique, LSTM avec GloVe/Word2Vec, BERT).

## Lien vers les données

Les données utilisées proviennent du dataset **Sentiment140** (retrouvé [ici](https://www.kaggle.com/kazanova/sentiment140)), qui contient des tweets étiquetés avec des sentiments positifs ou négatifs.

## Prérequis

- **Python 3.12**
- **Windows** : Ce projet est configuré pour être exécuté sur un environnement Windows. Si vous utilisez un autre système d'exploitation, vous devrez adapter le fichier `config.yaml` (voir ci-dessous).



## Contenu du Projet

- **best_model.pkl** : Le modèle de régression logistique entraîné, sauvegardé à l'aide de [joblib](w).
- **app.py** : Le script principal pour déployer le modèle sous forme d'API avec [FastAPI](w).
- **test.py** : Un script pour tester les endpoints de l'API.
- **requirements.txt** : Liste des dépendances Python nécessaires pour faire fonctionner le projet.
- **azure-webapps-python.yml** : Fichier de configuration pour suivre l'expérience avec [MLFlow](w).

## Déploiement

Pour déployer l'API localement ou sur Azure, assurez-vous d'avoir les prérequis installés, tels que [FastAPI](w), [uvicorn](w), et [MLFlow](w).

### Étapes pour Exécuter le Projet Localement

1. **Cloner le Repo** :

    ```bash
    git clone https://github.com/ASaoussen/P7_Realisez_une_analyse_de_sentiments
    
    ```

2. **Créer un Environnement Virtuel** :

    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Mac/Linux
    venv\Scripts\activate  # Sur Windows
    ```

3. **Installer les Dépendances** :

    ```bash
    pip install -r requirements.txt
    ```
4.**Modifiez le fichier azure-webapps-python.yml si vous n'utilisez pas Windows** :

Si vous êtes sur Linux ou macOS, ajustez les chemins de répertoires et configurations spécifiques à votre environnement.

5. **Lancer l'API Localement** :

    ```bash
    uvicorn app:app --reload
    ```

6. Accédez à [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) pour tester l'API.

### Tester l'API

Une fois l'API en fonctionnement, vous pouvez envoyer des requêtes à l'endpoint `/predict` pour obtenir des prédictions sur de nouveaux tweets.


## Déploiement sur Azure

1. Configurez votre instance [Azure](w) et déployez le modèle en suivant les instructions dans la [documentation Azure](w).
2. Utilisez [MLFlow](w) pour suivre les expériences et enregistrer les meilleurs modèles.

## Résultats

Le modèle a été évalué à l'aide de métriques de classification telles que la précision, l'AUC et la log-loss. Le meilleur modèle de régression logistique a été sauvegardé dans `model.pkl` et est utilisé pour les prédictions sur l'API.








