<?php
require_once "conexao.php";
header("Content-Type: application/json; charset=utf-8");

$id = $_POST["id"] ?? null;

if (!$id || !is_numeric($id)) {
    echo json_encode(["ok"=>false,"msg"=>"ID inválido"]);
    exit;
}

try {
    $stmt = $pdo->prepare("DELETE FROM clientes WHERE id = :id");
    $stmt->execute([":id"=>$id]);

    if ($stmt->rowCount() > 0) {
        echo json_encode(["ok"=>true,"msg"=>"Cliente excluído com sucesso!"]);
    } else {
        echo json_encode(["ok"=>false,"msg"=>"Cliente não encontrado"]);
    }
} catch(PDOException $e) {
    echo json_encode(["ok"=>false,"msg"=>"Erro: ".$e->getMessage()]);
}
?>