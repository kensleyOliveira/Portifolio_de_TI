<?php
require_once "conexao.php";
header("Content-Type: application/json; charset=utf-8");

// Recebe dados do POST
$id = $_POST["id"] ?? null;
$nome = $_POST["nome"] ?? "";
$endereco = $_POST["endereco"] ?? "";
$cpf = $_POST["cpf"] ?? "";
$data_nascimento = $_POST["data_nascimento"] ?? "";

// Validações básicas
if (!$id || !is_numeric($id)) {
    echo json_encode(["ok"=>false,"msg"=>"ID inválido"]);
    exit;
}

if (!$nome) {
    echo json_encode(["ok"=>false,"msg"=>"O nome é obrigatório"]);
    exit;
}

try {
    $sql = "UPDATE clientes SET nome=:nome, endereco=:endereco, cpf=:cpf, data_nascimento=:data_nascimento WHERE id=:id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        ":nome" => $nome,
        ":endereco" => $endereco,
        ":cpf" => $cpf,
        ":data_nascimento" => $data_nascimento,
        ":id" => $id
    ]);

    if ($stmt->rowCount() > 0) {
        echo json_encode(["ok"=>true,"msg"=>"Cliente atualizado com sucesso!"]);
    } else {
        echo json_encode(["ok"=>false,"msg"=>"Nenhuma alteração realizada ou cliente não encontrado"]);
    }
} catch(PDOException $e) {
    echo json_encode(["ok"=>false,"msg"=>"Erro ao atualizar cliente: ".$e->getMessage()]);
}
?>
