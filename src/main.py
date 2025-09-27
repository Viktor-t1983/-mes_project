from fastapi import FastAPI

app = FastAPI(
    title="MES-X v4.0",
    description="Система управления производством (MES) для несерийного производства",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в MES-X v4.0!"}

@app.get("/health")
def health_check():
    return {"status": "OK", "version": "0.1.0"}
  feat: add main.py with FastAPI endpoint
