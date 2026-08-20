import Flyweight.Car;
import Flyweight.CarFactory;
import Mediator.TrafficControlMediator;
import Mediator.TrafficLight;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        // Criar Mediator
        TrafficControlMediator mediator = new TrafficControlMediator();

        // Criar Semáforos
        TrafficLight tl1 = new TrafficLight("Av. Paulista e Rua A");
        TrafficLight tl2 = new TrafficLight("Av. Brasil e Rua B");
        mediator.addTrafficLight(tl1);
        mediator.addTrafficLight(tl2);

        // Criar Carros (Flyweight em ação)
        Car car1 = new Car(CarFactory.getCarModel("Toyota", "Corolla", "Preto"), "ABC-1234", "Av. Paulista e Rua A", 0);
        Car car2 = new Car(CarFactory.getCarModel("Toyota", "Corolla", "Preto"), "XYZ-9876", "Av. Brasil e Rua B", 0);
        Car car3 = new Car(CarFactory.getCarModel("Honda", "Civic", "Branco"), "LMN-4567", "Av. Paulista e Rua A", 0);

        // Mostrar status inicial
        System.out.println("\n--- STATUS INICIAL ---");
        car1.showStatus();
        car2.showStatus();
        car3.showStatus();

        // Abrir sinal na Av. Paulista
        System.out.println("\n--- SEMÁFOROS ---");
        tl1.setGreen(true);
        tl2.setGreen(false);

        // Carros tentam se mover
        System.out.println("\n--- MOVIMENTAÇÃO ---");
        car1.move(mediator);
        car2.move(mediator);
        car3.move(mediator);
    }
}