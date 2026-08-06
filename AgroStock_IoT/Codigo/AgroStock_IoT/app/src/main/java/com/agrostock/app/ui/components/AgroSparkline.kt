package com.agrostock.app.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.ExperimentalTextApi
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.util.Locale

@OptIn(ExperimentalTextApi::class)
@Composable
fun AgroSparkline(
    data: List<Double>,
    lineColor: Color,
    modifier: Modifier = Modifier
) {
    val textMeasurer = rememberTextMeasurer()
    val labelStyle = TextStyle(
        color = Color(0xFF757575),
        fontSize = 9.sp
    )

    Canvas(modifier = modifier.fillMaxSize()) {
        val width = size.width
        val height = size.height
        val maxVal = if (data.isNotEmpty()) data.maxOrNull() ?: 0.0 else 0.0
        val minVal = if (data.isNotEmpty()) data.minOrNull() ?: 0.0 else 0.0
        val avgVal = if (data.isNotEmpty()) data.average() else 0.0

        val delta = if (maxVal == minVal) 1.0 else (maxVal - minVal)

        val dashEffect = PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
        val gridColor = Color(0xFFE0E0E0)

        val paddingBottom = 10f
        val usableHeight = height - paddingBottom

        val yMax = usableHeight - ((maxVal - minVal) / delta * (usableHeight * 0.7f)).toFloat() - (usableHeight * 0.1f).toFloat()
        val yMin = usableHeight - ((minVal - minVal) / delta * (usableHeight * 0.7f)).toFloat() - (usableHeight * 0.1f).toFloat()
        val yAvg = usableHeight - ((avgVal - minVal) / delta * (usableHeight * 0.7f)).toFloat() - (usableHeight * 0.1f).toFloat()

        drawLine(color = gridColor, start = Offset(0f, yMax), end = Offset(width, yMax), strokeWidth = 1.dp.toPx(), pathEffect = dashEffect)
        drawText(textMeasurer = textMeasurer, text = String.format(Locale.US, "Máx: %.1f", maxVal), style = labelStyle, topLeft = Offset(8f, yMax - 30f))

        if (maxVal != minVal || data.isEmpty()) {
            drawLine(color = gridColor.copy(alpha = 0.5f), start = Offset(0f, yAvg), end = Offset(width, yAvg), strokeWidth = 1.dp.toPx(), pathEffect = dashEffect)
            drawText(textMeasurer = textMeasurer, text = String.format(Locale.US, "Média: %.1f", avgVal), style = labelStyle.copy(color = lineColor), topLeft = Offset(width - 140f, yAvg - 30f))
        }

        drawLine(color = gridColor, start = Offset(0f, yMin), end = Offset(width, yMin), strokeWidth = 1.dp.toPx(), pathEffect = dashEffect)
        drawText(textMeasurer = textMeasurer, text = String.format(Locale.US, "Mín: %.1f", minVal), style = labelStyle, topLeft = Offset(8f, yMin - 5f))

        if (data.size >= 2) {
            val divisoes = 4
            val step = (data.size - 1) / divisoes.coerceAtLeast(1)

            for (i in 0..divisoes) {
                val indexData = (i * step).coerceAtMost(data.size - 1)
                val x = indexData * (width / (data.size - 1))
                drawLine(color = gridColor, start = Offset(x, yMax), end = Offset(x, usableHeight), strokeWidth = 1.dp.toPx(), pathEffect = dashEffect)
            }

            val points = data.mapIndexed { index, value ->
                val x = index * (width / (data.size - 1))
                val y = usableHeight - ((value - minVal) / delta * (usableHeight * 0.7f)).toFloat() - (usableHeight * 0.1f).toFloat()
                Offset(x, y)
            }

            val strokePath = Path()
            val fillPath = Path()

            strokePath.moveTo(points[0].x, points[0].y)
            fillPath.moveTo(points[0].x, points[0].y)

            for (i in 0 until points.size - 1) {
                val p1 = points[i]
                val p2 = points[i + 1]
                val conX1 = (p1.x + p2.x) / 2
                strokePath.cubicTo(conX1, p1.y, conX1, p2.y, p2.x, p2.y)
                fillPath.cubicTo(conX1, p1.y, conX1, p2.y, p2.x, p2.y)
            }

            fillPath.lineTo(width, usableHeight)
            fillPath.lineTo(0f, usableHeight)
            fillPath.close()

            drawPath(path = fillPath, brush = Brush.verticalGradient(colors = listOf(lineColor.copy(alpha = 0.25f), Color.Transparent), startY = points.map { it.y }.minOrNull() ?: 0f, endY = usableHeight))
            drawPath(path = strokePath, color = lineColor, style = Stroke(width = 3.dp.toPx()))
        }
    }
}