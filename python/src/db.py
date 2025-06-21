from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.questionpaper import QuestionPaper

async def init_db():
    # client = AsyncIOMotorClient("mongodb://localhost:27017")
    client = AsyncIOMotorClient("mongodb+srv://rithwikchaithu09:1bavyCTvijvvLVNJ@paperanalysis.lwey1id.mongodb.net/")
    await init_beanie(database=client.mydb, document_models=[QuestionPaper])
