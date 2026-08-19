'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function GestaoUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const loggedUser = JSON.parse(localStorage.getItem('user'));
    if (!loggedUser || loggedUser.perfil !== 'admin') {
      alert('Acesso negado. Esta área é restrita ao Gestor.');
      router.push('/');
      return;
    }

    async function buscarUsuarios() {
      try {
        const res = await fetch('/api/admin/usuarios');
        const data = await res.json();
        if (Array.isArray(data)) {
          setUsuarios(data);
        } else {
          setUsuarios([]);
        }
      } catch (err) {
        console.error('Erro ao buscar usuários:', err);
        setUsuarios([]);
      }
    }
    buscarUsuarios();
  }, [router]);

  const excluirUsuario = async (id) => {
    if (confirm('Deseja realmente excluir este registro de fazenda?')) {
      const res = await fetch(`/api/admin/usuarios/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setUsuarios(usuarios.filter((u) => u.id !== id));
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <Link href="/dashboard" className="text-green-700 hover:underline text-sm font-bold">
          ← Voltar ao Painel
        </Link>
        <h1 className="text-3xl font-black text-gray-800 mt-4 mb-8">Gestão de Produtores</h1>

        <div className="bg-white shadow-xl rounded-2xl overflow-hidden border border-gray-200">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-100 text-gray-600 uppercase text-xs font-bold">
              <tr>
                <th className="p-4">Produtor / Fazenda</th>
                <th className="p-4">Contato</th>
                <th className="p-4">Perfil</th>
                <th className="p-4 text-center">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {usuarios.length > 0 ? (
                usuarios.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50 transition">
                    <td className="p-4">
                      <p className="font-bold text-gray-800">{u.nome}</p>
                      <p className="text-xs text-green-600 font-semibold">
                        {u.nome_fazenda || 'Sem fazenda'}
                      </p>
                    </td>
                    <td className="p-4">
                      <p className="text-sm">{u.email}</p>
                      <p className="text-xs text-gray-400">{u.telefone}</p>
                    </td>
                    <td className="p-4">
                      <span
                        className={`px-2 py-1 rounded-full text-[10px] font-black uppercase ${u.perfil === 'admin' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'}`}>
                        {u.perfil}
                      </span>
                    </td>
                    <td className="p-4 text-center">
                      <button
                        onClick={() => excluirUsuario(u.id)}
                        className="text-red-600 hover:text-red-800 font-bold text-sm">
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="p-10 text-center text-gray-400">
                    Nenhum produtor cadastrado.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
