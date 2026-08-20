# ATIVIDADE: MAIS SOBRE OBJETOS DE VALOR (1)

### 1. CoordenadaGPS

Para o cálculo de distância foi usado a **Fórmula de Haversine**, que é o padrão para calcular a distância entre dois pontos em uma esfera (Terra).

> **Nota:** O enunciado da atividade pede longitude de 0 a 180, mas globalmente o padrão é -180 a +180. 

```java
public record CoordenadaGPS(double latitude, double longitude) {
    public CoordenadaGPS {
        if (latitude < -90 || latitude > 90) {
            throw new IllegalArgumentException("Latitude deve estar entre -90 e +90");
        }
        if (longitude < 0 || longitude > 180) {
            throw new IllegalArgumentException("Longitude deve estar entre 0 e 180");
        }
    }

    public double distanceTo(CoordenadaGPS outra) {
        final int R = 6371; // Raio da Terra em km
        double latDistance = Math.toRadians(outra.latitude - this.latitude);
        double lonDistance = Math.toRadians(outra.longitude - this.longitude);
        
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(this.latitude)) * Math.cos(Math.toRadians(outra.latitude))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c; // Retorno em quilômetros
    }
}

```

---

### 2. Senha (Value Object)

Aqui, o record recebe a senha "limpa", valida o tamanho e armazena apenas o **hash**. Usei o algoritmo SHA-256 para o exemplo.

```java
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

public record Senha(String hash) {
    public Senha {
        // O construtor compacto aqui espera que o valor já chegue processado ou validado
    }

    public static Senha criar(String senhaLimpa) {
        if (senhaLimpa == null || senhaLimpa.length() < 8) {
            throw new IllegalArgumentException("A senha deve ter no mínimo 8 caracteres.");
        }
        return new Senha(gerarHash(senhaLimpa));
    }

    private static String gerarHash(String texto) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedhash = digest.digest(texto.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().encodeToString(encodedhash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Erro ao processar hash da senha", e);
        }
    }
}

```

---

### 3. E-mail (Value Object)

Utilizei uma **Expressão Regular (Regex)** para garantir que apenas letras, números, pontos e sublinhados sejam aceitos, conforme a regra de negócio do exercício.

```java
import java.util.regex.Pattern;

public record Email(String endereco) {
    // Regex: Permite letras, números, . e _ antes e depois do @
    private static final String REGEX = "^[a-zA-Z0-9._]+@[a-zA-Z0-9._]+\\.[a-zA-Z0-9._]+$";
    private static final Pattern PATTERN = Pattern.compile(REGEX);

    public Email {
        if (endereco == null || !endereco.contains("@")) {
            throw new IllegalArgumentException("E-mail inválido: ausência de '@'.");
        }
        
        if (!PATTERN.matcher(endereco).matches()) {
            throw new IllegalArgumentException("Formato inválido. Use apenas letras, números, ponto e sublinhado.");
        }
    }
}

```

---

### Por que usar Records para isso?

* **Imutabilidade:** Um objeto de valor não deve mudar após criado. Se a coordenada mudar, você cria uma nova instância.
* **Expressividade:** O código fica muito mais limpo (sem getters/setters repetitivos).
* **Segurança:** A validação no construtor garante que nunca existirá um `Email` ou uma `Senha` inválida circulando no seu sistema.
