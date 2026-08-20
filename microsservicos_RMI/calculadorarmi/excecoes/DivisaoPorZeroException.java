/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package calculadorarmi.excecoes;

/**
 *
 * @author kensl
 */
/*
Esse código define uma exceção personalizada em Java chamada DivisaoPorZeroException.
O código define uma exceção personalizada chamada DivisaoPorZeroException, usada para 
sinalizar que ocorreu uma tentativa de dividir por zero, permitindo um tratamento de 
erro mais claro e específico.
*/
public class DivisaoPorZeroException extends Exception {
    public DivisaoPorZeroException(String mensagem) {
        super(mensagem);
    }
}
