# from fastapi import FastAPI
# from routes.python_routes import router as pdf_router 

# app = FastAPI()

# app.include_router(pdf_router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from routes.python_routes import router as pdf_router

# 👇 Lifespan context for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    uri = "mongodb+srv://rithwikchaithu09:1bavyCTvijvvLVNJ@paperanalysis.lwey1id.mongodb.net/"
    app.mongodb_client = AsyncIOMotorClient(uri)
    app.mongodb = app.mongodb_client["PaperAnalysis"]
    yield
    app.mongodb_client.close()

    print("🛑 MongoDB connection closed")

# 🌀 Initialize FastAPI with lifespan context
app = FastAPI(lifespan=lifespan)

# 📌 Register router
app.include_router(pdf_router)

# 🔁 Dev server (optional for script execution)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
