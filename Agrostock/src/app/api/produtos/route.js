import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function GET() {
  try {
    const [rows] = await db.execute(
      'SELECT id, nome, categoria, preco_base, unidade FROM produtos'
    );
    return NextResponse.json(rows);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function POST(request) {
  try {
    const { nome, categoria, preco_base, unidade } = await request.json();
    const [result] = await db.execute(
      'INSERT INTO produtos (nome, categoria, preco_base, unidade) VALUES (?, ?, ?, ?)',
      [nome, categoria, preco_base || 0, unidade]
    );
    return NextResponse.json({ id: result.insertId, success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function DELETE(request, { params }) {
  try {
    const { id } = params;
    await db.execute('DELETE FROM produtos WHERE id = ?', [id]);
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
