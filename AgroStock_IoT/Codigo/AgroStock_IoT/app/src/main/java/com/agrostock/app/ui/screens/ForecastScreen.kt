package com.agrostock.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrostock.app.ui.viewmodel.DashboardState
import java.text.SimpleDateFormat
import java.util.Locale

@Composable
fun ForecastScreen(state: DashboardState) {
    val formatoEntrada = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    val formatoSaida = SimpleDateFormat("dd/MM (EEE)", Locale.getDefault())

    fun formatarDataPrevisao(dataStr: String): String {
        return try {
            val data = formatoEntrada.parse(dataStr)
            if (data != null) formatoSaida.format(data).uppercase() else dataStr
        } catch (e: Exception) {
            dataStr
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF4F6F9))
            .padding(16.dp)
    ) {
        Text(
            text = "Previsão Regional (15 dias)",
            fontSize = 22.sp,
            color = Color(0xFF1E1E1E),
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        LazyColumn(
            verticalArrangement = Arrangement.spacedBy(8.dp),
            modifier = Modifier.fillMaxSize()
        ) {
            items(state.forecast) { day ->
                Card(
                    shape = RoundedCornerShape(12.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier
                            .padding(16.dp)
                            .fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = formatarDataPrevisao(day.data),
                                color = Color(0xFF1E1E1E),
                                fontSize = 14.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(
                                text = "Chuva: ${day.chuvaProb}%",
                                color = if (day.chuvaProb > 50) Color(0xFF1976D2) else Color.Gray,
                                fontSize = 13.sp
                            )
                        }

                        Text(
                            text = "${String.format(Locale.US, "%.1f", day.tempMax)}°C / ${String.format(Locale.US, "%.1f", day.tempMin)}°C",
                            color = Color(0xFF1E1E1E),
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp
                        )
                    }
                }
            }
        }
    }
}