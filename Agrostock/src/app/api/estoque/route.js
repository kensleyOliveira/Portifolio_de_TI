import { NextResponse } from 'next/server';
import db from '@/lib/db';

export async function PUT(request, { params }) {
  try {
    const { id } = params;
    const { quantidade, data_validade } = await request.json();

    const [result] = await db.execute(
      'UPDATE estoque_usuario SET quantidade = ?, data_validade = ? WHERE id = ?',
      [Number(quantidade), data_validade, id]
    );

    if (result.affectedRows === 0) {
      return NextResponse.json({ message: 'Item não encontrado' }, { status: 404 });
    }

    return NextResponse.json({ success: true, message: 'Estoque atualizado!' });
  } catch (error) {
    console.error('Erro na API PUT:', error.message);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const usuario_id = searchParams.get('usuario_id');

    const [rows] = await db.execute(
      `SELECT 
        estoque_id AS id, 
        produto_nome AS nome, 
        categoria,           -- <--- ADICIONE ESTA LINHA AQUI
        quantidade, 
        unidade, 
        status,
        motivo_rejeicao, 
        valor_calculado AS valor_estimado
      FROM v_estoque_detalhado 
      WHERE usuario_id = ? 
      ORDER BY estoque_id DESC`,
      [usuario_id]
    );

    return NextResponse.json(rows);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function POST(request) {
  try {
    const body = await request.json();

    const usuario_id = parseInt(body.usuario_id);
    const produto_id = parseInt(body.produto_id);
    const quantidade = parseFloat(body.quantidade);
    const data_validade = body.data_validade;

    console.log('Processando lançamento:', { usuario_id, produto_id, quantidade });

    const [result] = await db.execute(
      'INSERT INTO estoque_usuario (usuario_id, produto_id, quantidade, data_validade, status) VALUES (?, ?, ?, ?, ?)',
      [usuario_id, produto_id, quantidade, data_validade, 'pendente']
    );

    return NextResponse.json({ success: true, id: result.insertId });
  } catch (error) {
    console.error('Erro no MySQL AgroStock:', error.message);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
