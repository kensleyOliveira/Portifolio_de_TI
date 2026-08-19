import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function PATCH(request, { params }) {
  try {
    const resolvedParams = await params;
    const id = resolvedParams.id;

    const body = await request.json();
    const { status, motivo_rejeicao } = body;

    console.log(`Atualizando ID: ${id} | Status: ${status} | Motivo: ${motivo_rejeicao}`);

    const sqlParams = [status || null, motivo_rejeicao || null, id || null];

    const [result] = await db.execute(
      'UPDATE estoque_usuario SET status = ?, motivo_rejeicao = ? WHERE id = ?',
      sqlParams
    );

    if (result.affectedRows === 0) {
      return NextResponse.json({ error: 'Item não encontrado' }, { status: 404 });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Erro detalhado na API:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
