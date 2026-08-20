package Flyweight;

// CarModel (Flyweight Concreto): Esta classe é o objeto Flyweight. Ela armazena
// o estado intrínseco e imutável (marca, modelo, cor) que pode ser compartilhado
// por vários objetos Car.
public class CarModel {

    // Estado Intrínseco (Intrinsic State): Dados que são compartilhados e
    // são independentes do contexto. São os dados que não mudam. No código, o
    // estado intrínseco é representado pela classe CarModel, que contém a marca,
    // modelo e cor de um carro. Esses atributos são os mesmos para todos os carros
    // do mesmo tipo.
    private final String brand;
    private final String model;
    private final String color;

    public CarModel(String brand, String model, String color) {
        this.brand = brand;
        this.model = model;
        this.color = color;
    }

    public void showInfo(String plate, String position, int speed) {
        System.out.println("Carro [" + brand + " " + model + ", " + color +
                "] - Placa: " + plate +
                " | Posição: " + position +
                " | Velocidade: " + speed + "km/h");
    }
}

