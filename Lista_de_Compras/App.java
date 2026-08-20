package com.javafx.listadecompras;

import java.io.File;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;

/**
 * JavaFX App
 */
public class App extends Application {

    private static Scene scene;
    private ArrayList<String> listaDeCompras = new ArrayList<>();
    private ListView<String> listaVisualizavel = new ListView<>();

    @Override
    public void start(Stage stage) throws IOException {
        
        stage.setTitle("Aplicativo de Lista de Compras");
        
        TextField textFieldDescricaoItem = new TextField();
        Button botaoAdicionar = new Button("Adicionar");
        Button botaoExportar = new Button("Exportar Lista");
        
        Label labelAdicionar = new Label("Digite o item que deseja adicionar:");
        Label labelListaDeCompras = new Label("Lista de Compra");
        
        // Criação do objeto ObservableList a partir da listaDeCompras.
        ObservableList<String> observableListDeCompras = FXCollections.observableArrayList(listaDeCompras);
        listaVisualizavel.setItems(observableListDeCompras);
        
        VBox vBox = new VBox();
        vBox.getChildren().addAll(labelAdicionar, textFieldDescricaoItem, botaoAdicionar);
        vBox.getChildren().addAll(labelListaDeCompras, listaVisualizavel, botaoExportar);
        vBox.setSpacing(10);
        vBox.setPadding(new Insets(10));
        
        botaoAdicionar.setOnAction(e -> {
            String item = textFieldDescricaoItem.getText();
            if (!item.isEmpty()){
                listaDeCompras.add(item);
                listaVisualizavel.getItems().add(item);
                textFieldDescricaoItem.clear();
            }
        });
        
        botaoExportar.setOnAction(e -> {
            try {
                File arquivo = new File("listaDeCompras.txt");
                PrintWriter writer = new PrintWriter(arquivo);
                for (String item : listaDeCompras) {
                    writer.println(item);
                }
                writer.close();

                // ✅ Exibe mensagem de sucesso
                Alert alerta = new Alert(Alert.AlertType.INFORMATION);
                alerta.setTitle("Exportação Concluída");
                alerta.setHeaderText(null);
                alerta.setContentText("A lista foi exportada com sucesso para o arquivo 'listaDeCompras.txt'.");
                alerta.showAndWait();

            } catch (Exception ex) {
                // ❌ Exibe mensagem de erro, se algo der errado
                Alert erro = new Alert(Alert.AlertType.ERROR);
                erro.setTitle("Erro");
                erro.setHeaderText("Erro ao exportar a lista");
                erro.setContentText("Detalhes: " + ex.getMessage());
                erro.showAndWait();
            }
        });
        
        scene = new Scene(vBox, 350, 300);
        stage.setScene(scene);
        stage.show();
    }

    static void setRoot(String fxml) throws IOException {
        scene.setRoot(loadFXML(fxml));
    }

    private static Parent loadFXML(String fxml) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(App.class.getResource(fxml + ".fxml"));
        return fxmlLoader.load();
    }

    public static void main(String[] args) {
        launch(args);
    }

}