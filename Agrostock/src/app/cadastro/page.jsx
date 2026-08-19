'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function CadastroFazenda() {
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    senha: '',
    nome_fazenda: '',
    endereco_fazenda: '',
    telefone: '',
    perfil: 'comum',
  });
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/api/auth/cadastro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });

    const data = await res.json();

    if (res.ok) {
      alert('Registro concluído!');
      router.push('/login');
    } else {
      alert('Erro: ' + (data.error || 'Falha no cadastro'));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-xl overflow-hidden flex flex-col md:flex-row">
        <div className="bg-green-700 md:w-1/3 p-8 text-white flex flex-col justify-center">
          <h2 className="text-3xl font-bold mb-4 font-sans">AgroStock</h2>
          <p className="text-green-100 text-sm">
            Junte-se a centenas de produtores que digitalizaram sua gestão rural.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="p-8 md:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-4">
          <h2 className="col-span-full text-2xl font-bold text-gray-800 mb-4">
            Registro da Fazenda
          </h2>

          <div className="col-span-full">
            <label className="block text-xs font-bold uppercase text-gray-500">
              Nome do Produtor
            </label>
            <input
              type="text"
              required
              className="w-full border-b-2 p-2 outline-none focus:border-green-600"
              onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase text-gray-500">E-mail</label>
            <input
              type="email"
              required
              className="w-full border-b-2 p-2 outline-none focus:border-green-600"
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase text-gray-500">
              Telefone Contato
            </label>
            <input
              type="text"
              required
              className="w-full border-b-2 p-2 outline-none focus:border-green-600"
              placeholder="(34) 99999-9999"
              onChange={(e) => setFormData({ ...formData, telefone: e.target.value })}
            />
          </div>

          <div className="col-span-full">
            <label className="block text-xs font-bold uppercase text-gray-500">
              Nome da Fazenda
            </label>
            <input
              type="text"
              required
              className="w-full border-b-2 p-2 outline-none focus:border-green-600"
              onChange={(e) => setFormData({ ...formData, nome_fazenda: e.target.value })}
            />
          </div>

          <div className="col-span-full">
            <label className="block text-xs font-bold uppercase text-gray-500">
              Endereço da Propriedade
            </label>
            <input
              type="text"
              required
              className="w-full border-b-2 p-2 outline-none focus:border-green-600"
              onChange={(e) => setFormData({ ...formData, endereco_fazenda: e.target.value })}
            />
          </div>

          <div className="col-span-full">
            <label className="block text-xs font-bold uppercase text-gray-500">
              Senha de Acesso
            </label>
            <input
              type="password"
              required
              className="w-full border-b-2 p-2 outline-none focus:border-green-600"
              onChange={(e) => setFormData({ ...formData, senha: e.target.value })}
            />
          </div>

          <button
            type="submit"
            className="col-span-full bg-green-600 text-white py-3 rounded-lg font-bold mt-4 hover:bg-green-700 transition shadow-lg">
            Finalizar Registro
          </button>

          <Link
            href="/login"
            className="col-span-full text-center text-sm text-gray-500 hover:underline">
            Já possui conta? Faça login
          </Link>
        </form>
      </div>
    </div>
  );
}
