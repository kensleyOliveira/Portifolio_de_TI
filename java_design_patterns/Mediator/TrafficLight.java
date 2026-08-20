package Mediator;

//TrafficLight (Colaborador/Colega): Esta classe (TrafficLight) representa um semáforo,
// um dos objetos que o mediador gerencia. Ele tem seu próprio estado (se está verde ou não)
// e não interage diretamente com os carros.
//              Padrão: Um dos objetos colaboradores que o mediador gerencia.
public class TrafficLight {
    private final String location;
    private boolean green;

    public TrafficLight(String location) {
        this.location = location;
        this.green = false;
    }

    public void setGreen(boolean green) {
        this.green = green;
        System.out.println("Semáforo em " + location + " agora está " + (green ? "VERDE" : "VERMELHO"));
    }

    public boolean isGreen() { return green; }
    public String getLocation() { return location; }
}

