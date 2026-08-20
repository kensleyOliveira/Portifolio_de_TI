package Flyweight;

import Mediator.TrafficMediator;

//Car (Colaborador/Colega): Embora não esteja completo no código fornecido, a classe
// Car seria a outra parte que interage com o mediador. Em vez de verificar o estado
// do semáforo diretamente, o carro delega essa responsabilidade ao TrafficControlMediator
// através do método requestMove.
//      Padrão: O outro objeto colaborador.
// Esta classe, também usa o Flyweight. Cada objeto Car armazena seu estado extrínseco
// (placa, posição, velocidade) e mantém uma referência a um objeto CarModel (o Flyweight)
// para obter o estado intrínseco.
public class Car {
    private final CarModel model; // Estado intrínseco (compartilhado)
    private final String plate;   // Estado extrínseco
    private String position; // Estado extrínseco
    private int speed; // Estado extrínseco

    public Car(CarModel model, String plate, String position, int speed) {
        this.model = model;
        this.plate = plate;
        this.position = position;
        this.speed = speed;
    }

    public void move(TrafficMediator mediator) {// Interface com mediator

        mediator.requestMove(this);
    }

    public void stop() {
        this.speed = 0;
        System.out.println("Carro " + plate + " PAROU no semáforo.");
    }

    public void go() {
        this.speed = 40; // Velocidade fixa só para exemplo
        System.out.println("Carro " + plate + " ESTÁ SEGUINDO.");
    }

    public void showStatus() {

        model.showInfo(plate, position, speed);
    }

    public String getPosition() {
        return position; }
    public String getPlate() {
        return plate; }
}