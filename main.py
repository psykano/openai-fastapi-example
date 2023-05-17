import openai
import os

from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from database import Database

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

db = Database(os.getenv("DB_FILE"))
db.createAnimalTableIfNotExists()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/openai/animal/{animalId}")
async def read_animal(animalId: int):
    # get from db
    animalName = 'test'
    names = 'test1, test2, test3'
    return {"animal_id": animalId, "animal_name": animalName, "names": names}


@app.post("/openai/animal/{name}")
async def update_animal(name: str):
    response = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=generate_prompt(name),
            temperature=0.6,
        )
    # store in db
    return {"animal": animal, "names": response.choices[0].text}


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize(),
    )