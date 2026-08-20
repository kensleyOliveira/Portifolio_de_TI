<?php
require_once "conexao.php";

// Verifica se o formulário foi enviado
if($_SERVER["REQUEST_METHOD"] == "POST"){
    // Valida se o ID foi enviado
    if(isset($_POST["id"]) && !empty($_POST["id"])){
        $id = $_POST["id"];

        // Prepara a instrução de UPDATE
        $sql = "UPDATE clientes SET nome = :nome, endereco = :endereco, cpf = :cpf, data_nascimento = :data_nascimento WHERE id = :id";
        
        if($stmt = $pdo->prepare($sql)){
            $stmt->bindParam(":nome", $_POST["nome"], PDO::PARAM_STR);
            $stmt->bindParam(":endereco", $_POST["endereco"], PDO::PARAM_STR);
            $stmt->bindParam(":cpf", $_POST["cpf"], PDO::PARAM_STR);
            $stmt->bindParam(":data_nascimento", $_POST["data_nascimento"], PDO::PARAM_STR);
            $stmt->bindParam(":id", $id, PDO::PARAM_INT);
            
            if($stmt->execute()){
                // Redireciona para a lista de clientes após a atualização
                header("location: listar_clientes.php");
                exit();
            } else{
                echo "Algo deu errado. Por favor, tente novamente.";
            }
        }
        unset($stmt);
    }
}
unset($pdo);
?>