package com.agrostock.app.data.model

import kotlinx.serialization.Serializable

@Serializable
data class TelemetriaResponse(
    val success: Boolean,
    val data: List<Telemetria>
)

@Serializable
data class Telemetria(
    val id: Int? = null,
    val temperatura: Double? = null,
    val umidade: Double? = null,
    val timestamp: String
)

@Serializable
data class PrevisaoResponse(
    val success: Boolean,
    val data: PrevisaoData
)

@Serializable
data class PrevisaoData(
    val daily: PrevisaoDaily
)

@Serializable
data class PrevisaoDaily(
    val time: List<String>,
    val temperature_2m_min: List<String>,
    val temperature_2m_max: List<String>,
    val precipitation_probability_max: List<Int>
)

data class PrevisaoDiaUI(
    val data: String,
    val tempMin: Double,
    val tempMax: Double,
    val chuvaProb: Int
)