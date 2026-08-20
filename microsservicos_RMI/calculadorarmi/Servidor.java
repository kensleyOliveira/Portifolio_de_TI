/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package calculadorarmi;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

/**
 *
 * @author kensl
 */
/*
Esse código é o servidor RMI (Remote Method Invocation) de uma calculadora distribuída. Ele:
    - Cria o objeto que implementa a interface remota Calculadora, ou seja, a lógica real das operações (somar, subtrair, etc.).
    - Cria o registro RMI embutido diretamente no servidor, na porta 2000.
    - O registry é como um “catálogo” onde os serviços remotos ficam registrados para que clientes possam encontrá-los.
    - Registra a instância calc no RMI Registry com o nome "CalculadoraService".
    - Isso permite que clientes possam procurar por esse nome e usar os métodos remotamente.
    - Se algo der errado (ex: porta em uso, falha ao instanciar a calculadora), o erro é exibido no console.
Em suma, o código inicia um servidor RMI na porta 2000 e registra um serviço de calculadora para que possa ser acessado remotamente por clientes.

*/
public class Servidor {
    public static void main(String[] args) {
        try {
            Calculadora calc = new CalculadoraImpl();
            Registry registry = LocateRegistry.createRegistry(2000);
            registry.rebind("CalculadoraService", calc);
            System.out.println("Servidor pronto. Calculadora registrada no RMI Registry.");
        } catch (Exception e) {
            System.err.println("Erro no servidor: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
