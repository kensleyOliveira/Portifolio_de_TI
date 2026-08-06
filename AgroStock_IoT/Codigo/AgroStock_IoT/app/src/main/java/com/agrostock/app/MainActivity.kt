package com.agrostock.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.ShowChart
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.*
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.agrostock.app.ui.screens.ForecastScreen
import com.agrostock.app.ui.screens.GraphicsScreen
import com.agrostock.app.ui.screens.HomeScreen
import com.agrostock.app.ui.viewmodel.AgroViewModel
import kotlinx.serialization.Serializable


@Serializable object Home
@Serializable object Graphics
@Serializable object Forecast

class MainActivity : ComponentActivity() {

    private val viewModel: AgroViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme(
                colorScheme = lightColorScheme(
                    primary = Color(0xFF2E7D32),
                    background = Color(0xFFF4F6F9),
                    surface = Color.White
                )
            ) {
                val navController = rememberNavController()
                val uiState by viewModel.state.collectAsState()
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentDestination = navBackStackEntry?.destination

                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    bottomBar = {
                        NavigationBar(
                            containerColor = Color.White,
                            tonalElevation = 8.dp
                        ) {
                            NavigationBarItem(
                                selected = currentDestination?.hasRoute<Home>() == true,
                                onClick = {
                                    navController.navigate(Home) {
                                        popUpTo(navController.graph.findStartDestination().id) {
                                            saveState = true
                                        }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                },
                                icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                                label = { Text("Home") },
                                colors = NavigationBarItemDefaults.colors(
                                    selectedIconColor = Color(0xFF2E7D32),
                                    selectedTextColor = Color(0xFF2E7D32),
                                    unselectedIconColor = Color.Gray,
                                    unselectedTextColor = Color.Gray,
                                    indicatorColor = Color(0xFFE8F5E9)
                                )
                            )

                            NavigationBarItem(
                                selected = currentDestination?.hasRoute<Graphics>() == true,
                                onClick = {
                                    navController.navigate(Graphics) {
                                        popUpTo(navController.graph.findStartDestination().id) {
                                            saveState = true
                                        }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                },
                                icon = { Icon(Icons.Default.ShowChart, contentDescription = "Gráficos") },
                                label = { Text("Monitoramento") },
                                colors = NavigationBarItemDefaults.colors(
                                    selectedIconColor = Color(0xFF2E7D32),
                                    selectedTextColor = Color(0xFF2E7D32),
                                    unselectedIconColor = Color.Gray,
                                    unselectedTextColor = Color.Gray,
                                    indicatorColor = Color(0xFFE8F5E9)
                                )
                            )

                            NavigationBarItem(
                                selected = currentDestination?.hasRoute<Forecast>() == true,
                                onClick = {
                                    navController.navigate(Forecast) {
                                        popUpTo(navController.graph.findStartDestination().id) {
                                            saveState = true
                                        }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                },
                                icon = { Icon(Icons.Default.WbSunny, contentDescription = "Previsão") },
                                label = { Text("Previsão") },
                                colors = NavigationBarItemDefaults.colors(
                                    selectedIconColor = Color(0xFF2E7D32),
                                    selectedTextColor = Color(0xFF2E7D32),
                                    unselectedIconColor = Color.Gray,
                                    unselectedTextColor = Color.Gray,
                                    indicatorColor = Color(0xFFE8F5E9)
                                )
                            )
                        }
                    }
                ) { innerPadding ->
                    NavHost(
                        navController = navController,
                        startDestination = Home,
                        modifier = Modifier.padding(innerPadding)
                    ) {
                        composable<Home> {
                            HomeScreen(state = uiState)
                        }

                        composable<Graphics> {
                            GraphicsScreen(
                                state = uiState,
                                onDateFilter = { start, end -> viewModel.updateDates(start, end) }
                            )
                        }

                        composable<Forecast> {
                            ForecastScreen(state = uiState)
                        }
                    }
                }
            }
        }
    }
}