import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function DELETE(request, { params }) {
  try {
    const resolvedParams = await params;
    const { id } = resolvedParams;

    const [result] = await db.execute('DELETE FROM usuarios WHERE id = ?', [id]);

    if (result.affectedRows === 0) {
      return NextResponse.json({ message: 'Usuário não encontrado' }, { status: 404 });
    }

    return NextResponse.json({
      success: true,
      message: 'Usuário removido com sucesso!',
    });
  } catch (error) {
    console.error('Erro ao deletar usuário:', error.message);
    return NextResponse.json({ error: 'Erro interno ao deletar usuário' }, { status: 500 });
  }
}

export async function PUT(request, { params }) {
  try {
    const { id } = await params;
    const data = await request.json();

    let query = `UPDATE usuarios SET nome=?, nome_fazenda=?, endereco_fazenda=?, telefone=?`;
    let values = [data.nome, data.nome_fazenda, data.endereco_fazenda, data.telefone];

    if (data.email) {
      query += `, email=?`;
      values.push(data.email);
    }

    if (data.senha && data.senha.length > 5) {
      const bcrypt = require('bcrypt');
      const hash = await bcrypt.hash(data.senha, 10);
      query += `, senha=?`;
      values.push(hash);
    }

    query += ` WHERE id=?`;
    values.push(id);

    await db.execute(query, values);
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function GET(request, { params }) {
  try {
    const { id } = await params;
    const [rows] = await db.execute(
      'SELECT id, nome, email, perfil, nome_fazenda, endereco_fazenda, telefone FROM usuarios WHERE id = ?',
      [id]
    );

    if (rows.length === 0) {
      return NextResponse.json({ error: 'Usuário não encontrado' }, { status: 404 });
    }

    return NextResponse.json(rows[0]);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
