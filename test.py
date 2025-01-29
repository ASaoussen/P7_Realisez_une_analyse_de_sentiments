import pytest
from fastapi.testclient import TestClient
from app import app  # Assurez-vous que votre fichier FastAPI est correctement importé

client = TestClient(app)

# Test de la route de base
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API d'Analyse de Sentiments !"}

# Test de prédiction avec texte valide
def test_predict_valid_text():
    input_data = {"text": "I love this product!"}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "sentiment" in response.json()
    assert response.json()["sentiment"] in ["Positive", "Negative"]

# Test de prédiction avec texte vide
def test_predict_empty_text():
    input_data = {"text": ""}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Le texte ne peut pas être vide."

# Test de prédiction avec texte avec des caractères spéciaux et chiffres
def test_predict_text_with_special_characters():
    input_data = {"text": "I love this 123! @product$%."}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "sentiment" in response.json()

# Test du fichier modèle introuvable
#def test_model_not_found(monkeypatch):
#    monkeypatch.setattr('os.path.exists', lambda x: False)  # Simuler un modèle manquant
#    with pytest.raises(RuntimeError):
#        client.post("/predict/", json={"text": "Good day!"})

# Test du comportement lors du chargement du modèle
#def test_model_loading_error(monkeypatch):
#    monkeypatch.setattr('joblib.load', lambda x: 1 / 0)  # Simuler une erreur lors du chargement du modèle
#    with pytest.raises(RuntimeError):
#        client.post("/predict/", json={"text": "Good day!"})

# Test de la route de prédiction avec texte qui pourrait entraîner une exception inattendue
def test_predict_unexpected_error():
    input_data = {"text": "This might break!"}
    # Simuler une erreur de traitement dans la prédiction
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200
    assert "detail" in response.json()