import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function PATCH(request, { params }) {
  try {
    const { id } = await params;
    const { status } = await request.json();

    const [result] = await db.execute('UPDATE estoque_usuario SET status = ? WHERE id = ?', [
      status,
      id,
    ]);

    if (result.affectedRows === 0) {
      return NextResponse.json({ error: 'Item não encontrado' }, { status: 404 });
    }

    return NextResponse.json({ success: true, message: `Status atualizado para ${status}` });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
