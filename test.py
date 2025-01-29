import pytest
from fastapi.testclient import TestClient
from app import app  # Remplace 'main' par le nom de ton fichier si nécessaire

client = TestClient(app)

def test_root():
    """Test de la racine de l'API"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API d'Analyse de Sentiments !"}

def test_predict_valid_text():
    """Test pour prédire un sentiment avec un texte valide"""
    input_data = {"text": "I love this product!"}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "sentiment" in response.json()

def test_predict_missing_text():
    """Test avec un champ 'text' manquant"""
    input_data = {}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()
    assert "loc" in response.json()["detail"][0]  # Validation de la présence de 'loc'

def test_predict_empty_text():
    """Test avec un texte vide"""
    input_data = {"text": ""}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 400  # Mauvaise requête (texte vide)
    assert response.json() == {"detail": "Le texte ne peut pas être vide."}

def test_predict_number_text():
    """Test avec un texte contenant uniquement un nombre"""
    input_data = {"text": "12345"}
    response = client.post("/predict/", json=input_data)
    assert response.status_code == 400  # Texte ne peut pas être un nombre
    assert response.json() == {"detail": "Le texte ne peut pas être un nombre."}

def test_predict_invalid_json():
    """Test avec une requête mal formatée (données non JSON)"""
    response = client.post("/predict/", data="Invalid JSON")
    assert response.status_code == 422  # Unprocessable Entity
