import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function PATCH(request, { params }) {
  try {
    const { id } = await params;
    const { acao, estoque_id } = await request.json();

    if (acao === 'concluido') {
      await db.execute('DELETE FROM estoque_usuario WHERE id = ?', [estoque_id]);

      await db.execute('UPDATE solicitacoes_ajuste SET status = "concluido" WHERE id = ?', [id]);
    } else {
      await db.execute('UPDATE solicitacoes_ajuste SET status = "rejeitado" WHERE id = ?', [id]);
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
