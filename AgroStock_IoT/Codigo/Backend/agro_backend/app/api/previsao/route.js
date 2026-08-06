import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Coordenadas de Monte Carmelo - MG (Latitude e Longitude)
    const latitude = -18.72;
    const longitude = -47.49;
    
    // URL da Open-Meteo configurada para buscar a previsão diária de 15 dias
    const urlOpenMeteo = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=America%2FSao_Paulo&forecast_days=15`;

    const response = await fetch(urlOpenMeteo, {
      next: { revalidate: 3600 } // Faz o cache da previsão por 1 hora para evitar requisições repetidas desnecessárias
    });

    if (!response.ok) {
      throw new Error(`Erro na integração com Open-Meteo: ${response.status}`);
    }

    const dataReal = await response.json();

    // Mapeamos a resposta da Open-Meteo exatamente no formato que o seu componente Page.jsx espera receber
    const dadosFormatados = {
      daily: {
        time: dataReal.daily.time, // Array de datas ["2026-07-24", "2026-07-25", ...]
        temperature_2m_max: dataReal.daily.temperature_2m_max.map(t => t.toFixed(1)),
        temperature_2m_min: dataReal.daily.temperature_2m_min.map(t => t.toFixed(1)),
        precipitation_probability_max: dataReal.daily.precipitation_probability_max
      }
    };

    return NextResponse.json({ success: true, data: dadosFormatados }, { status: 200 });
    
  } catch (error) {
    console.error("Erro na API de previsão meteorológica real:", error.message);
    return NextResponse.json({ success: false, message: 'Erro interno ao obter previsão real.' }, { status: 500 });
  }
}