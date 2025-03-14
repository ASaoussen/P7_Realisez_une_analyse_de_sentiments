import os
import re
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Configuration des journaux
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Assurer que nltk_data est bien accessible (doit être géré par le YAML)
NLTK_DATA_PATH = os.getenv("NLTK_DATA", os.path.join(os.getcwd(), "myenv", "nltk_data"))  # Ajuste ce chemin selon ton environnement
nltk.data.path = [NLTK_DATA_PATH]
#nltk.data.path.append(NLTK_DATA_PATH)

# Téléchargement des ressources nécessaires
RESOURCES = ['wordnet', 'omw-1.4', 'stopwords', 'punkt', 'punkt_tab']
for resource in RESOURCES:
    try:
        nltk.data.find(f"tokenizers/{resource}" if resource in ['punkt', 'punkt_tab'] else f"corpora/{resource}")
    except LookupError:
        logging.info(f"Téléchargement du package NLTK : {resource}")
        nltk.download(resource, download_dir=NLTK_DATA_PATH)



# Initialisation de l'analyseur lexical et des stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """Nettoie le texte en supprimant les caractères spéciaux et les chiffres."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Supprime la ponctuation
    text = re.sub(r'\d+', '', text)  # Supprime les chiffres
    return text

def preprocess_text(text: str) -> str:
    """Prépare le texte en le nettoyant, le tokenisant et en le lemmatisant."""
    text = clean_text(text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Création de l'application FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API d'Analyse de Sentiments !"}

# Chargement du modèle
MODEL_PATH = "best_model.pkl"
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Le fichier {MODEL_PATH} est introuvable.")
    pipeline = joblib.load(MODEL_PATH)
except Exception as e:
    logging.error(f"Erreur lors du chargement du modèle : {e}")
    raise RuntimeError(f"Échec du chargement du modèle : {e}")



class InputData(BaseModel):
    text: str

    @field_validator('text')
    def validate_text(cls, v):
        """Valide que le texte n'est pas vide et n'est pas un nombre."""
        
        # Vérifie si v est vide après avoir retiré les espaces
        if not v.strip():   
            raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide.")
        
        # Vérifie si v est un nombre (int ou float)
        try:
            # Tente de convertir le texte en float pour voir s'il s'agit d'un nombre
            float(v)  
            raise HTTPException(status_code=400, detail="Le texte ne peut pas être un nombre.")
        except ValueError:
            # Si une exception est levée, cela signifie que v n'est pas un nombre
            pass
        
        return v
@app.post("/predict/")
async def predict(input_data: InputData):
    """Prédit le sentiment d'un texte."""
    try:
        # Prétraitement du texte
        cleaned_text = preprocess_text(input_data.text)
        
        # Prédiction avec le modèle
        predictions = pipeline.predict([cleaned_text])
        sentiment = "Positive" if predictions[0] == 1 else "Negative"
        
        # Retour de la réponse
        return {"prediction": int(predictions[0]), "sentiment": sentiment}
    except ValueError as ve:
        logging.error(f"Erreur lors de la prédiction : {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Erreur lors de la prédiction : {e}")
        raise HTTPException(status_code=500, detail=str(e))

#Lancer l'API avec Uvicorn
#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)
