import { NextResponse } from 'next/server';
import db from '@/lib/db';
import bcrypt from 'bcrypt';

export async function POST(request) {
  try {
    const { email, senha } = await request.json();

    const [rows] = await db.execute(
      `SELECT 
        id, 
        nome, 
        email, 
        senha, 
        perfil, 
        nome_fazenda, 
        endereco_fazenda, 
        telefone 
       FROM usuarios WHERE email = ?`,
      [email]
    );

    if (rows.length > 0) {
      const usuario = rows[0];

      const senhaCorreta = await bcrypt.compare(senha, usuario.senha);

      if (senhaCorreta) {
        return NextResponse.json({
          success: true,
          usuario: {
            id: usuario.id,
            nome: usuario.nome,
            email: usuario.email,
            perfil: usuario.perfil,
            nome_fazenda: usuario.nome_fazenda,
            endereco_fazenda: usuario.endereco_fazenda,
            telefone: usuario.telefone,
          },
        });
      }
    }

    return NextResponse.json(
      { success: false, message: 'E-mail ou senha inválidos' },
      { status: 401 }
    );
  } catch (error) {
    console.error('Erro interno no Login:', error.message);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
