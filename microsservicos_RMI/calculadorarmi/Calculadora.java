/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package calculadorarmi;
import java.rmi.Remote;
import java.rmi.RemoteException;

/**
 *
 * @author kensl
 */
/*
A interface Calculadora estende java.rmi.Remote, o que a torna uma interface remota.
Isso significa que os métodos definidos nela podem ser chamados remotamente (de outro computador ou processo via rede).
O Remote é a marca registrada de que a interface será usada pelo mecanismo RMI do Java.
Esses métodos representam operações matemáticas simples: soma, subtração, divisão e multiplicação.
Todos eles:
    Recebem dois valores do tipo double.
    Retornam um double com o resultado.
    Lançam RemoteException, pois esse tipo de exceção pode ocorrer durante chamadas remotas (ex: falha de rede, servidor offline etc).
*/

public interface Calculadora extends Remote {
    double somar(double a, double b) throws RemoteException;
    double subtrair(double a, double b) throws RemoteException;
    double multiplicar(double a, double b) throws RemoteException;
    double dividir(double a, double b) throws RemoteException, calculadorarmi.excecoes.DivisaoPorZeroException;
}
