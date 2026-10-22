import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="API de Produtos com SQLite")

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_BANCO = BASE_DIR / "loja.db"
CAMINHO_SCHEMA = BASE_DIR / "schema.sql"
PASTA_STATIC = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=PASTA_STATIC), name="static")


class ProdutoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    preco: float = Field(gt=0, allow_inf_nan=False)
    fabricante: str = Field(min_length=1)

    @field_validator("nome", "fabricante")
    @classmethod
    def validar_texto(cls, valor, info):
        valor = valor.strip()
        if not valor:
            raise ValueError(f"O campo {info.field_name} não pode conter apenas espaços")
        return valor


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar()
    try:
        conexao.executescript(CAMINHO_SCHEMA.read_text(encoding="utf-8"))
        conexao.commit()
    finally:
        conexao.close()


criar_tabela()


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(PASTA_STATIC / "index.html")


@app.get("/produtos")
def listar_produtos():
    conexao = conectar()
    try:
        linhas = conexao.execute(
            "SELECT id, nome, preco, fabricante FROM produtos ORDER BY id"
        ).fetchall()
        return [dict(linha) for linha in linhas]
    finally:
        conexao.close()


@app.get("/produtos/{produto_id}")
def buscar_produto(produto_id: int):
    conexao = conectar()
    try:
        linha = conexao.execute(
            "SELECT id, nome, preco, fabricante FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()
        if linha is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return dict(linha)
    finally:
        conexao.close()


@app.post("/produtos", status_code=201)
def criar_produto(produto: ProdutoEntrada):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "INSERT INTO produtos (nome, preco, fabricante) VALUES (?, ?, ?)",
            (produto.nome, produto.preco, produto.fabricante),
        )
        conexao.commit()
        return {
            "id": cursor.lastrowid,
            "nome": produto.nome,
            "preco": produto.preco,
            "fabricante": produto.fabricante,
        }
    finally:
        conexao.close()


@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: int, produto: ProdutoEntrada):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "UPDATE produtos SET nome = ?, preco = ?, fabricante = ? WHERE id = ?",
            (produto.nome, produto.preco, produto.fabricante, produto_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        conexao.commit()
        return {
            "id": produto_id,
            "nome": produto.nome,
            "preco": produto.preco,
            "fabricante": produto.fabricante,
        }
    finally:
        conexao.close()


@app.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int):
    conexao = conectar()
    try:
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE id = ?", (produto_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        conexao.commit()
        return {"mensagem": "Produto excluído com sucesso"}
    finally:
        conexao.close()