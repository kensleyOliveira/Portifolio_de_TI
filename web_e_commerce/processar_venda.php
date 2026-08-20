<?php
    header('Content-Type: application/json');
    require_once "conexao.php";

    $response = ['status' => 'error', 'message' => 'Dados inválidos.'];

    if (isset($_POST['cliente_id']) && isset($_POST['carrinho'])) {
        $cliente_id = $_POST['cliente_id'];
        $carrinho = json_decode($_POST['carrinho'], true);
        
        if (empty($carrinho)) {
            $response['message'] = 'Carrinho vazio.';
            echo json_encode($response);
            exit;
        }

        $valor_total = 0;
        foreach ($carrinho as $item) {
            $valor_total += floatval($item['subtotal']);
        }

        try {
            // Inicia uma transação
            $pdo->beginTransaction();

            // 1. Insere na tabela 'vendas'
            $sql_venda = "INSERT INTO vendas (cliente_id, valor_total) VALUES (:cliente_id, :valor_total)";
            $stmt_venda = $pdo->prepare($sql_venda);
            $stmt_venda->bindParam(':cliente_id', $cliente_id, PDO::PARAM_INT);
            $stmt_venda->bindParam(':valor_total', $valor_total);
            $stmt_venda->execute();
            
            // Pega o ID da venda que acabamos de criar
            $venda_id = $pdo->lastInsertId();

            // 2. Insere cada item na tabela 'venda_itens'
            $sql_item = "INSERT INTO venda_itens (venda_id, produto_nome, quantidade, valor_unitario, subtotal) VALUES (:venda_id, :produto_nome, :quantidade, :valor_unitario, :subtotal)";
            $stmt_item = $pdo->prepare($sql_item);

            foreach ($carrinho as $item) {
                $stmt_item->execute([
                    ':venda_id' => $venda_id,
                    ':produto_nome' => $item['nome'],
                    ':quantidade' => $item['quantidade'],
                    ':valor_unitario' => $item['valor'],
                    ':subtotal' => $item['subtotal']
                ]);
            }
            
            // Se tudo deu certo, confirma a transação
            $pdo->commit();

            $response = ['status' => 'success', 'venda_id' => $venda_id];

        } catch (Exception $e) {
            // Se algo deu errado, desfaz a transação
            $pdo->rollBack();
            $response['message'] = 'Erro no banco de dados: ' . $e->getMessage();
        }
    }

echo json_encode($response);
?>