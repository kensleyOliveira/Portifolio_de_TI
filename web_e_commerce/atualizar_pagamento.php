<?php
    require_once "conexao.php";

    if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['venda_id']) && isset($_POST['metodo_pagamento'])) {
        $venda_id = $_POST['venda_id'];
        $metodo_pagamento = $_POST['metodo_pagamento'];

        $sql = "UPDATE vendas SET metodo_pagamento = :metodo_pagamento, status = 'pago' WHERE id = :venda_id";
        $stmt = $pdo->prepare($sql);
        
        $stmt->bindParam(':metodo_pagamento', $metodo_pagamento, PDO::PARAM_STR);
        $stmt->bindParam(':venda_id', $venda_id, PDO::PARAM_INT);
        
        if ($stmt->execute()) {
            // Redireciona para uma página de sucesso
            header("Location: compra_sucesso.html");
            exit();
        } else {
            echo "Erro ao atualizar o pagamento.";
        }
    } else {
        // Redireciona se os dados estiverem incorretos
        header("Location: index.html");
        exit();
    }
?>