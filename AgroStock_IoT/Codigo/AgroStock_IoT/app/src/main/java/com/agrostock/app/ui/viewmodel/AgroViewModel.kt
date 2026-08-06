package com.agrostock.app.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.agrostock.app.data.remote.AgroApiService
import com.agrostock.app.data.model.Telemetria
import com.agrostock.app.data.model.PrevisaoDiaUI
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

data class DashboardState(
    val telemetrias: List<Telemetria> = emptyList(),
    val tempValues: List<Double> = emptyList(),
    val humValues: List<Double> = emptyList(),
    val avgTemp: Double = 0.0,
    val avgHum: Double = 0.0,
    val latestTemp: Double = 0.0,
    val latestHum: Double = 0.0,
    val startDate: String = "",
    val endDate: String = "",
    val forecast: List<PrevisaoDiaUI> = emptyList(),
    val isLoading: Boolean = false
)

class AgroViewModel : ViewModel() {
    private val apiService = AgroApiService()
    private val formatoData = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())

    private val _state = MutableStateFlow(DashboardState())
    val state: StateFlow<DashboardState> = _state.asStateFlow()

    init {
        val calendar = Calendar.getInstance()
        val dataFim = formatoData.format(calendar.time)
        calendar.add(Calendar.DAY_OF_MONTH, -7)
        val dataInicio = formatoData.format(calendar.time)

        _state.value = _state.value.copy(startDate = dataInicio, endDate = dataFim)
        loadData()
    }

    fun updateDates(start: String, end: String) {
        _state.value = _state.value.copy(startDate = start, endDate = end)
        loadData()
    }

    fun loadData() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true)
            try {
                val dadosBrutos = apiService.fetchTelemetry(_state.value.startDate, _state.value.endDate)
                val forecastData = apiService.fetch15DayForecast()
                val temperaturas = dadosBrutos.mapNotNull { it.temperatura }
                val umidades = dadosBrutos.mapNotNull { it.umidade }
                val leituraRecente = dadosBrutos.firstOrNull()

                _state.value = _state.value.copy(
                    telemetrias = dadosBrutos,
                    tempValues = temperaturas.reversed(),
                    humValues = umidades.reversed(),
                    avgTemp = if (temperaturas.isNotEmpty()) temperaturas.average() else 0.0,
                    avgHum = if (umidades.isNotEmpty()) umidades.average() else 0.0,
                    latestTemp = leituraRecente?.temperatura ?: 0.0,
                    latestHum = leituraRecente?.umidade ?: 0.0,
                    forecast = forecastData,
                    isLoading = false
                )
            } catch (e: Exception) {
                _state.value = _state.value.copy(isLoading = false)
            }
        }
    }
}