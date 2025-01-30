import streamlit as st
import requests
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Remplacez par votre Instrumentation Key
instrumentation_key = "aef8c367-658f-4580-92e6-05a082b5cd6c"

# Configuration du logger pour Application Insights
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=f'InstrumentationKey={instrumentation_key}'))
logger.setLevel(logging.INFO)

# Titre de l'application
st.title("Analyse de Sentiments - Air Paradis")

# Saisie du prénom et du nom
prenom = st.text_input("Entrez votre prénom", "").strip()
nom = st.text_input("Entrez votre nom", "").strip()

if prenom and nom:
    st.write(f"Bonjour {prenom} {nom}, bienvenue sur notre application d'analyse de sentiments !")

# Saisie du texte utilisateur
user_input = st.text_area("Entrez le texte que vous souhaitez analyser")

if st.button("Prédire"):
    if not user_input.strip():
        st.error("Veuillez entrer un texte valide avant de cliquer sur 'Prédire'.")
        logger.warning(f"Utilisateur n'a pas fourni de texte valide.")
    else:
        try:
            # Appel de l'API
            response = requests.post("http://localhost:8000/predict/", json={"text": user_input})
            response.raise_for_status()
            prediction = response.json()

            # Affichage des résultats
            st.write(f"Prédiction : {prediction['prediction']} (Sentiment : {prediction['sentiment']})")

            # Envoi des logs à Application Insights
            logger.info(f"Texte utilisateur analysé : {user_input}")
            logger.info(f"Prédiction reçue : {prediction['prediction']}, Sentiment : {prediction['sentiment']}")

            # Feedback utilisateur
            is_valid = st.radio("La prédiction est-elle correcte ?", ("Oui", "Non"))

            if is_valid == "Non":
                st.write("Merci pour votre retour, nous améliorerons notre modèle.")
                logger.info("Utilisateur a validé la prédiction comme incorrecte.")
            else:
                st.write("Merci d'avoir validé la prédiction.")
                logger.info("Utilisateur a validé la prédiction comme correcte.")

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.error(f"Erreur de connexion à l'API : {e}")
