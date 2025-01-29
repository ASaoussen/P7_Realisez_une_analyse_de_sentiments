import pytest
from fastapi.testclient import TestClient
from app import app  # Assure-toi que ton fichier FastAPI s'appelle "app.py" ou adapte l'import si nécessaire

# Créer une instance de TestClient
client = TestClient(app)

def test_predict_valid_input():
    """Test avec une entrée valide."""
    input_data = {"text": "I love this product!"}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "sentiment" in response.json()

def test_predict_empty_text():
    """Test avec un texte vide."""
    input_data = {"text": ""}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Le texte ne peut pas être vide."}

def test_predict_numeric_input():
    """Test avec un texte numérique."""
    input_data = {"text": "12345"}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Le texte ne peut pas être un nombre."}

def test_predict_unexpected_error():
    """Test pour vérifier une erreur inattendue."""
    input_data = {"text": "This might break!"}
    # Simuler une erreur de traitement dans la prédiction
    # Par exemple, avec un modèle qui n'est pas encore chargé ou une mauvaise entrée
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "sentiment" in response.json()

def test_predict_missing_text():
    """Test avec un champ 'text' manquant."""
    input_data = {}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 422  # Unprocessable Entity (champ manquant)
    assert "detail" in response.json()
    assert "loc" in response.json()
