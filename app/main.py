from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import read_use_model, read_use_prompt, read_case

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# origins = [
#     "http://127.0.0.1:5173",
#     "http://localhost:5173",
#     "https://127.0.0.1:5173",
#     "https://localhost:5173",
# ]
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root():
    return {"message": "OK"}

@app.get("/favicon.ico")
async def get_favicon():
    return {"file": "static/favicon.ico"}

@app.get("/model")
async def get_model():
    model_name = read_use_model()
    return {"model": model_name}


@app.get("/prompt/{category}")
async def get_prompt(category):
    prompt = read_use_prompt(category)
    return {"prompt": prompt}

@app.get('/case/{id}')
async def get_case(id): 
    content = read_case(id)
    return {"case": content}