CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
    preco REAL NOT NULL CHECK (preco > 0),
    fabricante TEXT NOT NULL CHECK (length(trim(fabricante)) > 0)
);