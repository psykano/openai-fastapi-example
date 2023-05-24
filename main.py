import openai
import os

from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from database import Database

class AnimalRequest(BaseModel):
    name: str
    regen: bool = False

class AnimalResponse(BaseModel):
    name: str = ''
    superheroNames: str = ''

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

db = Database(os.getenv("DB_FILE"))
db.createTableIfNotExists()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/openai/animal/recent/{rowLimit}")
async def read_animals(rowLimit: int):
    rows = db.showRecent(rowLimit)
    return rows


@app.post("/openai/animal/")
async def create_animal(animal: AnimalRequest):
    animal.name = animal.name.strip().capitalize()
    superheroNames = ""

    # Check if prompt exists in cache
    #  If not, create new entry
    #  If so, just update the cache entry
    promptId = db.getPromptId(animal.name)
    if (promptId == 0):
        superheroNames = await getAnimalSuperheroNames(animal.name)
        superheroNames = superheroNames.strip()
        db.insertPrompt(animal.name, superheroNames)
    else:
        # Check if we want to regenerate new superhero names
        if (animal.regen == False):
            superheroNames = db.getPromptResultsFromId(promptId)
            db.updatePromptHit(promptId)
        else:
            superheroNames = await getAnimalSuperheroNames(animal.name)
            superheroNames = superheroNames.strip()
            db.updatePrompt(promptId, superheroNames)
    
    res = AnimalResponse()
    res.name = animal.name
    res.superheroNames = superheroNames
    return res


async def getAnimalSuperheroNames(animal):
    response = await openai.Completion.acreate(
        model="text-davinci-003",
        prompt=generate_prompt(animal),
        temperature=0.6,
    )
    return response.choices[0].text


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.
Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(animal)