import uvicorn

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

templates = Jinja2Templates(directory="templates")

# Create object of ChatBot class with Storage Adapter
bot = ChatBot(
    'Buddy',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        {   
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Maaf, saya tidak faham.',
            'maximum_similarity_threshold': 0.90
        }],
    read_only=True
)

trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "chatterbot.corpus.indonesia"
)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/getChatBotResponse")
def get_bot_response(msg: str):
    return str(bot.get_response(msg))

if __name__ == "__main__":
    uvicorn.run("main:app")