from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    imagem: str
    descricao: str

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    conn = get_db_connection()
    produtos = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [Produto(**dict(p)) for p in produtos]
