<?php
    // Inclui o arquivo de conexão
    require_once "conexao.php";

    // Verifica se o formulário foi enviado (método POST)
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Prepara uma instrução de inserção
        $sql = "INSERT INTO clientes (nome, endereco, cpf, data_nascimento) VALUES (:nome, :endereco, :cpf, :data_nascimento)";

        if ($stmt = $pdo->prepare($sql)) {
            // Vincula as variáveis aos parâmetros da instrução preparada
            $stmt->bindParam(":nome", $_POST["nome"], PDO::PARAM_STR);
            $stmt->bindParam(":endereco", $_POST["endereco"], PDO::PARAM_STR);
            $stmt->bindParam(":cpf", $_POST["cpf"], PDO::PARAM_STR);
            $stmt->bindParam(":data_nascimento", $_POST["data_nascimento"], PDO::PARAM_STR);
            
            // Tenta executar a instrução preparada
            if ($stmt->execute()) {
                // ALTERAÇÃO AQUI: Redireciona para a página inicial (home) com sucesso
                header("location: index.html");
                exit();
            } else {
                echo "Oops! Algo deu errado. Por favor, tente novamente mais tarde.";
            }
        }
        
        // Fecha a instrução
        unset($stmt);
    }

    // Fecha a conexão
    unset($pdo);
?>