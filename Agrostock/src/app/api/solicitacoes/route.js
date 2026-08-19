import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function POST(request) {
  try {
    const { usuario_id, estoque_id, motivo } = await request.json();
    await db.execute(
      'INSERT INTO solicitacoes_ajuste (usuario_id, estoque_id, motivo) VALUES (?, ?, ?)',
      [usuario_id, estoque_id, motivo]
    );
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function GET() {
  try {
    const [rows] = await db.execute(`
      SELECT s.*, u.nome as produtor, p.nome as produto, e.quantidade
      FROM solicitacoes_ajuste s
      JOIN usuarios u ON s.usuario_id = u.id
      JOIN estoque_usuario e ON s.estoque_id = e.id
      JOIN produtos p ON e.produto_id = p.id
      WHERE s.status = 'pendente'
    `);
    return NextResponse.json(rows);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
