'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function AprovacaoInsumos() {
  const [itensPendentes, setItensPendentes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const router = useRouter();

  const carregarPendentes = async () => {
    try {
      setCarregando(true);
      const res = await fetch('/api/admin/estoque/pendentes');
      const data = await res.json();
      if (Array.isArray(data)) {
        setItensPendentes(data);
      }
    } catch (err) {
      console.error('Erro ao carregar pendências:', err);
    } finally {
      setCarregando(false);
    }
  };

  useEffect(() => {
    const loggedUser = JSON.parse(localStorage.getItem('user'));
    if (!loggedUser || loggedUser.perfil !== 'admin') {
      router.push('/');
      return;
    }
    carregarPendentes();
  }, [router]);

  const julgarInsumo = async (id, status) => {
    const confirmacao =
      status === 'aprovado' ? 'Aprovar este lançamento?' : 'Rejeitar este lançamento?';
    if (!confirm(confirmacao)) return;

    try {
      const res = await fetch(`/api/admin/estoque/aprovar/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      });

      if (res.ok) {
        setItensPendentes(itensPendentes.filter((item) => item.id !== id));
      }
    } catch (err) {
      alert('Erro ao processar ação.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <Link href="/dashboard" className="text-green-700 font-bold hover:underline">
          ← Voltar ao Painel
        </Link>

        <div className="mt-4 mb-8">
          <h1 className="text-3xl font-black text-gray-800 uppercase tracking-tighter">
            Aprovação de Lançamentos
          </h1>
          <p className="text-gray-500 font-medium">
            Analise os novos insumos registrados pelos produtores antes de publicá-los.
          </p>
        </div>

        <div className="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50 text-gray-400 uppercase text-[10px] font-black tracking-widest border-b">
              <tr>
                <th className="p-6">Fazenda Solicitante</th>
                <th className="p-6">Insumo / Descrição</th>
                <th className="p-6 text-center">Quantidade</th>
                <th className="p-6">Valor Total</th>
                <th className="p-6 text-right">Ações de Gestão</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {carregando ? (
                <tr>
                  <td colSpan="5" className="p-10 text-center animate-pulse">
                    Buscando pendências...
                  </td>
                </tr>
              ) : itensPendentes.length > 0 ? (
                itensPendentes.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                    <td className="p-6">
                      <p className="font-black text-gray-800">{item.produtor}</p>
                      <p className="text-[10px] text-green-600 font-bold uppercase">
                        Produtor Ativo
                      </p>
                    </td>
                    <td className="p-6">
                      <p className="font-bold text-gray-700">{item.insumo_nome}</p>
                    </td>
                    <td className="p-6 text-center">
                      <span className="bg-gray-100 px-3 py-1 rounded-lg font-bold text-gray-600">
                        {item.quantidade} {item.unidade}
                      </span>
                    </td>
                    <td className="p-6 font-black text-gray-900">
                      {new Intl.NumberFormat('pt-BR', {
                        style: 'currency',
                        currency: 'BRL',
                      }).format(item.valor_estimado)}
                    </td>
                    <td className="p-6 text-right space-x-3">
                      <button
                        onClick={() => julgarInsumo(item.id, 'aprovado')}
                        className="bg-green-600 text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-green-700 shadow-md transition-all active:scale-95">
                        ✓ Aprovar
                      </button>
                      <button
                        onClick={() => julgarInsumo(item.id, 'rejeitado')}
                        className="bg-white text-red-600 border border-red-100 px-4 py-2 rounded-xl text-xs font-bold hover:bg-red-50 transition-all">
                        ✕ Recusar
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="p-20 text-center text-gray-400 italic">
                    Não há novos lançamentos aguardando aprovação.
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
