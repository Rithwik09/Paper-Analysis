from fastapi import FastAPI
from routes.python_routes import router as pdf_router 

app = FastAPI()

app.include_router(pdf_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
