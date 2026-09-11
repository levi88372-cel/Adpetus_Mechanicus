class ContaBancaria:
    def __init__(self, titular: str, saldo_inicial: float):
        self._titular = titular
        self._saldo = saldo_inicial
        
    def deposistar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            print(f"Depositor de R${valor:.2f} realizado com sucesso!")
        else:
            print(f"Deposito invalido.")
            
            
    def consultar_saldo(self):
        return f"titular:{self._titular} | Saldo : R$ {self._saldo:.2f}"
    
    def sacar(self, valor: float):
        if 0 < valor <=  self._saldo:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado na conta comum")
        else:
            print("saldo insuficiente ou valor invalido.")
            
             
class ContaCorrente(ContaBancaria):
    def __init__(self, titular: str, saldo_inicial: float, limite_credito: float):
        super().__init__(titular, saldo_inicial)
        self._limite_credito = limite_credito
        
    def sacar(self, valor: float):
        saldo_total_disponivel = self._saldo + self._limite_credito
        if 0 < valor <= saldo_total_disponivel:
            self._saldo -= valor
            print(f"saque de R${valor:.2f} realizado no cheque especial/limite!")
        else:
            print("saque negado: limite excedido!")
            
class ContaPoupança(ContaBancaria):
    def rendimento_mensal(self):
        self._saldo += self._saldo * 0.005
        print("Rendimento de 0.5% aplicado a poupança!")
        
        
minha_cc = ContaCorrente (titular="Ana", saldo_inicial=100.00, limite_credito=500.0)
minha_cc.deposistar(50)
print(minha_cc.consultar_saldo())

minha_cc.sacar(300)
print(minha_cc.consultar_saldo())
print("-" * 40)

minha_poupança = ContaPoupança(titular="Carlos", saldo_inicial=1000.0)
minha_poupança.sacar(1200)

minha_poupança.rendimento_mensal()
print(minha_poupança.consultar_saldo())

              
        

        






































































































