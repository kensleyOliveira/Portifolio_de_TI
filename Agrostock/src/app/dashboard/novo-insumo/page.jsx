'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function NovoLançamento() {
  const [produtos, setProdutos] = useState([]);
  const [formData, setFormData] = useState({
    produto_id: '',
    quantidade: '',
    data_validade: '',
  });
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const loggedUser = localStorage.getItem('user');
    if (!loggedUser) {
      router.push('/login');
    } else {
      setUser(JSON.parse(loggedUser));
    }

    async function buscarCatalogo() {
      const res = await fetch('/api/produtos');
      const data = await res.json();
      setProdutos(data);
    }
    buscarCatalogo();
  }, [router]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      ...formData,
      usuario_id: user.id,
    };

    const res = await fetch('/api/estoque', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      alert('Insumo lançado com sucesso!');
      router.push('/dashboard');
    } else {
      alert('Erro ao realizar lançamento.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-lg mx-auto bg-white p-8 rounded-xl shadow-md border border-gray-200">
        <h1 className="text-2xl font-bold text-green-800 mb-6 text-center">
          Novo Lançamento de Insumo
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Selecione o Insumo</label>
            <select
              required
              className="w-full border p-2 rounded-lg mt-1"
              onChange={(e) => setFormData({ ...formData, produto_id: e.target.value })}>
              <option value="">Selecione um produto...</option>
              {produtos.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.nome} ({p.unidade})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Quantidade</label>
            <input
              type="number"
              step="0.01"
              required
              className="w-full border p-2 rounded-lg mt-1"
              placeholder="Ex: 50.5"
              onChange={(e) => setFormData({ ...formData, quantidade: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Data de Validade</label>
            <input
              type="date"
              required
              className="w-full border p-2 rounded-lg mt-1"
              onChange={(e) => setFormData({ ...formData, data_validade: e.target.value })}
            />
          </div>

          <div className="flex gap-4 mt-8">
            <button
              type="button"
              onClick={() => router.push('/dashboard')}
              className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg hover:bg-gray-300 transition">
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 font-bold transition">
              Confirmar Lançamento
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
