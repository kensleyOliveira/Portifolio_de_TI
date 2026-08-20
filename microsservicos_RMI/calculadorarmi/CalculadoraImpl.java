/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package calculadorarmi;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import calculadorarmi.excecoes.DivisaoPorZeroException;

/**
 *
 * @author kensl
 */
/*
CalculadoraImpl é a implementação concreta da interface Calculadora.
Herda de UnicastRemoteObject, que é obrigatório para objetos remotos no RMI:
Isso permite que o objeto seja exportado e possa aceitar chamadas remotas de clientes RMI.
Implementa Calculadora, a interface que define os métodos que o cliente poderá usar remotamente.
*/

public class CalculadoraImpl extends UnicastRemoteObject implements Calculadora {

    protected CalculadoraImpl() throws RemoteException {
        super();
    }

    public double somar(double a, double b) throws RemoteException {
        return a + b;
    }

    public double subtrair(double a, double b) throws RemoteException {
        return a - b;
    }

    public double multiplicar(double a, double b) throws RemoteException {
        return a * b;
    }

    public double dividir(double a, double b) throws RemoteException, DivisaoPorZeroException {
        if (b == 0) {
            throw new DivisaoPorZeroException("Erro: Divisão por zero não é permitida.");
        }
        return a / b;
    }
}
