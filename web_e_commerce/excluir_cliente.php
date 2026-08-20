<?php
// Processa a operação de exclusão após a confirmação
if(isset($_GET["id"]) && !empty($_GET["id"])){
    require_once "conexao.php";
    
    $sql = "DELETE FROM clientes WHERE id = :id";
    
    if($stmt = $pdo->prepare($sql)){
        $stmt->bindParam(":id", $_GET["id"], PDO::PARAM_INT);
        
        if($stmt->execute()){
            // Excluído com sucesso, redireciona para a lista
            header("location: listar_clientes.php");
            exit();
        } else{
            echo "Oops! Algo deu errado. Por favor, tente novamente.";
        }
    }
    unset($stmt);
    unset($pdo);
} else{
    // Se não houver um ID, redireciona para a página de listagem
    header("location: listar_clientes.php");
    exit();
}
?>