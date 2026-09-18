class ItemMenu:
    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self._preco = preco

    def get_preco(self) -> float:
        return self._preco


class Entregas:
    def __init__(self, endereco: str, distancia_km: float):
        self.endereco = endereco
        self.distancia_km = distancia_km


class EntregaPropia(Entregas):
    def calcular_frete(self) -> float:
        return 4.00 + (self.distancia_km * 1.50)

    def tempo_estimado(self) -> str:
        return "28 a 40 minutos (delivery)"

cardapio = {
    "1": ItemMenu("Esfiha", 2.90),
    "2": ItemMenu("Kibe Tradicional", 4.90),
    "3": ItemMenu("Refrigerante 2L", 11.00)
}

def executar_sistema():
    print("=" * 50)
    print("   SISTEMA DE PEDIDOS ")
    print("=" * 50)

    cliente = input("Digite o seu nome: ")
    endereco = input("Digite o seu endereço: ")
    
    try:
        distancia = float(input("Distância até ao restaurante (em km): "))
    except ValueError:
        print("Distância inválida! A usar o valor padrão de 1.0 km.")
        distancia = 1.0

    entrega = EntregaPropia(endereco, distancia)
    itens_pedidos = []
    subtotal = 0.0

    print("\n--- CARDÁPIO ---")
    for chave, item in cardapio.items():
        print(f"[{chave}] {item.nome} - R$ {item.get_preco():.2f}")

    while True:
        opcao = input("\nEscolha o número do item (ou '0' para finalizar): ")
        if opcao == "0":
            break

        if opcao in cardapio:
            item = cardapio[opcao]
            try:
                qtd = int(input(f"Quantidade de '{item.nome}': "))
            except ValueError:
                print("Quantidade inválida! Tente novamente.")
                continue

            if qtd > 0:
                total_item = item.get_preco() * qtd
                subtotal += total_item
                itens_pedidos.append({"nome": item.nome, "qtd": qtd, "total": total_item})
                print(f"Adicionado: {qtd}x {item.nome}")
        else:
            print("Opção inválida! Tente novamente.")

    if not itens_pedidos:
        print("\nNenhum item foi selecionado. Pedido cancelado.")
        return

    frete = entrega.calcular_frete()
    total_geral = subtotal + frete

    
    print("\n" + "=" * 50)
    print("  COMPROVANTE DE PEDIDO ")
    print("=" * 50)
    print(f"Cliente: {cliente}")
    print(f"Endereço: {endereco}")
    print(f"Tempo Estimado: {entrega.tempo_estimado()}")
    print("-" * 50)
    print("ITENS:")
    for item in itens_pedidos:
        print(f" • {item['qtd']}x {item['nome']:<28} R$ {item['total']:.2f}")

    print("-" * 50)
    print(f"Subtotal: R$ {subtotal:.2f}")
    print(f"Taxa de Entrega: R$ {frete:.2f}")
    print(f"TOTAL A PAGAR: R$ {total_geral:.2f}")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    executar_sistema()