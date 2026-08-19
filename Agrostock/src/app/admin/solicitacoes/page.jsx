'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function PainelSolicitacoes() {
  const [pedidos, setPedidos] = useState([]);
  const router = useRouter();

  useEffect(() => {
    const loggedUser = JSON.parse(localStorage.getItem('user'));
    if (!loggedUser || loggedUser.perfil !== 'admin') {
      router.push('/');
      return;
    }
    carregarPedidos();
  }, []);

  const carregarPedidos = async () => {
    const res = await fetch('/api/solicitacoes');
    const data = await res.json();
    if (Array.isArray(data)) setPedidos(data);
  };

  const processarPedido = async (pedidoId, estoqueId, acao) => {
    const res = await fetch(`/api/solicitacoes/${pedidoId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ acao, estoque_id: estoqueId }),
    });

    if (res.ok) {
      alert(acao === 'concluido' ? 'Ajuste realizado e item removido!' : 'Solicitação rejeitada.');
      carregarPedidos();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">
        <Link href="/dashboard" className="text-green-700 font-bold hover:underline">
          ← Voltar ao Painel
        </Link>
        <h1 className="text-3xl font-black text-gray-800 mt-4 mb-8 tracking-tighter uppercase">
          Solicitações de Ajuste
        </h1>

        <div className="grid gap-6">
          {pedidos.length > 0 ? (
            pedidos.map((p) => (
              <div
                key={p.id}
                className="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-orange-500 flex justify-between items-center animate-in slide-in-from-left-4 duration-300">
                <div className="space-y-1">
                  <p className="text-xs font-black text-orange-600 uppercase tracking-widest">
                    Pedido #{p.id}
                  </p>
                  <h3 className="text-lg font-bold text-gray-800">Produtor: {p.produtor}</h3>
                  <p className="text-sm text-gray-600 italic">"Motivo: {p.motivo}"</p>
                  <div className="mt-2 py-1 px-3 bg-gray-100 rounded-lg inline-block">
                    <span className="text-xs font-bold text-gray-500 uppercase">
                      Item a remover:
                    </span>
                    <p className="text-sm font-black text-red-600">
                      {p.produto} - {p.quantidade} unidades
                    </p>
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                  <button
                    onClick={() => processarPedido(p.id, p.estoque_id, 'concluido')}
                    className="bg-green-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-green-700 transition shadow-md">
                    Aprovar e Excluir
                  </button>
                  <button
                    onClick={() => processarPedido(p.id, p.estoque_id, 'rejeitado')}
                    className="text-red-500 font-bold text-sm hover:underline">
                    Rejeitar Pedido
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-20 bg-white rounded-3xl border-2 border-dashed border-gray-200">
              <p className="text-gray-400 font-medium italic">
                Nenhuma solicitação pendente no momento.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
