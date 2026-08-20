package Mediator;

import Flyweight.Car;

//TrafficMediator (Interface do Mediator): Esta interface (TrafficMediator)
// define o contrato para a comunicação entre os objetos. Ela possui o método
// requestMove(Car car), que é a única forma de um carro interagir com o sistema de tráfego.
//      Padrão: Define a interface para a comunicação do mediador.

public interface TrafficMediator {
    void requestMove(Car car); // Objeto Car - Interação através da interface.
}
