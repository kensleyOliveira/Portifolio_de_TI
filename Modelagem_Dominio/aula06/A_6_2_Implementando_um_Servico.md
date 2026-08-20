# ATIVIDADE: IMPLEMENTANDO UM SERVIÇO


## 1. Estrutura das Classes de Entidade

Primeiro, definimos os modelos básicos para que o serviço funcione.

```java
import java.time.LocalDate;

// Representa o Usuário
class Usuario {
    private String nome;
    private String tipo; // Ex: "ALUNO", "PROFESSOR"
    private boolean regular;

    public Usuario(String nome, String tipo, boolean regular) {
        this.nome = nome;
        this.tipo = tipo;
        this.regular = regular;
    }

    public String getTipo() { return tipo; }
    public boolean isRegular() { return regular; }
}

// Representa o Livro
class Livro {
    private String titulo;
    private boolean disponivel;

    public Livro(String titulo) {
        this.titulo = titulo;
        this.disponivel = true;
    }

    public boolean isDisponivel() { return disponivel; }
    public void setDisponivel(boolean disponivel) { this.disponivel = disponivel; }
}

// Representa o Emprestimo realizado
class Emprestimo {
    private Livro livro;
    private Usuario usuario;
    private LocalDate dataDevolucao;

    public Emprestimo(Livro livro, Usuario usuario, LocalDate dataDevolucao) {
        this.livro = livro;
        this.usuario = usuario;
        this.dataDevolucao = dataDevolucao;
    }
}

```

---

## 2. Implementação do ServicoEmprestimo

Aqui está a lógica principal, tratando as exceções e as regras de data de devolução.

```java
import java.time.LocalDate;

public class ServicoEmprestimo {

    public Emprestimo emprestarLivro(Usuario usuario, Livro livro) throws Exception {
        
        // Regra 1: O livro deve estar disponível
        if (!livro.isDisponivel()) {
            throw new Exception("Operação cancelada: O livro já está emprestado.");
        }

        // Regra 2: O usuário deve estar em situação regular
        if (!usuario.isRegular()) {
            throw new Exception("Operação cancelada: Usuário possui pendências no sistema.");
        }

        // Regra 3: A data de devolução depende do tipo de usuário
        LocalDate hoje = LocalDate.now();
        LocalDate dataDevolucao;

        if (usuario.getTipo().equalsIgnoreCase("PROFESSOR")) {
            dataDevolucao = hoje.plusDays(30); // Professores têm 30 dias
        } else {
            dataDevolucao = hoje.plusDays(7);  // Alunos/Geral têm 7 dias
        }

        // Efetivando o empréstimo
        livro.setDisponivel(false);
        System.out.println("Empréstimo realizado com sucesso!");
        
        return new Emprestimo(livro, usuario, dataDevolucao);
    }
}

```

---
