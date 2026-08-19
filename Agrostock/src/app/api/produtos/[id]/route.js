import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function DELETE(request, { params }) {
  try {
    const { id } = await params;

    const [result] = await db.execute('DELETE FROM produtos WHERE id = ?', [id]);

    if (result.affectedRows === 0) {
      return NextResponse.json({ message: 'Produto não encontrado' }, { status: 404 });
    }

    return NextResponse.json({
      success: true,
      message: 'Produto removido do catálogo!',
    });
  } catch (error) {
    console.error('Erro ao deletar produto:', error.message);

    return NextResponse.json(
      {
        error:
          'Não foi possível excluir o produto. Verifique se ele está sendo usado em algum estoque.',
      },
      { status: 500 }
    );
  }
}
