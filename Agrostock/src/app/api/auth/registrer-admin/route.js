import { NextResponse } from 'next/server';
import db from '@/lib/db';
import bcrypt from 'bcrypt';

export async function POST(request) {
  try {
    const { nome, email, senha, token } = await request.json();

    const serverToken = process.env.ADMIN_AUTH_TOKEN;

    if (!token || token !== serverToken) {
      return NextResponse.json(
        { error: 'Código Autenticador inválido. Acesso negado.' },
        { status: 403 }
      );
    }

    const [userExists] = await db.execute('SELECT id FROM usuarios WHERE email = ?', [email]);
    if (userExists.length > 0) {
      return NextResponse.json({ error: 'E-mail já cadastrado.' }, { status: 400 });
    }

    const hashedSenha = await bcrypt.hash(senha, 10);

    await db.execute('INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)', [
      nome,
      email,
      hashedSenha,
      'admin',
    ]);

    return NextResponse.json({ success: true, message: 'Gestor cadastrado com sucesso!' });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
