import { NextResponse } from 'next/server';
import db from '@/lib/db';
import bcrypt from 'bcrypt';

export async function GET() {
  try {
    const senhaLimpa = 'admin123';
    const saltRounds = 10;
    const novoHash = await bcrypt.hash(senhaLimpa, saltRounds);

    const [rows] = await db.execute('SELECT id FROM usuarios WHERE email = ?', [
      'admin@agrostock.com',
    ]);

    if (rows.length > 0) {
      await db.execute(
        'UPDATE usuarios SET senha = ?, perfil = "admin", nome = "Gestor AgroStock" WHERE email = ?',
        [novoHash, 'admin@agrostock.com']
      );
    } else {
      await db.execute(
        'INSERT INTO usuarios (nome, email, senha, perfil, nome_fazenda) VALUES (?, ?, ?, ?, ?)',
        ['Gestor AgroStock', 'admin@agrostock.com', novoHash, 'admin', 'AgroStock Central']
      );
    }

    return NextResponse.json({
      message: 'Admin configurado com sucesso!',
      email: 'admin@agrostock.com',
      senha: 'admin123',
      hash_gerado: novoHash,
    });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
