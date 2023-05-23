# OpenAI example using FastAPI

## Features
* Asynchronous endpoints
* Caches results from prompt

## Get started

Run the following to get started
```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Then you can start the server with
```
uvicorn main:app --reload
```

## First

Head over to http://127.0.0.1:8000

You will see

```
{"Hello": "World"}
```

Head over to http://127.0.0.1:8000/docs

Or over to http://127.0.0.1:8000/redoc

You will see automatic API documentation

## Check it out

Head over to http://127.0.0.1:8000/static/index.html

You will see the homepage

![alt text](homepage.png?raw=true "Homepage")