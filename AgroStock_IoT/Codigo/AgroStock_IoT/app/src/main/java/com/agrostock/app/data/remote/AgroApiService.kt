package com.agrostock.app.data.remote

import com.agrostock.app.data.model.PrevisaoDiaUI
import com.agrostock.app.data.model.PrevisaoResponse
import com.agrostock.app.data.model.Telemetria
import com.agrostock.app.data.model.TelemetriaResponse
import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.defaultRequest
import io.ktor.client.request.get
import io.ktor.http.URLProtocol
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

object KtorClient {
    private const val HOST_URL = "splendid-empathy-production-efed.up.railway.app"

    val httpClient = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true
            })
        }
        defaultRequest {
            url {
                protocol = URLProtocol.HTTPS
                host = HOST_URL
            }
        }
    }
}

class AgroApiService {

    suspend fun fetchTelemetry(inicio: String, fim: String): List<Telemetria> {
        val url = "/api/telemetria?inicio=$inicio&fim=$fim"
        val response: TelemetriaResponse = KtorClient.httpClient.get(url).body()
        return response.data
    }

    suspend fun fetch15DayForecast(): List<PrevisaoDiaUI> {
        val response: PrevisaoResponse = KtorClient.httpClient.get("/api/previsao").body()

        return response.data.daily.time.mapIndexed { index, dataTexto ->
            PrevisaoDiaUI(
                data = dataTexto,
                tempMin = response.data.daily.temperature_2m_min[index].toDouble(),
                tempMax = response.data.daily.temperature_2m_max[index].toDouble(),
                chuvaProb = response.data.daily.precipitation_probability_max[index]
            )
        }
    }
}