package com.agrostock.app.ui.screens

import android.app.DatePickerDialog
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.Thermostat
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrostock.app.ui.components.AgroSparkline
import com.agrostock.app.ui.viewmodel.DashboardState
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun GraphicsScreen(
    state: DashboardState,
    onDateFilter: (String, String) -> Unit
) {
    val context = LocalContext.current
    val calendar = Calendar.getInstance()
    val formatoBanco = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    val formatoExibicao = SimpleDateFormat("dd/MM", Locale.getDefault())

    fun formatarParaExibicao(dataStr: String): String {
        return try {
            val data = formatoBanco.parse(dataStr)
            if (data != null) formatoExibicao.format(data) else dataStr
        } catch (e: Exception) { dataStr }
    }

    val datePickerInicio = DatePickerDialog(
        context,
        { _, year, month, dayOfMonth ->
            val dataFormatada = String.format("%04d-%02d-%02d", year, month + 1, dayOfMonth)
            onDateFilter(dataFormatada, state.endDate)
        },
        calendar.get(Calendar.YEAR),
        calendar.get(Calendar.MONTH),
        calendar.get(Calendar.DAY_OF_MONTH)
    )

    val datePickerFim = DatePickerDialog(
        context,
        { _, year, month, dayOfMonth ->
            val dataFormatada = String.format("%04d-%02d-%02d", year, month + 1, dayOfMonth)
            onDateFilter(state.startDate, dataFormatada)
        },
        calendar.get(Calendar.YEAR),
        calendar.get(Calendar.MONTH),
        calendar.get(Calendar.DAY_OF_MONTH)
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF4F6F9)) // Fundo Claro
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            shape = RoundedCornerShape(16.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Row(
                modifier = Modifier
                    .padding(16.dp)
                    .fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("DATA INICIAL", fontSize = 11.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                    OutlinedButton(
                        onClick = { datePickerInicio.show() },
                        modifier = Modifier.fillMaxWidth().padding(end = 4.dp),
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF1E1E1E))
                    ) {
                        Icon(Icons.Default.DateRange, contentDescription = null, Modifier.size(16.dp), tint = Color.Gray)
                        Spacer(Modifier.width(8.dp))
                        Text(formatarParaExibicao(state.startDate), fontSize = 13.sp)
                    }
                }

                Column(modifier = Modifier.weight(1f)) {
                    Text("DATA FINAL", fontSize = 11.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                    OutlinedButton(
                        onClick = { datePickerFim.show() },
                        modifier = Modifier.fillMaxWidth().padding(start = 4.dp),
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF1E1E1E))
                    ) {
                        Icon(Icons.Default.DateRange, contentDescription = null, Modifier.size(16.dp), tint = Color.Gray)
                        Spacer(Modifier.width(8.dp))
                        Text(formatarParaExibicao(state.endDate), fontSize = 13.sp)
                    }
                }
            }
        }

        Text(
            text = "Período de ${formatarParaExibicao(state.startDate)} a ${formatarParaExibicao(state.endDate)}",
            color = Color(0xFF1E1E1E),
            fontWeight = FontWeight.Bold,
            fontSize = 15.sp,
            modifier = Modifier.padding(bottom = 24.dp)
        )

        if (state.isLoading) {
            Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(color = Color(0xFF2E7D32))
            }
        } else {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                Box(modifier = Modifier.weight(1f)) {
                    TelemetryCard(
                        value = String.format(Locale.US, "%.1f", state.avgTemp),
                        unit = "°C",
                        icon = Icons.Default.Thermostat,
                        lineColor = Color(0xFFFF5722),
                        data = state.tempValues,
                        startDateFormatted = formatarParaExibicao(state.startDate),
                        endDateFormatted = formatarParaExibicao(state.endDate)
                    )
                }

                Box(modifier = Modifier.weight(1f)) {
                    TelemetryCard(
                        value = String.format(Locale.US, "%.1f", state.avgHum),
                        unit = "%",
                        icon = Icons.Default.WaterDrop,
                        lineColor = Color(0xFF2196F3),
                        data = state.humValues,
                        startDateFormatted = formatarParaExibicao(state.startDate),
                        endDateFormatted = formatarParaExibicao(state.endDate)
                    )
                }
            }
        }
    }
}

@Composable
fun TelemetryCard(
    value: String, unit: String, icon: androidx.compose.ui.graphics.vector.ImageVector,
    lineColor: Color, data: List<Double>, startDateFormatted: String, endDateFormatted: String
) {
    Card(
        shape = RoundedCornerShape(32.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 3.dp),
        modifier = Modifier.fillMaxWidth().height(240.dp)
    ) {
        Box(modifier = Modifier.fillMaxSize()) {
            Icon(
                imageVector = icon, contentDescription = null,
                tint = Color.Gray.copy(alpha = 0.3f),
                modifier = Modifier.size(44.dp).align(Alignment.TopEnd).padding(top = 16.dp, end = 16.dp)
            )

            Column(modifier = Modifier.padding(start = 20.dp, top = 36.dp)) {
                Row(verticalAlignment = Alignment.Bottom) {
                    Text(text = value, fontSize = 48.sp, color = Color(0xFF1E1E1E), fontWeight = FontWeight.Light)
                    Text(text = unit, fontSize = 18.sp, color = Color(0xFF1E1E1E), modifier = Modifier.padding(bottom = 8.dp, start = 2.dp))
                }
            }

            Box(modifier = Modifier.fillMaxWidth().height(85.dp).align(Alignment.Center).padding(top = 28.dp)) {
                AgroSparkline(data = data, lineColor = lineColor)
            }

            Row(
                modifier = Modifier.fillMaxWidth().align(Alignment.BottomCenter).padding(start = 20.dp, end = 20.dp, bottom = 12.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(text = startDateFormatted, fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Medium)
                Text(text = endDateFormatted, fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Medium)
            }
        }
    }
}