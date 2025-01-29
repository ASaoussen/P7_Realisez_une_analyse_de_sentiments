from fastapi import FastAPI

# Création de l'application FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API d'Analyse de Sentiments !"}

# Code pour démarrer l'API via Uvicorn (si nécessaire)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)