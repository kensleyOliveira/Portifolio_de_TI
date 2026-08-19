import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function GET() {
  try {
    const [rows] = await db.execute(`
      SELECT 
        e.id, 
        e.quantidade, 
        COALESCE(e.valor_estimado, e.quantidade * p.preco_base) as valor_estimado, 
        e.status, 
        u.nome as produtor, 
        p.nome as insumo_nome,
        p.unidade
      FROM estoque_usuario e
      JOIN usuarios u ON e.usuario_id = u.id
      JOIN produtos p ON e.produto_id = p.id
      WHERE e.status = 'pendente'
    `);

    return NextResponse.json(rows || []);
  } catch (error) {
    console.error('Erro na API de Pendentes:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
