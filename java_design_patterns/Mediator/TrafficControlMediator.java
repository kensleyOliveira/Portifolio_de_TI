package Mediator;

import Flyweight.Car;
import java.util.HashMap;
import java.util.Map;

//TrafficControlMediator (Mediador Concreto): Esta classe (TrafficControlMediator)
// implementa a interface TrafficMediator. Ela orquestra a comunicação entre os carros
// e os semáforos, mantendo uma lista de semáforos e decidindo se um carro pode prosseguir.
//          Padrão: O mediador concreto que encapsula a lógica de comunicação entre os
//          objetos.

public class TrafficControlMediator implements TrafficMediator {
    private final Map<String, TrafficLight> trafficLights = new HashMap<>();

    public void addTrafficLight(TrafficLight light) {
        trafficLights.put(light.getLocation(), light);
    }

    @Override
    public void requestMove(Car car) {
        TrafficLight light = trafficLights.get(car.getPosition()); //Chamada de um objeto - TrafficLight
        if (light != null && light.isGreen()) {
            car.go();
        } else {
            car.stop();
        }
    }
}
