<?php
// Inclui o arquivo de conexão
require_once "conexao.php";

// Define variáveis e inicializa com valores vazios
$nome = $endereco = $cpf = $data_nascimento = "";
$id = 0;

// Verifica se um ID foi passado pela URL
if(isset($_GET["id"]) && !empty(trim($_GET["id"]))){
    $id = trim($_GET["id"]);
    
    // Prepara a consulta para buscar o cliente
    $sql = "SELECT * FROM clientes WHERE id = :id";
    if($stmt = $pdo->prepare($sql)){
        $stmt->bindParam(":id", $id, PDO::PARAM_INT);
        
        if($stmt->execute()){
            if($stmt->rowCount() == 1){
                $row = $stmt->fetch(PDO::FETCH_ASSOC);
                // Recupera os valores dos campos
                $nome = $row["nome"];
                $endereco = $row["endereco"];
                $cpf = $row["cpf"];
                $data_nascimento = $row["data_nascimento"];
            } else{
                header("location: listar_clientes.php");
                exit();
            }
        } else{
            echo "Oops! Algo deu errado. Tente novamente.";
        }
    }
    unset($stmt);
} else{
    header("location: listar_clientes.php");
    exit();
}
unset($pdo);
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Editar Cliente | EletroShop</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <main class="container my-5">
        <h2 class="text-center mb-4">Editar Cliente</h2>
        <form action="atualizar_cliente.php" method="post" class="mx-auto" style="max-width: 600px;">
            <input type="hidden" name="id" value="<?php echo $id; ?>"/>
            <div class="mb-3">
                <label class="form-label">Nome</label>
                <input type="text" name="nome" class="form-control" value="<?php echo htmlspecialchars($nome); ?>" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Endereço</label>
                <input type="text" name="endereco" class="form-control" value="<?php echo htmlspecialchars($endereco); ?>" required>
            </div>
            <div class="mb-3">
                <label class="form-label">CPF</label>
                <input type="text" name="cpf" class="form-control" value="<?php echo htmlspecialchars($cpf); ?>" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Data de Nascimento</label>
                <input type="date" name="data_nascimento" class="form-control" value="<?php echo $data_nascimento; ?>" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Salvar Alterações</button>
            <a href="listar_clientes.php" class="btn btn-secondary w-100 mt-2">Cancelar</a>
        </form>
    </main>
</body>
</html>