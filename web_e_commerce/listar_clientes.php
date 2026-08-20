<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Clientes Cadastrados | EletroShop</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header class="bg-primary text-white py-4">
    <div class="container text-center">
      <h1>⚡ EletroShop</h1>
      <nav class="nav justify-content-center mt-3">
        <a class="nav-link text-white" href="index.html">Home</a>
        <a class="nav-link text-white" href="produtos.html">Produtos</a>
        <a class="nav-link text-white" href="cadastro.html">Novo Cliente</a>
      </nav>
    </div>
  </header>

  <main class="container my-5">
    <h2 class="text-center mb-4">Clientes Cadastrados</h2>
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>#</th>
            <th>Nome</th>
            <th>Endereço</th>
            <th>CPF</th>
            <th>Data de Nascimento</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <?php
          require_once "conexao.php";
          
          $sql = "SELECT * FROM clientes ORDER BY nome";
          if ($result = $pdo->query($sql)) {
              if ($result->rowCount() > 0) {
                  while ($row = $result->fetch()) {
                      echo "<tr>";
                      echo "<td>" . $row['id'] . "</td>";
                      echo "<td>" . htmlspecialchars($row['nome']) . "</td>";
                      echo "<td>" . htmlspecialchars($row['endereco']) . "</td>";
                      echo "<td>" . htmlspecialchars($row['cpf']) . "</td>";
                      echo "<td>" . date("d/m/Y", strtotime($row['data_nascimento'])) . "</td>";
                      echo '<td>
                              <a href="editar_cliente.php?id='. $row['id'] .'" class="btn btn-warning btn-sm">Editar</a>
                              <a href="excluir_cliente.php?id='. $row['id'] .'" class="btn btn-danger btn-sm" onclick="return confirm(\'Tem certeza que deseja excluir este cliente?\');">Excluir</a>
                            </td>';
                      echo "</tr>";
                  }
                  unset($result);
              } else {
                  echo '<tr><td colspan="6" class="text-center">Nenhum cliente cadastrado.</td></tr>';
              }
          } else {
              echo '<tr><td colspan="6" class="text-center">ERRO: Não foi possível executar a consulta.</td></tr>';
          }
          unset($pdo);
          ?>
        </tbody>
      </table>
    </div>
  </main>
  
  <footer class="bg-dark text-white text-center py-3 mt-5">
    <p>&copy; 2025 EletroShop - Todos os direitos reservados</p>
  </footer>

</body>
</html>