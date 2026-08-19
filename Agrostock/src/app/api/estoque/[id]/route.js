import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function GET(request, { params }) {
  try {
    const resolvedParams = await params;
    const id = resolvedParams.id;

    const [rows] = await db.execute(
      `SELECT e.id, e.quantidade, e.data_validade, p.nome 
       FROM estoque_usuario e 
       JOIN produtos p ON e.produto_id = p.id 
       WHERE e.id = ?`,
      [id]
    );

    if (rows.length === 0) {
      return NextResponse.json({ error: 'Insumo não encontrado' }, { status: 404 });
    }

    return NextResponse.json(rows[0]);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function DELETE(request, { params }) {
  try {
    const resolvedParams = await params;
    const id = resolvedParams.id;

    const [result] = await db.execute('DELETE FROM estoque_usuario WHERE id = ?', [id]);

    if (result.affectedRows === 0) {
      return NextResponse.json({ message: 'Item não encontrado' }, { status: 404 });
    }

    return NextResponse.json({ success: true, message: 'Item removido!' });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function PUT(request, { params }) {
  try {
    const resolvedParams = await params;
    const id = resolvedParams.id;

    const { quantidade, data_validade } = await request.json();

    const [result] = await db.execute(
      'UPDATE estoque_usuario SET quantidade = ?, data_validade = ? WHERE id = ?',
      [quantidade, data_validade, id]
    );

    return NextResponse.json({ success: true, message: 'Atualizado com sucesso!' });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
