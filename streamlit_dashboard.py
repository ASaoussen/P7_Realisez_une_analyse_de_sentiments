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

# Appliquer un style CSS personnalisé
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-bottom: 10px;
        }
        .title {
            font-size: 36px;
            font-weight: bold;
            color: #1DA1F2;  /* Bleu Twitter */
            font-family: 'Arial', sans-serif;
        }
        .twitter-logo {
            width: 50px;
            height: 50px;
        }
        .prediction-box {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            text-align: center;
            margin-top: 10px;
            border-left: 5px solid #1DA1F2;
        }
        .separator {
            border-top: 2px solid #ddd;
            margin: 20px 0;
        }
        .welcome {
            text-align: center;
            font-size: 18px;
            color: #444;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# Titre avec logo Twitter
st.markdown("""
    <div class="title-container">
        <img src="https://cdn-icons-png.flaticon.com/512/124/124021.png" class="twitter-logo">
        <p class="title">Analyse de Sentiments - Air Paradis</p>
    </div>
""", unsafe_allow_html=True)

# Saisie du prénom et du nom
prenom = st.text_input("Entrez votre prénom", "").strip()
nom = st.text_input("Entrez votre nom", "").strip()

# Affichage du message de bienvenue sous le titre
if prenom and nom:
    st.markdown(f'<p class="welcome">👋 Bonjour **{prenom} {nom}**, bienvenue sur notre application d\'analyse de sentiments !</p>', unsafe_allow_html=True)

# Séparateur visuel
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Saisie du texte utilisateur
user_input = st.text_area("✍️ Entrez le texte que vous souhaitez analyser")

if st.button("🔍 Prédire"):
    if not user_input.strip():
        st.error("❌ Veuillez entrer un texte valide avant de cliquer sur 'Prédire'.")
        logger.warning("Utilisateur n'a pas fourni de texte valide.")
    else:
        try:
            # Appel de l'API
            response = requests.post("http://localhost:8000/predict/", json={"text": user_input})
            response.raise_for_status()
            prediction = response.json()

            sentiment = prediction['sentiment']  # Récupérer le sentiment

            # Affichage des résultats
            st.markdown(f"""
                <div class="prediction-box">
                    <strong>📝 Prédiction :</strong> {prediction['prediction']}<br>
                    <strong>📊 Sentiment :</strong> {sentiment}
                </div>
            """, unsafe_allow_html=True)

            # Envoi des logs uniquement si le sentiment est négatif
            if sentiment.lower() == "negative":
                logger.warning(f"🚨 Sentiment négatif détecté : {user_input}")
                logger.warning(f"Prédiction reçue : {prediction['prediction']}, Sentiment : {sentiment}")

            # Séparateur avant feedback utilisateur
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

            # Feedback utilisateur
            is_valid = st.radio("✅ La prédiction est-elle correcte ?", ("Oui", "Non"))

            if st.button("Envoyer mon retour"):
                if is_valid == "Non":
                    st.warning("🛠 Merci pour votre retour, nous améliorerons notre modèle !")
                    logger.info("Utilisateur a validé la prédiction comme incorrecte.")
                else:
                    st.success("🎉 Merci d'avoir validé la prédiction !")
                    logger.info("Utilisateur a validé la prédiction comme correcte.")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Erreur de connexion à l'API : {e}")
            logger.error(f"Erreur de connexion à l'API : {e}")
