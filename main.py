from fastapi import FastAPI
from pydantic import BaseModel
from model import search_tools
from fastapi.middleware.cors import CORSMiddleware

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
    return {"results": results}
