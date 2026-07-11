"""FastAPI application entry point."""
from fastapi import FastAPI

app = FastAPI(title="Tiny Python")

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
