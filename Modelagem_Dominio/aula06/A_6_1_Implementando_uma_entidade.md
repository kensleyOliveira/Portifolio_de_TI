# ATIVIDADE: IMPLEMENTANDO UM ENTIDADE


### Implementação da Entidade `Livro`

```java
import java.util.regex.Pattern;

public class Livro {
    private String isbn;
    private String titulo;
    private String autor; // Formato esperado: "Nome Sobrenome"
    private String sobrenomeAutor;
    private String nomeAutor;
    private int ano;
    private String editora;
    private String cidade;

    public Livro(String isbn, String titulo, String autor, int ano, String editora, String cidade) {
        if (!validarISBN(isbn)) {
            throw new IllegalArgumentException("ISBN inválido! O código deve conter 10 ou 13 dígitos numéricos.");
        }
        this.isbn = isbn;
        this.titulo = titulo;
        this.autor = autor;
        this.ano = ano;
        this.editora = editora;
        this.cidade = cidade;
        
        // Auxiliar para formatar a citação ABNT (separa o último nome)
        processarNomeAutor(autor);
    }

    // 2. Validação de ISBN (Simplificada para 10 ou 13 dígitos)
    private boolean validarISBN(String isbn) {
        if (isbn == null) return false;
        // Remove traços ou espaços para validar apenas os números
        String cleanIsbn = isbn.replaceAll("[\\s-]", "");
        return Pattern.matches("^(\\d{10}|\\d{13})$", cleanIsbn);
    }

    private void processarNomeAutor(String nomeCompleto) {
        String[] partes = nomeCompleto.trim().split(" ");
        if (partes.length > 1) {
            this.sobrenomeAutor = partes[partes.length - 1].toUpperCase();
            this.nomeAutor = nomeCompleto.substring(0, nomeCompleto.lastIndexOf(" "));
        } else {
            this.sobrenomeAutor = nomeCompleto.toUpperCase();
            this.nomeAutor = "";
        }
    }

    // 3. Regra de citação ABNT
    // Padrão: SOBRENOME, Nome. Título. Cidade: Editora, Ano.
    public String obterCitacaoABNT() {
        return String.format("%s, %s. %s. %s: %s, %d.", 
            sobrenomeAutor, nomeAutor, titulo, cidade, editora, ano);
    }

    // Getters
    public String getIsbn() { return isbn; }
    public String getTitulo() { return titulo; }
}

```

---

### Destaques da Solução:

* **Validação no Construtor:** Conforme solicitado, o construtor verifica o ISBN usando Expressões Regulares (`Regex`). Se o formato estiver incorreto, ele lança uma `IllegalArgumentException`, impedindo a criação de um objeto inválido.
* **Identidade Única:** O campo `isbn` atua como a chave natural da entidade.
* **Formatação ABNT:** O método `obterCitacaoABNT()` manipula a string do autor para colocar o último sobrenome em caixa alta, seguido pelo nome e os dados da publicação, respeitando a pontuação clássica das normas brasileiras.

---

### Exemplo de Uso:

```java
try {
    Livro meuLivro = new Livro("9788535902778", "Dom Casmurro", "Machado de Assis", 1899, "Editora Garnier", "Rio de Janeiro");
    System.out.println(meuLivro.obterCitacaoABNT());
    // Saída: ASSIS, Machado de. Dom Casmurro. Rio de Janeiro: Editora Garnier, 1899.
} catch (IllegalArgumentException e) {
    System.err.println(e.getMessage());
}

```

