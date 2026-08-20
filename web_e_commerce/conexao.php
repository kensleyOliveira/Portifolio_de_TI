<?php
    // Configurações do banco de dados
    $servidor = 'localhost';
    $usuario = 'root';
    $senha = 'mysql'; // Senha informada na sua solicitação.
    $banco = 'eletroshop'; // Nome do banco de dados criado

    try {
        // Cria uma nova conexão PDO
        $pdo = new PDO("mysql:host=$servidor;dbname=$banco;charset=utf8", $usuario, $senha);
        
        // Define o modo de erro do PDO para exceção
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
    } catch(PDOException $e) {
        // Se a conexão falhar, exibe uma mensagem de erro
        die("ERRO: Não foi possível conectar ao banco de dados. " . $e->getMessage());
    }
?>