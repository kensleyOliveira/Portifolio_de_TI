'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export default function DetalhesProdutor() {
  const { id } = useParams();
  const [estoque, setEstoque] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [modalAberto, setModalAberto] = useState(false);
  const [itemParaRejeitar, setItemParaRejeitar] = useState(null);
  const [motivo, setMotivo] = useState('');

  useEffect(() => {
    carregarDados();
  }, [id]);

  async function carregarDados() {
    setCarregando(true);
    try {
      const res = await fetch(`/api/admin/usuarios/${id}/estoque`);
      const data = await res.json();
      if (Array.isArray(data)) setEstoque(data);
    } catch (err) {
      console.error('Erro ao carregar detalhes:', err);
    } finally {
      setCarregando(false);
    }
  }

  const formatarMoeda = (v) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0);

  const totalAprovado = estoque
    .filter((i) => i.status === 'aprovado')
    .reduce((acc, i) => acc + (parseFloat(i.valor_estimado) || 0), 0);
  const alterarStatus = async (itemId, novoStatus, motivoTexto = null) => {
    try {
      const res = await fetch(`/api/admin/estoque/${itemId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          status: novoStatus,
          motivo_rejeicao: motivoTexto,
        }),
      });

      if (res.ok) {
        setEstoque((prev) =>
          prev.map((i) =>
            i.id === itemId ? { ...i, status: novoStatus, motivo_rejeicao: motivoTexto } : i
          )
        );

        if (novoStatus === 'rejeitado') {
          fecharModal();
        }
      } else {
        const errorData = await res.json();
        alert(`Erro: ${errorData.error || 'Falha ao atualizar status'}`);
      }
    } catch (err) {
      console.error('Erro na requisição:', err);
      alert('Erro de conexão ao atualizar status');
    }
  };

  const fecharModal = () => {
    setModalAberto(false);
    setMotivo('');
    setItemParaRejeitar(null);
  };

  const excluirItem = async (itemId) => {
    if (!confirm('Deseja excluir permanentemente este lançamento?')) return;
    try {
      const res = await fetch(`/api/admin/estoque/${itemId}`, { method: 'DELETE' });
      if (res.ok) setEstoque(estoque.filter((i) => i.id !== itemId));
    } catch (err) {
      alert('Erro ao excluir');
    }
  };

  const exportarPDF = () => {
    const doc = new jsPDF();
    doc.setFontSize(18);
    doc.text('Relatório de Inventário - AgroStock', 14, 20);
    doc.setFontSize(10);
    doc.text(`ID Produtor: ${id} | Data: ${new Date().toLocaleDateString('pt-BR')}`, 14, 28);

    const rows = estoque.map((i) => [
      i.insumo,
      `${i.quantidade} ${i.unidade}`,
      i.status.toUpperCase(),
      formatarMoeda(i.valor_estimado),
      i.data_validade ? new Date(i.data_validade).toLocaleDateString('pt-BR') : 'N/A',
    ]);

    autoTable(doc, {
      startY: 35,
      head: [['Insumo', 'Qtd', 'Status', 'Valor Est.', 'Vencimento']],
      body: rows,
      theme: 'grid',
      headStyles: { fillColor: [21, 128, 61] },
    });

    doc.text(
      `Patrimônio Total Aprovado: ${formatarMoeda(totalAprovado)}`,
      14,
      doc.lastAutoTable.finalY + 10
    );
    doc.save(`relatorio_produtor_${id}.pdf`);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <Link href="/admin/usuarios" className="text-green-700 font-bold hover:underline">
            ← Voltar para Lista
          </Link>
          <button
            onClick={exportarPDF}
            className="bg-blue-600 text-white px-5 py-2 rounded-xl font-bold text-xs uppercase shadow-lg hover:bg-blue-700 transition-colors">
            📥 Exportar PDF
          </button>
        </div>

        <div className="flex justify-between items-end mb-8">
          <div>
            <h1 className="text-3xl font-black text-gray-800 uppercase tracking-tighter">
              Inventário do Produtor
            </h1>
            <p className="text-gray-500">Gestão detalhada de insumos e patrimônio</p>
          </div>
          <div className="text-right">
            <p className="text-[10px] font-black text-gray-400 uppercase">Total Aprovado</p>
            <p className="text-2xl font-black text-green-700">{formatarMoeda(totalAprovado)}</p>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100">
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-gray-400 uppercase text-[10px] font-black border-b">
              <tr>
                <th className="p-6">Insumo</th>
                <th className="p-6">Qtd</th>
                <th className="p-6">Status</th>
                <th className="p-6">Valor</th>
                <th className="p-6 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {carregando ? (
                <tr>
                  <td colSpan="5" className="p-20 text-center animate-pulse">
                    Carregando dados do inventário...
                  </td>
                </tr>
              ) : estoque.length === 0 ? (
                <tr>
                  <td colSpan="5" className="p-10 text-center text-gray-400">
                    Nenhum item encontrado para este produtor.
                  </td>
                </tr>
              ) : (
                estoque.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                    <td className="p-6 font-bold text-gray-800">{item.insumo}</td>
                    <td className="p-6 text-gray-600">
                      {item.quantidade}{' '}
                      <span className="text-xs text-gray-400 font-normal">{item.unidade}</span>
                    </td>
                    <td className="p-6">
                      <span
                        className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${
                          item.status === 'aprovado'
                            ? 'bg-green-100 text-green-700'
                            : item.status === 'rejeitado'
                              ? 'bg-red-100 text-red-700'
                              : 'bg-yellow-100 text-yellow-700'
                        }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="p-6 font-black text-gray-700">
                      {formatarMoeda(item.valor_estimado)}
                    </td>
                    <td className="p-6 flex justify-end gap-2">
                      {item.status === 'pendente' && (
                        <>
                          <button
                            title="Aprovar Item"
                            onClick={() => alterarStatus(item.id, 'aprovado')}
                            className="p-2 bg-green-50 text-green-600 rounded-lg hover:bg-green-600 hover:text-white transition-all shadow-sm">
                            ✓
                          </button>
                          <button
                            type="button"
                            title="Rejeitar Item"
                            onClick={() => {
                              console.log('Abrindo modal para item:', item.id);
                              setItemParaRejeitar(item);
                              setModalAberto(true);
                            }}
                            className="p-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-600 hover:text-white transition-all shadow-sm">
                            ✕
                          </button>
                        </>
                      )}
                      <button
                        title="Excluir Definitivamente"
                        onClick={() => excluirItem(item.id)}
                        className="p-2 text-gray-300 hover:text-red-500 transition-colors">
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {modalAberto && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-[9999] p-4">
          <div
            className="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl scale-100 opacity-100 transition-all border border-gray-100"
            onClick={(e) => e.stopPropagation()}>
            <div className="flex flex-col items-center text-center mb-6">
              <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mb-4">
                <span className="text-3xl">⚠️</span>
              </div>
              <h2 className="text-xl font-black text-gray-800 uppercase tracking-tight">
                Motivo da Rejeição
              </h2>
              <p className="text-xs text-gray-400 mt-2 font-medium italic">
                O produtor verá esta justificativa no painel de controle dele.
              </p>
            </div>

            <textarea
              autoFocus
              className="w-full h-32 p-4 bg-gray-50 border border-gray-200 rounded-2xl mb-6 outline-none focus:ring-4 focus:ring-red-500/10 focus:border-red-500 transition-all text-sm text-gray-700 placeholder:text-gray-300"
              placeholder="Ex: Produto com data de validade vencida ou documentação insuficiente..."
              value={motivo}
              onChange={(e) => setMotivo(e.target.value)}
            />

            <div className="flex gap-3">
              <button
                type="button"
                onClick={fecharModal}
                className="flex-1 py-4 text-xs font-black uppercase text-gray-400 hover:text-gray-600 transition-colors">
                Cancelar
              </button>
              <button
                type="button"
                onClick={() => {
                  if (!motivo.trim()) {
                    alert('Por favor, descreva o motivo da rejeição para orientar o produtor.');
                    return;
                  }
                  alterarStatus(itemParaRejeitar.id, 'rejeitado', motivo);
                }}
                className="flex-1 py-4 bg-red-600 text-white rounded-2xl text-xs font-black uppercase shadow-xl shadow-red-200 hover:bg-red-700 active:scale-95 transition-all">
                Confirmar Rejeição
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
