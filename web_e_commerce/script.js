const produtos = [
  { nome: "Disjuntor 10A", preco: 15.00, unidade: "unidade", imagem: "imagens/disjuntor.png" },
  { nome: "Fio 2,5mm 100m", preco: 120.00, unidade: "metro", imagem: "imagens/fios.png" }
];

// Carregar produtos na página de produtos
function carregarProdutos() {
  const $container = $("#lista-produtos");
  if ($container.length === 0) return;

  $container.empty();
  $.each(produtos, function (_, produto) {
    const $card = $(`
      <div class="produto-card">
        <img src="${produto.imagem}" alt="${produto.nome}" />
        <h3>${produto.nome}</h3>
        <p>R$ ${produto.preco.toFixed(2)} / ${produto.unidade}</p>
        <a href="venda.html?produto=${encodeURIComponent(produto.nome.toLowerCase())}&nome=${encodeURIComponent(produto.nome)}&valor=${produto.preco}&unidade=${produto.unidade}" class="botao">Ver detalhes</a>
      </div>
    `);
    $container.append($card);
  });
}

// Adicionar item ao carrinho a partir da página de detalhes
function adicionarAoCarrinhoDetalhado() {
  const params = new URLSearchParams(window.location.search);
  const nome = params.get("nome") || "Produto";
  const valor = parseFloat(params.get("valor") || "0");
  const unidade = params.get("unidade") || "unidade";
  const quantidade = parseInt($("input[name='quantidade']").val(), 10);

  if (!quantidade || quantidade <= 0) {
    alert("Informe uma quantidade válida.");
    return;
  }

  let cor = "", diametro = "";
  if (unidade === "metro") {
    cor = $("select[name='cor']").val();
    diametro = $("select[name='diametro']").val();
    if (!cor) { alert("Selecione a cor."); return; }
    if (!diametro) { alert("Selecione o diâmetro."); return; }
  }

  const item = { nome, valor, unidade, quantidade, subtotal: (valor * quantidade).toFixed(2), cor, diametro };
  const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  carrinho.push(item);
  localStorage.setItem("carrinho", JSON.stringify(carrinho));
  
  alert("Produto adicionado ao carrinho com sucesso!");
}


// Adiciona ao carrinho e redireciona para a página do carrinho
function comprarAgora() {
  // Primeiro, executa a função de adicionar o item
  adicionarAoCarrinhoDetalhado();
  // Em seguida, redireciona o usuário
  window.location.href = 'carrinho.html';
}

// Carregar itens na página do carrinho
function carregarCarrinho() {
  const $container = $("#carrinho-lista");
  if ($container.length === 0) return;

  const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  if (carrinho.length === 0) {
    $container.html("<p>Seu carrinho está vazio.</p>");
    return;
  }

  const $ul = $("<ul class='list-group'>");
  $.each(carrinho, function (index, item) {
    const $li = $(`
      <li class="list-group-item">
        <strong>${item.nome}</strong><br>
        Quantidade: <input type="number" class="form-control d-inline w-25 me-2 qtd-item" value="${item.quantidade}" min="1" data-index="${index}">
        ${item.unidade}(s) - R$ ${item.valor.toFixed(2)} cada<br>
        Subtotal: <span class="subtotal">R$ ${item.subtotal}</span><br>
        ${item.cor ? "Cor: " + item.cor + "<br>" : ""}
        ${item.diametro ? "Diâmetro: " + item.diametro + "<br>" : ""}
        <div class="mt-2">
          <button class="btn btn-sm btn-warning alterar-item" data-index="${index}">Alterar</button>
          <button class="btn btn-sm btn-danger excluir-item" data-index="${index}">Excluir</button>
        </div>
      </li>
    `);
    $ul.append($li);
  });
  $container.empty().append($ul);
}

// Excluir item do carrinho
$(document).on("click", ".excluir-item", function () {
  const index = $(this).data("index");
  let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  carrinho.splice(index, 1);
  localStorage.setItem("carrinho", JSON.stringify(carrinho));
  carregarCarrinho();
});

