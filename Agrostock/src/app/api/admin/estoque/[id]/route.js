import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function DELETE(request, { params }) {
  try {
    const { id } = await params;

    const [result] = await db.execute('DELETE FROM estoque_usuario WHERE id = ?', [id]);

    if (result.affectedRows === 0) {
      return NextResponse.json({ error: 'Item não encontrado' }, { status: 404 });
    }

    return NextResponse.json({ message: 'Item excluído com sucesso' });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
