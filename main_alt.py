from fastapi import FastAPI

app = FastAPI(title="MES Day 4", version="1.0.0")

@app.get("/")
def root():
    return {"message": "MES System - Day 4 (Port 8001)", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/achievements")
def achievements():
    return [
        {"id": 1, "name": "First Blood", "points": 10},
        {"id": 2, "name": "Quality Master", "points": 25}
    ]

@app.get("/api/v1/leaderboard")
def leaderboard():
    return [
        {"rank": 1, "employee_name": "Ivan Petrov", "points": 150},
        {"rank": 2, "employee_name": "Maria Ivanova", "points": 135}
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