// Alterar quantidade no carrinho
$(document).on("click", ".alterar-item", function () {
  const index = $(this).data("index");
  let carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  const novaQtd = parseInt($(`.qtd-item[data-index="${index}"]`).val(), 10);

  if (novaQtd > 0) {
    carrinho[index].quantidade = novaQtd;
    carrinho[index].subtotal = (carrinho[index].valor * novaQtd).toFixed(2);
    localStorage.setItem("carrinho", JSON.stringify(carrinho));
  }
  carregarCarrinho();
});

// Carregar detalhes na página de venda
function carregarDetalhesProduto() {
  if (!$("body").find("#nome-produto").length) return;
  const params = new URLSearchParams(window.location.search);
  const nome = params.get("nome");
  const valor = params.get("valor");
  const unidade = params.get("unidade") || "unidade";
  $("#nome-produto").text(nome || "Produto");
  $("#valor-produto").text(parseFloat(valor || "0").toFixed(2));
  $("#unidade").text(unidade === "metro" ? "por metro" : "por unidade");

  if (unidade === "metro") {
    $("#campos-dinamicos").html(`
      <label>Cor: <select name="cor" required><option value="">Selecione</option><option value="azul">Azul</option><option value="vermelho">Vermelho</option><option value="preto">Preto</option></select></label>
      <label>Diâmetro: <select name="diametro" required><option value="">Selecione</option><option value="1.5mm">1.5 mm</option><option value="2.5mm">2.5 mm</option><option value="4mm">4 mm</option></select></label>
    `);
  }
}

// Execução principal quando o documento está pronto
$(document).ready(function () {
  carregarProdutos();
  carregarCarrinho();
  carregarDetalhesProduto();
});

// ===================================================================
// LÓGICA DE CHECKOUT
// ===================================================================

let clienteVerificadoId = null; 

// 1. Ao clicar em Finalizar Compra, abre o modal
$(document).on("click", "#finalizar-compra", function () {
  const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  if (carrinho.length === 0) {
    alert("Seu carrinho está vazio!");
    return;
  }
  $('#clienteModal').modal('show');
});

// 2. Ao submeter o formulário de verificação de CPF
$('#form-verificar-cliente').on('submit', function(e) {
  e.preventDefault();
  const cpf = $('#cpfCliente').val();

  $.ajax({
    url: 'verificar_cliente.php',
    type: 'POST',
    data: { cpf: cpf },
    dataType: 'json',
    success: function(response) {
      if (response.status === 'encontrado') {
        $('#cliente-info').html(`Cliente encontrado: <strong>${response.nome}</strong>`).show();
        $('#prosseguir-compra').show();
        clienteVerificadoId = response.cliente_id;
      } else {
        alert('Cliente não encontrado. Você será redirecionado para a página de cadastro.');
        window.location.href = 'cadastro.html';
      }
    },
    error: function() {
      alert('Ocorreu um erro ao verificar o cliente. Tente novamente.');
    }
  });
});

// 3. Ao clicar no botão de Prosseguir para Pagamento
$('#prosseguir-compra').on('click', function() {
  const carrinho = JSON.parse(localStorage.getItem("carrinho")) || [];
  if (!clienteVerificadoId) {
    alert('Erro: ID do cliente não encontrado.');
    return;
  }

  $.ajax({
    url: 'processar_venda.php',
    type: 'POST',
    data: {
      cliente_id: clienteVerificadoId,
      carrinho: JSON.stringify(carrinho)
    },
    dataType: 'json',
    success: function(response) {
      if (response.status === 'success') {
        localStorage.removeItem('carrinho');
        // SE CHEGAR AQUI, O REDIRECIONAMENTO ACONTECE
        window.location.href = `pagamento.html?venda_id=${response.venda_id}`;
      } else {
        alert('Erro ao processar a venda: ' + response.message);
      }
    },
    error: function() {
      alert('Ocorreu um erro ao registrar a venda. Tente novamente.');
    }
  });
});