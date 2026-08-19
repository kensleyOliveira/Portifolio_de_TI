import { NextResponse } from 'next/server';
import db from '@/lib/db';
import bcrypt from 'bcrypt';

export async function POST(request) {
  try {
    const body = await request.json();
    const { nome, email, senha, perfil, nome_fazenda, endereco_fazenda, telefone } = body;

    const [existente] = await db.execute('SELECT id FROM usuarios WHERE email = ?', [email]);
    if (existente.length > 0) {
      return NextResponse.json({ error: 'E-mail já cadastrado' }, { status: 400 });
    }

    const senhaHash = await bcrypt.hash(senha, 10);

    const [result] = await db.execute(
      `INSERT INTO usuarios 
      (nome, email, senha, perfil, nome_fazenda, endereco_fazenda, telefone) 
      VALUES (?, ?, ?, ?, ?, ?, ?)`,
      [
        nome || null,
        email || null,
        senhaHash || null,
        perfil || 'comum',
        nome_fazenda || null,
        endereco_fazenda || null,
        telefone || null,
      ]
    );

    return NextResponse.json({
      success: true,
      id: result.insertId,
      message: 'Cadastro realizado com sucesso!',
    });
  } catch (error) {
    console.error('Erro no Cadastro:', error.message);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
