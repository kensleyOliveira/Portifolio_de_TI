/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.javafx.system_weather_information;

import java.io.IOException;
import org.json.JSONObject;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;



/**
 *
 * @author kensl
 */
public class System_Weather_Information {

    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        System.out.println("Digite o nome da cidade: ");
        String cidade = scanner.nextLine(); // Lê a cidade do teclado
        
        try {
            String dadosClimaticos = getDadosClimaticos(cidade); // Retorna um JSON
            
            // Código 1006 siginifica localização não é encontrada
            if (dadosClimaticos.contains("\"code\":1006")) { // \"code\":1006 representa "code":1006 no JSO
                System.out.println("Localizacao nao encontrada. Por favor, tente novamente.");               
            } else {
                imprimirDadosClimaticos(dadosClimaticos);
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private static String getDadosClimaticos(String cidade) throws Exception {
         Path apiPath = Paths.get("..", "SWI", "api_key.txt");
         
         String apiKey = Files.readString(apiPath).trim();
                  
         String formataNomeCidade = URLEncoder.encode(cidade, StandardCharsets.UTF_8);
         String apiUrl = "http://api.weatherapi.com/v1/current.json?key=" + apiKey + "&q=" + formataNomeCidade;
         HttpRequest request = HttpRequest.newBuilder() // Começa a construção de uma nova solicitação HTTP
                 .uri(URI.create(apiUrl)) // Este método define o URU da solicitação HTTP
                 .build(); // Finaliza a construção da solicitação HTTP
         
         // Criar objeto envia solictações HTTP e receber respostas HTTP, para acessar o site WeatherAPI
         HttpClient client = HttpClient.newHttpClient();
         
         // Agora vamos enviar requisições HTTP e receber respostas HTTP, comunicar com site da API Meteorologia.
         HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
         
         return response.body(); // Retorna os dados metereológicos obtidos no site da API (WeatherAPI)
    }
    
    // Métdo para imprimir os dados metereológicos de forma organizada
    public static void imprimirDadosClimaticos(String dados){
        
        //System.out.println("Dados originais (JSON) obtidos no site meteorológico" + dados);
        
        JSONObject dadosJson = new JSONObject(dados);
        JSONObject informacoesMeteorolicas = dadosJson.getJSONObject("current");
        
        // Extrai os dados da localização
        String cidade = dadosJson.getJSONObject("location").getString("name");
        String pais = dadosJson.getJSONObject("location").getString("country");
        
        // Extrai os dados adicionais
        String condicaoTempo = informacoesMeteorolicas.getJSONObject("condition").getString("text");
        int umidade = informacoesMeteorolicas.getInt("humidity");
        float velocidadeVento = informacoesMeteorolicas.getFloat("wind_kph");
        float pressaoAtmosferica = informacoesMeteorolicas.getFloat("pressure_mb");
        float sensacaoTermica = informacoesMeteorolicas.getFloat("feelslike_c");
        float temperaturaAtual = informacoesMeteorolicas.getFloat("temp_c");
        
        
        // Extrai a data e hora da string retornada pela API
        String dataHoraString = informacoesMeteorolicas.getString("last_updated");
        
        // Imprime as informações atuais
        System.out.println("Informacoes Meteorologicas para " + cidade + "," + pais);
        System.out.println("Data e Hora: " + dataHoraString);
        System.out.println("Temperatura Atual: " + temperaturaAtual + "oC");
        System.out.println("Sensacao Termica: " + sensacaoTermica + "oC");
        System.out.println("Condicao do Tempo: " + condicaoTempo);
        System.out.println("Umidade: " + umidade + "%");
        System.out.println("Velocidade do Vento: " + velocidadeVento + " km/h");
        System.out.println("Pressao Atmosferica: " + pressaoAtmosferica + " mb");   
    }
}
