from typing import List

class ItemMenu:
    def __init__(self, nome: str, preco: float):
        self._nome = nome
        self._preco = preco
        
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def preco(self) -> float:
        return self._preco
    
    def descrever(self) -> str:
        return f"{self._nome}: R$ {self._preco:.2f}"
    
class Lanche(ItemMenu):
    def __init__(self, nome: str, preco: float, ingredientes: List[str]):
        super().__init__(nome, preco)
        self.ingredientes = ingredientes
    
    def descrever(self) -> str:
        ingredientes_str = ",".join(self.ingredientes)
        return f"{self._nome} (Ingredientes:{ingredientes_str}) - R$ {self._preco:.2f}"
    
class Bebida(ItemMenu):
    def __init__(self, nome: str, preco: float, tamanho_ml: int):
        super().__init__(nome, preco)
        self.tamanho_m1 = self.tamanho_m1
        
    def descrever(self) -> str:
        return f"{self._nome} ({self.tamanho_m1}m1) - R$ {self._preco:.2f}"
            

        
        

    
        


    
    
    
    
    
   
        