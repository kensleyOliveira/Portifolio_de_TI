'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function PerfilPage() {
  const [user, setUser] = useState(null);
  const [formData, setFormData] = useState({
    nome: '',
    nome_fazenda: '',
    telefone: '',
    endereco_fazenda: '',
    email: '',
  });
  const router = useRouter();

  useEffect(() => {
    const loggedUser = JSON.parse(localStorage.getItem('user'));
    if (!loggedUser) return router.push('/');
    setUser(loggedUser);
    setFormData(loggedUser);
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();
    const res = await fetch(`/api/admin/usuarios/${user.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    if (res.ok) {
      localStorage.setItem('user', JSON.stringify({ ...user, ...formData }));
      alert('Dados atualizados com sucesso!');
      router.push('/dashboard');
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-3xl shadow-xl p-10 border border-gray-100">
        <h1 className="text-3xl font-black text-gray-800 mb-6">Configurações da Conta</h1>

        <form onSubmit={handleUpdate} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-black uppercase text-gray-400">
                Nome do Produtor
              </label>
              <input
                type="text"
                value={formData.nome}
                className="w-full border-b-2 p-2 outline-none focus:border-green-600"
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-xs font-black uppercase text-gray-400">
                E-mail (Apenas Gestor altera)
              </label>
              <input
                type="email"
                value={formData.email}
                disabled
                className="w-full border-b-2 p-2 bg-gray-50 text-gray-400 cursor-not-allowed"
              />
            </div>
            <div className="col-span-full">
              <label className="block text-xs font-black uppercase text-gray-400">
                Nome da Fazenda
              </label>
              <input
                type="text"
                value={formData.nome_fazenda}
                className="w-full border-b-2 p-2 outline-none focus:border-green-600"
                onChange={(e) => setFormData({ ...formData, nome_fazenda: e.target.value })}
              />
            </div>
            <div className="col-span-full">
              <label className="block text-xs font-black uppercase text-gray-400">Endereço</label>
              <input
                type="text"
                value={formData.endereco_fazenda}
                className="w-full border-b-2 p-2 outline-none focus:border-green-600"
                onChange={(e) => setFormData({ ...formData, endereco_fazenda: e.target.value })}
              />
            </div>
          </div>

          <div className="flex gap-4 pt-6">
            <button
              type="submit"
              className="flex-1 bg-green-600 text-white py-3 rounded-xl font-bold hover:bg-green-700 transition">
              Salvar Alterações
            </button>
            <button
              type="button"
              onClick={() => router.push('/dashboard')}
              className="px-6 py-3 border border-gray-200 rounded-xl font-bold text-gray-500 hover:bg-gray-50">
              Voltar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
