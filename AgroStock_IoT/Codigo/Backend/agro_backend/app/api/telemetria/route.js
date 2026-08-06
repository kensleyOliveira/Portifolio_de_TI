import { NextResponse } from 'next/server';
import pool from '@/lib/db';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const dataInicio = searchParams.get('inicio');
  const dataFim = searchParams.get('fim');

  try {
    let query = `
      SELECT 
        id, 
        temperatura, 
        h AS umidade, 
        data_hora AS timestamp 
      FROM telemetria_microclima
    `;
    const queryParams = [];

    // Lógica de filtro por data
    if (dataInicio && dataFim) {
      query += ' WHERE data_hora >= ? AND data_hora <= ?';
      // Garante que a busca cubra do primeiro segundo do dia de início até o último segundo do dia de fim
      queryParams.push(`${dataInicio} 00:00:00`, `${dataFim} 23:59:59`);
    }

    query += ' ORDER BY data_hora DESC LIMIT 10000';

    // Executa a query no MySQL
    const [rows] = await pool.execute(query, queryParams);

    return NextResponse.json({ success: true, data: rows }, { status: 200 });
    
  } catch (error) {
    console.error("Erro ao buscar dados do MySQL:", error);
    return NextResponse.json({ success: false, message: 'Erro interno na API.' }, { status: 500 });
  }
}