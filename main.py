import openai
import os

from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/openai/{animal}")
async def read_item(animal: str):
    response = await openai.Completion.acreate(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
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