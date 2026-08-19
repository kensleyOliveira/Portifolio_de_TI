import { NextResponse } from 'next/server';
import db from '@/lib/db';

export const dynamic = 'force-dynamic';

export async function GET(request, { params }) {
  try {
    const { id } = await params;

    console.log('📡 Buscando dados reais para o ID:', id);

    const [rows] = await db.execute(
      `SELECT 
        estoque_id AS id, 
        produto_nome AS insumo, 
        quantidade, 
        unidade, 
        status, 
        valor_calculado AS valor_estimado, -- Mapeia para o nome que o Frontend usa
        data_validade
      FROM v_estoque_detalhado
      WHERE usuario_id = ?
      ORDER BY status ASC, estoque_id DESC`,
      [id]
    );

    const responseData = rows || [];

    return NextResponse.json(responseData, {
      headers: {
        'Cache-Control': 'no-store, max-age=0',
      },
    });
  } catch (error) {
    console.error('❌ Erro na API:', error.message);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
