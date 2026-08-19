'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function GerenciarCatalogo() {
  const [produtos, setProdutos] = useState([]);
  const [novoProduto, setNovoProduto] = useState({
    nome: '',
    categoria: '',
    preco_base: '',
    unidade: '',
  });
  const [isAdmin, setIsAdmin] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const loggedUser = JSON.parse(localStorage.getItem('user'));
    if (!loggedUser || loggedUser.perfil !== 'admin') {
      router.push('/dashboard');
      return;
    }
    setIsAdmin(true);
    buscarProdutos();
  }, [router]);

  async function buscarProdutos() {
    const res = await fetch('/api/produtos');
    const data = await res.json();
    setProdutos(data);
  }

  const handleAddProduto = async (e) => {
    e.preventDefault();

    const payload = {
      ...novoProduto,
      preco_base: parseFloat(novoProduto.preco_base) || 0,
    };

    const dadosParaEnviar = {
      nome: novoProduto.nome,
      categoria: novoProduto.categoria,
      unidade: novoProduto.unidade,
      preco_base: novoProduto.preco_base || 0,
    };

    const res = await fetch('/api/produtos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dadosParaEnviar),
    });
    if (res.ok) {
      setNovoProduto({ nome: '', categoria: '', preco_base: '', unidade: '' });
      buscarProdutos();
      alert('Produto adicionado ao catálogo global!');
    }
  };

  const excluirProduto = async (id) => {
    if (
      confirm('Excluir este produto do catálogo? Isso afetará os registros de estoque vinculados.')
    ) {
      const res = await fetch(`/api/produtos/${id}`, { method: 'DELETE' });
      if (res.ok) {
        buscarProdutos();
      } else {
        const data = await res.json();
        alert(data.error || 'Erro ao excluir produto.');
      }
    }
  };

  if (!isAdmin) return null;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-5xl mx-auto">
        <Link href="/dashboard" className="text-green-700 hover:underline text-sm">
          ← Voltar ao Painel
        </Link>
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Gerenciar Catálogo Global</h1>

        <form
          onSubmit={handleAddProduto}
          className="bg-white p-6 rounded-lg shadow-md mb-8 grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div>
            <label className="block text-xs font-bold text-gray-600 uppercase">Nome</label>
            <input
              type="text"
              required
              className="w-full border p-2 rounded mt-1"
              value={novoProduto.nome}
              onChange={(e) => setNovoProduto({ ...novoProduto, nome: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-600 uppercase">Categoria</label>
            <input
              type="text"
              required
              className="w-full border p-2 rounded mt-1"
              value={novoProduto.categoria}
              onChange={(e) => setNovoProduto({ ...novoProduto, categoria: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-600 uppercase">Unidade</label>
            <input
              type="text"
              required
              placeholder="Ex: Litro, KG"
              className="w-full border p-2 rounded mt-1"
              value={novoProduto.unidade}
              onChange={(e) => setNovoProduto({ ...novoProduto, unidade: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-gray-600 uppercase">
              Preço Base (R$)
            </label>
            <input
              type="number"
              step="0.01"
              required
              className="w-full border p-2 rounded mt-1"
              value={novoProduto.preco_base}
              onChange={(e) => setNovoProduto({ ...novoProduto, preco_base: e.target.value })}
            />
          </div>
          <button
            type="submit"
            className="bg-green-600 text-white p-2 rounded font-bold hover:bg-green-700">
            + Adicionar ao Catálogo
          </button>
        </form>

        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-4">Produto</th>
                <th className="p-4">Categoria</th>
                <th className="p-4">Unidade</th>
                <th className="p-4">Preço Base</th>
                <th className="p-4 text-center">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {produtos.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="p-4 font-medium">{p.nome}</td>
                  <td className="p-4">{p.categoria}</td>
                  <td className="p-4">{p.unidade}</td>
                  <td className="p-4">
                    {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(
                      p.preco_base
                    )}
                  </td>
                  <td className="p-4 text-center">
                    <button
                      onClick={() => excluirProduto(p.id)}
                      className="text-red-600 hover:underline">
                      Excluir
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
