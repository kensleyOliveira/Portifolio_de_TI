'use client';
import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';

export default function EditarInsumo() {
  const { id } = useParams(); // Pega o ID da URL
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    nome: '',
    quantidade: '',
    data_validade: '',
  });

  useEffect(() => {
    async function carregarDados() {
      try {
        const res = await fetch(`/api/estoque/${id}`);
        const data = await res.json();

        const dataFormatada = data.data_validade ? data.data_validade.split('T')[0] : '';

        setFormData({
          nome: data.nome,
          quantidade: data.quantidade,
          data_validade: dataFormatada,
        });
      } catch (err) {
        console.error('Erro ao carregar dados do insumo.');
      } finally {
        setLoading(false);
      }
    }
    carregarDados();
  }, [id]);

  const handleUpdate = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`/api/estoque/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quantidade: formData.quantidade,
          data_validade: formData.data_validade,
        }),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        alert('Estoque atualizado com sucesso!');
        router.push('/dashboard');
      } else {
        alert('Erro: ' + (data.message || data.error));
      }
    } catch (err) {
      alert('Falha na conexão com o servidor.');
    }
  };

  if (loading) return <p className="p-10 text-center">Carregando dados...</p>;

  return (
    <div className="min-h-screen bg-gray-50 p-6 flex items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-xl shadow-lg border border-gray-200">
        <h1 className="text-2xl font-bold text-green-800 mb-2 text-center">Editar Lançamento</h1>
        <p className="text-gray-500 text-center mb-6">
          Insumo: <span className="font-semibold text-gray-700">{formData.nome}</span>
        </p>

        <form onSubmit={handleUpdate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Quantidade Atualizada</label>
            <input
              type="number"
              step="0.01"
              required
              className="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
              value={formData.quantidade}
              onChange={(e) => setFormData({ ...formData, quantidade: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Data de Validade</label>
            <input
              type="date"
              required
              className="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
              value={formData.data_validade}
              onChange={(e) => setFormData({ ...formData, data_validade: e.target.value })}
            />
          </div>

          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={() => router.push('/dashboard')}
              className="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg hover:bg-gray-200 transition font-semibold">
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 bg-green-600 text-white py-2.5 rounded-lg hover:bg-green-700 font-bold transition shadow-md">
              Salvar Alterações
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
