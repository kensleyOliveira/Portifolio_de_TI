package Flyweight;

import java.util.HashMap;
import java.util.Map;

//CarFactory (Flyweight Factory): Esta é a fábrica responsável por gerenciar e criar
// os objetos Flyweight (CarModel). Ela garante que, para cada combinação de marca,
// modelo e cor, apenas uma única instância de CarModel seja criada e reutilizada.
// O método getCarModel() verifica se um CarModel com a combinação de atributos
//  solicitada já existe no Map. Se sim, ele o retorna; se não, ele cria um novo,
//  armazena-o no Map e o retorna.
public class CarFactory {
    private static final Map<String, CarModel> carModels = new HashMap<>();

    public static CarModel getCarModel(String brand, String model, String color) {
        String key = brand + "-" + model + "-" + color;
        if (!carModels.containsKey(key)) {
            carModels.put(key, new CarModel(brand, model, color));
        }
        return carModels.get(key);
    }
}
