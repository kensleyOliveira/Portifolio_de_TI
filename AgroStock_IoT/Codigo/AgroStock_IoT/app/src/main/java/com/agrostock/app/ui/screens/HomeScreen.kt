package com.agrostock.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.WbCloudy
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.agrostock.app.ui.components.AgroSparkline
import com.agrostock.app.ui.viewmodel.DashboardState
import java.text.SimpleDateFormat
import java.util.Locale

@Composable
fun HomeScreen(state: DashboardState) {
    val formatoEntrada = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
    val formatoSaida = SimpleDateFormat("dd/MM (EEE)", Locale.getDefault())

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF4F6F9))
            .verticalScroll(rememberScrollState())
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF2E7D32))
                .padding(top = 40.dp, bottom = 24.dp, start = 20.dp, end = 20.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Eco, contentDescription = "Logo", tint = Color.White, modifier = Modifier.size(32.dp))
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Text("AgroStock Monitor", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                        Text("Monte Carmelo - MG", color = Color.White.copy(alpha = 0.8f), fontSize = 12.sp)
                    }
                }
                Row {
                    Icon(Icons.Default.Notifications, contentDescription = null, tint = Color.White)
                    Spacer(modifier = Modifier.width(16.dp))
                    Icon(Icons.Default.Settings, contentDescription = null, tint = Color.White)
                }
            }
        }

        Column(modifier = Modifier.padding(20.dp)) {
            Text("Dashboard", fontSize = 26.sp, fontWeight = FontWeight.ExtraBold, color = Color(0xFF1E1E1E), modifier = Modifier.padding(bottom = 16.dp))

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                Card(
                    modifier = Modifier.weight(1f).height(120.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                        Text("TEMPERATURA", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                        Text("${String.format(Locale.US, "%.1f", state.latestTemp)}°C", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E1E1E))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(modifier = Modifier.size(8.dp).clip(RoundedCornerShape(4.dp)).background(Color(0xFFFF5722)))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Microclima Atual", fontSize = 12.sp, color = Color.Gray)
                        }
                    }
                }

                Card(
                    modifier = Modifier.weight(1f).height(120.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp).fillMaxSize(), verticalArrangement = Arrangement.SpaceBetween) {
                        Text("UMIDADE RELATIVA", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                        Text("${String.format(Locale.US, "%.1f", state.latestHum)}%", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E1E1E))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(modifier = Modifier.size(8.dp).clip(RoundedCornerShape(4.dp)).background(Color(0xFF2196F3)))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Microclima Atual", fontSize = 12.sp, color = Color.Gray)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("TENDÊNCIA DA TEMPERATURA (7 DIAS)", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(16.dp))
                    if (state.isLoading) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally), color = Color(0xFF2E7D32))
                    } else {
                        Box(modifier = Modifier.fillMaxWidth().height(120.dp)) {
                            AgroSparkline(data = state.tempValues, lineColor = Color(0xFFFF5722))
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("CLIMA DO DIA (PREVISÃO)", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(12.dp))

                    val previsaoHoje = state.forecast.firstOrNull()

                    if (previsaoHoje != null) {
                        val dataFormatada = try {
                            val data = formatoEntrada.parse(previsaoHoje.data)
                            if (data != null) formatoSaida.format(data).uppercase() else previsaoHoje.data
                        } catch (e: Exception) { previsaoHoje.data }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.WbCloudy, contentDescription = null, tint = Color(0xFF2196F3), modifier = Modifier.size(36.dp))
                                Spacer(modifier = Modifier.width(12.dp))
                                Column {
                                    Text(dataFormatada, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1E1E1E))
                                    Text("Probabilidade de Chuva: ${previsaoHoje.chuvaProb}%", fontSize = 12.sp, color = if (previsaoHoje.chuvaProb > 50) Color(0xFF1976D2) else Color.Gray)
                                }
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("${String.format(Locale.US, "%.1f", previsaoHoje.tempMax)}°", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFFD32F2F))
                                Text("${String.format(Locale.US, "%.1f", previsaoHoje.tempMin)}°", fontSize = 16.sp, fontWeight = FontWeight.Medium, color = Color(0xFF1976D2))
                            }
                        }
                    } else if (state.isLoading) {
                        CircularProgressIndicator(modifier = Modifier.align(Alignment.CenterHorizontally), color = Color(0xFF2E7D32))
                    } else {
                        Text("Previsão não disponível", color = Color.Gray, fontSize = 14.sp)
                    }
                }
            }
        }
    }
}