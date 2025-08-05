from fastapi import FastAPI
from pydantic import BaseModel
from model import search_tools
from fastapi.middleware.cors import CORSMiddleware
from textgen import generar_respuesta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
def search(request: SearchRequest):
    results = search_tools(request.query)
    respuesta = generar_respuesta(request.query, results)
    return {
        "message": respuesta,
        "results": results
    }
