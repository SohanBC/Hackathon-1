# backend/main.py
from fastapi import FastAPI
from backend.routes.scan_url import router as scan_url_router

app = FastAPI(title="Fake App Detection API")
app.include_router(scan_url_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app , port=8000)