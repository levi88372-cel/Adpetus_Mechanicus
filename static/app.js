const API = "/produtos";

const form = document.getElementById("form-produto");
const lista = document.getElementById("lista");
const mensagem = document.getElementById("mensagem");
const tituloForm = document.getElementById("titulo-form");
const btnCancelar = document.getElementById("btn-cancelar");

let editandoId = null; // null = criando; número = editando

function mostrarMensagem(texto, tipo) {
  mensagem.textContent = texto;
  mensagem.className = tipo;
}

function formatarPreco(valor) {
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function criarBotao(texto, classe, aoClicar) {
  const botao = document.createElement("button");
  botao.type = "button";
  botao.textContent = texto;
  if (classe) botao.className = classe;
  botao.addEventListener("click", aoClicar);
  return botao;
}

// Extrai a mensagem de erro que o FastAPI devolve (string ou lista de erros 422)
async function lerErro(resposta) {
  try {
    const dados = await resposta.json();
    if (typeof dados.detail === "string") return dados.detail;
    if (Array.isArray(dados.detail)) return dados.detail.map((e) => e.msg).join("; ");
  } catch (_) {}
  return "Erro inesperado no sistema.";
}

async function carregarProdutos() {
  const resposta = await fetch(API);
  const produtos = await resposta.json();

  lista.replaceChildren();

  for (const p of produtos) {
    const linha = document.createElement("tr");

    for (const valor of [p.id, p.nome, formatarPreco(p.preco), p.fabricante]) {
      const celula = document.createElement("td");
      celula.textContent = valor; // textContent evita injeção de HTML
      linha.appendChild(celula);
    }

    const acoes = document.createElement("td");
    acoes.appendChild(criarBotao("Editar", "secundario", () => iniciarEdicao(p)));
    acoes.appendChild(criarBotao("Excluir", "perigo", () => excluirProduto(p.id)));
    linha.appendChild(acoes);

    lista.appendChild(linha);
  }
}

function iniciarEdicao(produto) {
  editandoId = produto.id;
  form.elements.nome.value = produto.nome;
  form.elements.preco.value = produto.preco;
  form.elements.fabricante.value = produto.fabricante;
  tituloForm.textContent = `Editando registro #${produto.id}`;
  btnCancelar.hidden = false;
  form.elements.nome.focus();
}

function resetarFormulario() {
  editandoId = null;
  form.reset();
  tituloForm.textContent = "Novo registro";
  btnCancelar.hidden = true;
}

async function excluirProduto(id) {
  if (!confirm("Confirma a remoção deste item do inventário oficial?")) return;

  const resposta = await fetch(`${API}/${id}`, { method: "DELETE" });
  if (!resposta.ok) {
    mostrarMensagem(await lerErro(resposta), "erro");
    return;
  }

  mostrarMensagem("Item removido do inventário.", "sucesso");
  if (editandoId === id) resetarFormulario();
  carregarProdutos();
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault(); // impede o recarregamento da página

  const dados = {
    nome: form.elements.nome.value,
    preco: parseFloat(form.elements.preco.value),
    fabricante: form.elements.fabricante.value,
  };

  const url = editandoId === null ? API : `${API}/${editandoId}`;
  const metodo = editandoId === null ? "POST" : "PUT";

  const resposta = await fetch(url, {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });

  if (!resposta.ok) {
    mostrarMensagem(await lerErro(resposta), "erro");
    return;
  }

  mostrarMensagem(
    editandoId === null ? "Registro incluído no inventário." : "Registro atualizado.",
    "sucesso"
  );
  resetarFormulario();
  carregarProdutos();
});

btnCancelar.addEventListener("click", resetarFormulario);

carregarProdutos();