import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function GET() {
  try {
    const [rows] = await db.execute(`
      SELECT 
        u.id, 
        u.nome, 
        u.nome_fazenda, 
        u.email,
        COALESCE((
          SELECT SUM(valor_calculado) 
          FROM v_estoque_detalhado 
          WHERE usuario_id = u.id AND status = 'aprovado'
        ), 0) as patrimonio_total
      FROM usuarios u
      WHERE u.perfil != 'admin'
    `);

    return NextResponse.json(rows);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
