<?php
    header('Content-Type: application/json');
    require_once "conexao.php";

    $response = ['status' => 'erro', 'message' => 'CPF não fornecido.'];

    if (isset($_POST['cpf'])) {
        $cpf = $_POST['cpf'];

        $sql = "SELECT id, nome FROM clientes WHERE cpf = :cpf";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':cpf', $cpf, PDO::PARAM_STR);
        $stmt->execute();

        if ($stmt->rowCount() > 0) {
            $cliente = $stmt->fetch(PDO::FETCH_ASSOC);
            $response = [
                'status' => 'encontrado',
                'cliente_id' => $cliente['id'],
                'nome' => $cliente['nome']
            ];
        } else {
            $response = ['status' => 'nao_encontrado'];
        }
    }

    echo json_encode($response);
?>