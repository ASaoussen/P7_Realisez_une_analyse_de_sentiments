from fastapi import FastAPI
import uvicorn

# Création de l'application FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API d'Analyse de Sentiments !"}
