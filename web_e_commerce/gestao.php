<?php
session_start();
require_once "conexao.php"; // Certifique-se de que está correto

$USERNAME = "kensley";
$PASSWORD = "123456";

// Logout
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: index.html");
    exit;
}

// Login via POST AJAX
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["action"]) && $_POST["action"] === "login") {
    $user = $_POST["username"] ?? "";
    $pass = $_POST["password"] ?? "";
    if ($user === $USERNAME && $pass === $PASSWORD) {
        $_SESSION["auth"] = true;
        echo json_encode(["ok" => true]);
    } else {
        echo json_encode(["ok" => false, "msg" => "Usuário ou senha inválidos"]);
    }
    exit;
}
?>
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gestão | EletroShop</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
  <header class="bg-primary text-white py-4">
    <div class="container text-center">
      <h1>⚡ EletroShop — Gestão</h1>
      <nav class="nav justify-content-center mt-2">
        <a class="nav-link text-white" href="index.html">Home</a>
        <a class="nav-link text-white" href="cadastro.html">Cadastro</a>
      </nav>
    </div>
  </header>

  <main class="container my-5">
    <?php if (!isset($_SESSION["auth"])): ?>
      <!-- Login -->
      <div class="card p-4 shadow-sm mx-auto" style="max-width:400px;">
        <h3 class="mb-3 text-center">Acesso à Gestão</h3>
        <form id="loginForm">
          <div class="mb-3">
            <label class="form-label">Usuário</label>
            <input type="text" name="username" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Senha</label>
            <input type="password" name="password" class="form-control" required>
          </div>
          <button class="btn btn-primary w-100" type="submit">Entrar</button>
        </form>
      </div>
      <script>
      $(function(){
        $("#loginForm").on("submit", function(e){
          e.preventDefault();
          var data = $(this).serialize() + "&action=login";
          $.post("gestao.php", data, function(resp){
            if (resp.ok) location.reload();
            else alert(resp.msg);
          }, "json");
        });
      });
      </script>
    <?php else: ?>
      <!-- Painel -->
      <div class="d-flex justify-content-between mb-4">
        <h3>Gestão de Clientes</h3>
        <div>
          <a href="index.html" class="btn btn-outline-secondary">Home</a>
          <a href="gestao.php?logout=1" class="btn btn-danger">Sair</a>
        </div>
      </div>

      <div class="card p-3 mb-4 shadow-sm">
        <form id="searchForm" class="row g-2 align-items-end">
          <div class="col-md-6">
            <label class="form-label">Nome</label>
            <input type="text" name="nome" class="form-control">
          </div>
          <div class="col-md-4">
            <label class="form-label">CPF</label>
            <input type="text" name="cpf" class="form-control">
          </div>
          <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Buscar</button>
          </div>
        </form>
      </div>

      <div id="results">Faça uma busca para listar clientes.</div>

      <!-- Modal editar -->
      <div class="modal fade" id="editModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <form id="editForm">
              <div class="modal-header">
                <h5 class="modal-title">Editar Cliente</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>
              <div class="modal-body">
                <input type="hidden" name="id" id="edit_id">
                <div class="mb-3">
                  <label class="form-label">Nome</label>
                  <input type="text" name="nome" id="edit_nome" class="form-control" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Endereço</label>
                  <input type="text" name="endereco" id="edit_endereco" class="form-control">
                </div>
                <div class="mb-3">
                  <label class="form-label">CPF</label>
                  <input type="text" name="cpf" id="edit_cpf" class="form-control">
                </div>
                <div class="mb-3">
                  <label class="form-label">Data Nascimento</label>
                  <input type="date" name="data_nascimento" id="edit_data" class="form-control">
                </div>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-success">Salvar</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <script>
      // Buscar clientes
      $("#searchForm").on("submit", function(e){
        e.preventDefault();
        $.post("listar_clientes_ajax.php", $(this).serialize(), function(html){
          $("#results").html(html);
        }).fail(()=>alert("Erro ao buscar clientes"));
      });

      // Abrir modal edição
      $(document).on("click", ".btn-edit", function(){
        $("#edit_id").val($(this).data("id"));
        $("#edit_nome").val($(this).data("nome"));
        $("#edit_endereco").val($(this).data("endereco"));
        $("#edit_cpf").val($(this).data("cpf"));
        $("#edit_data").val($(this).data("data_nascimento"));
        new bootstrap.Modal(document.getElementById("editModal")).show();
      });

      // Salvar edição
      $("#editForm").on("submit", function(e){
        e.preventDefault();
        $.post("editar_cliente_ajax.php", $(this).serialize(), function(resp){
            alert(resp.msg);
            if (resp.ok) {
                $("#searchForm").submit();
                bootstrap.Modal.getInstance(document.getElementById("editModal")).hide();
            }
        }, "json");
      });

      // Excluir cliente
      $(document).on("click", ".btn-delete", function(){
        if (!confirm("Deseja realmente excluir este cliente?")) return;
        let id = $(this).data("id");
        $.post("excluir_cliente_ajax.php", {id:id}, function(resp){
          alert(resp.msg);
          if (resp.ok) $("#searchForm").submit();
        }, "json");
      });
      </script>
    <?php endif; ?>
  </main>

  <footer class="bg-dark text-white text-center py-3 mt-5">
    <p>&copy; 2025 EletroShop - Todos os direitos reservados</p>
  </footer>
</body>
</html>
