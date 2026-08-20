/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package calculadorarmi;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import calculadorarmi.excecoes.DivisaoPorZeroException;
import javax.swing.JOptionPane;

/**
 *
 * @author kensl
 */
/*
Esse código é o cliente de uma calculadora distribuída via RMI (Remote Method Invocation). Ele:
    - Acessa o registro RMI que está rodando no localhost na porta 2000.
    - Obtém uma referência remota ao serviço de calculadora chamado "CalculadoraService".
    - Mostra um menu com as operações: somar, subtrair, multiplicar, dividir e sair.
    - Lê a escolha do usuário.
    - Solicita dois números reais, senda a casa dos decimais separada por ponto via caixas de entrada.
    - Envia os valores para o servidor que realiza o cálculo e retorna o resultado.
    - Exibe o resultado em um JOptionPane.
    - Verifica se os números inseridos são válidos.
    - Trata a exceção personalizada DivisaoPorZeroException, exibindo uma mensagem de erro caso o usuário tente dividir por zero.
    - Trata também exceções gerais (como falha de conexão com o servidor).

Inicialização do programa
    Prompt - No diretório CalculadoraRMI
        Incia: start rmiregistry
    Botão direito do mouse clique em run.file, sobre o Servidor.Java 
    Botão direito do mouse clique em run.file, sobre o Cliente.Java 
    Prompt - No diretório CalculadoraRMI
        Encerra: taskkill /F /IM rmiregistry.exe
*/
public class Cliente {
    public static void main(String[] args) {
        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 2000);
            Calculadora calc = (Calculadora) registry.lookup("CalculadoraService");

            String menu = """
            === Calculadora Distribuída RMI ===
            Escolha a operação:
            1 - Somar
            2 - Subtrair
            3 - Multiplicar
            4 - Dividir
            0 - Sair
            """;

            while (true) {
                String opStr = JOptionPane.showInputDialog(menu);
                if (opStr == null) break;  // Usuário cancelou

                int op;
                try {
                    op = Integer.parseInt(opStr);
                } catch (NumberFormatException e) {
                    JOptionPane.showMessageDialog(null, "Entrada inválida.");
                    continue;
                }

                if (op == 0) break;

                // Entrada dos operandos
                String aStr = JOptionPane.showInputDialog("Digite o primeiro número:");
                String bStr = JOptionPane.showInputDialog("Digite o segundo número:");
                if (aStr == null || bStr == null) continue;

                double a, b;
                try {
                    a = Double.parseDouble(aStr);
                    b = Double.parseDouble(bStr);
                } catch (NumberFormatException e) {
                    JOptionPane.showMessageDialog(null, "Número inválido.");
                    continue;
                }

                // Executar operação
                try {
                    double resultado = switch (op) {
                        case 1 -> calc.somar(a, b);
                        case 2 -> calc.subtrair(a, b);
                        case 3 -> calc.multiplicar(a, b);
                        case 4 -> calc.dividir(a, b);
                        default -> {
                            JOptionPane.showMessageDialog(null, "Opção inválida.");
                            yield 0;
                        }
                    };

                    JOptionPane.showMessageDialog(null, "Resultado: " + resultado);
                } catch (DivisaoPorZeroException e) {
                    JOptionPane.showMessageDialog(null, e.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
                }
            }

        } catch (Exception e) {
            JOptionPane.showMessageDialog(null, "Erro no cliente: " + e.getMessage());
            e.printStackTrace();
        }
    }
}