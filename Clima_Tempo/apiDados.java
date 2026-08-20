/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.javafx.system_weather_information;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author kensl
 */
public class apiDados {
    
    public String getDadosClimaticos(String cidade) {

        try {
            // ATENÇÃO: Este caminho relativo pode falhar dependendo de onde você executa.
            // É mais seguro usar um caminho absoluto ou colocar o 'api_key.txt'
            // na raiz do projeto e usar apenas Paths.get("api_key.txt")
            Path apiPath = Paths.get("api_key.txt");

            String apiKey = Files.readString(apiPath).trim();

            String formataNomeCidade = URLEncoder.encode(cidade, StandardCharsets.UTF_8);
            String apiUrl = "http://api.weatherapi.com/v1/current.json?key=" + apiKey + "&q=" + formataNomeCidade;
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(apiUrl))
                    .build();

            HttpClient client = HttpClient.newHttpClient();
            HttpResponse<String> response;

            response = client.send(request, HttpResponse.BodyHandlers.ofString());
            return response.body(); // Retorna os dados metereológicos (em formato JSON)

        } catch (IOException ex) {
            Logger.getLogger(apiDados.class.getName()).log(Level.SEVERE, null, ex);
            // # MUDANÇA 2: Adicionado 'return null' para indicar falha
            return null; 
        } catch (InterruptedException ex) {
            Logger.getLogger(apiDados.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }
}
    

