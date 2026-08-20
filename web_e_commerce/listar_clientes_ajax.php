<?php
require_once "conexao.php";

$nome = $_POST["nome"] ?? "";
$cpf = $_POST["cpf"] ?? "";

$sql = "SELECT * FROM clientes WHERE 1=1";
$params = [];

if ($nome) {
    $sql .= " AND nome LIKE :nome";
    $params[":nome"] = "%$nome%";
}
if ($cpf) {
    $sql .= " AND cpf LIKE :cpf";
    $params[":cpf"] = "%$cpf%";
}

$stmt = $pdo->prepare($sql);
$stmt->execute($params);
$clientes = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (!$clientes) {
    echo "<div class='alert alert-info'>Nenhum cliente encontrado.</div>";
    exit;
}

echo "<table class='table table-bordered'>";
echo "<thead><tr><th>ID</th><th>Nome</th><th>CPF</th><th>Endereço</th><th>Data Nasc.</th><th>Ações</th></tr></thead><tbody>";

foreach ($clientes as $c) {
    echo "<tr>
            <td>{$c['id']}</td>
            <td>{$c['nome']}</td>
            <td>{$c['cpf']}</td>
            <td>{$c['endereco']}</td>
            <td>{$c['data_nascimento']}</td>
            <td>
                <button class='btn btn-sm btn-primary btn-edit'
                    data-id='{$c['id']}' 
                    data-nome='{$c['nome']}' 
                    data-cpf='{$c['cpf']}' 
                    data-endereco='{$c['endereco']}' 
                    data-data_nascimento='{$c['data_nascimento']}'>
                    Editar
                </button>
                <button class='btn btn-sm btn-danger btn-delete' data-id='{$c['id']}'>Excluir</button>
            </td>
          </tr>";
}
echo "</tbody></table>";
?>

