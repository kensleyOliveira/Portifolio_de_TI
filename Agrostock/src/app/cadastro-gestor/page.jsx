'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function CadastroGestor() {
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    senha: '',
    perfil: 'admin',
    token: '',
  });

  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch('/api/auth/cadastro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (res.ok) {
        alert('✅ Gestor autenticado e cadastrado com sucesso!');
        router.push('/login');
      } else {
        alert('❌ Erro na validação: ' + (data.error || data.message));
      }
    } catch (err) {
      alert('⚠️ Falha crítica ao conectar com o servidor.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden">
        <div className="bg-slate-800 p-8 text-white text-center">
          <div className="mb-2 flex justify-center">
            <span className="bg-slate-700 p-3 rounded-full text-2xl">🔐</span>
          </div>
          <h2 className="text-2xl font-black uppercase tracking-tighter italic">
            Portal do Gestor
          </h2>
          <p className="text-slate-400 text-xs mt-1 font-medium">
            Área Restrita: Autenticação Administrativa AgroStock
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-5">
          {/* Campo: Nome */}
          <div>
            <label className="block text-[10px] font-black uppercase text-slate-400 mb-1">
              Nome Administrativo
            </label>
            <input
              name="nome"
              type="text"
              required
              placeholder="Ex: Diretor de Operações"
              className="w-full border-b-2 border-slate-100 p-2 outline-none focus:border-slate-800 transition-all text-slate-700 font-medium"
              value={formData.nome}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-[10px] font-black uppercase text-slate-400 mb-1">
              E-mail Corporativo
            </label>
            <input
              name="email"
              type="email"
              required
              placeholder="admin@agrostock.com"
              className="w-full border-b-2 border-slate-100 p-2 outline-none focus:border-slate-800 transition-all text-slate-700 font-medium"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div>
            <label className="block text-[10px] font-black uppercase text-slate-400 mb-1">
              Sua Senha Mestra
            </label>
            <input
              name="senha"
              type="password"
              required
              placeholder="••••••••"
              className="w-full border-b-2 border-slate-100 p-2 outline-none focus:border-slate-800 transition-all text-slate-700 font-medium"
              value={formData.senha}
              onChange={handleChange}
            />
          </div>

          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200">
            <label className="block text-[10px] font-black uppercase text-red-500 mb-1">
              Código Autenticador (Mestre)
            </label>
            <input
              name="token"
              type="password"
              required
              placeholder="Digite o código autenticador"
              className="w-full bg-transparent border-b-2 border-slate-300 p-2 outline-none focus:border-red-500 transition-all text-center font-mono tracking-widest text-slate-800"
              value={formData.token}
              onChange={handleChange}
            />
            <p className="text-[9px] text-slate-400 mt-2 text-center uppercase font-bold">
              Verificação necessária para privilégios de administrador
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full ${loading ? 'bg-slate-400' : 'bg-slate-800 hover:bg-slate-900'} text-white py-4 rounded-xl font-bold uppercase tracking-widest transition-all shadow-lg active:scale-95 flex justify-center items-center gap-2`}>
            {loading ? 'Validando...' : 'Finalizar e Ativar Acesso'}
          </button>

          <div className="text-center pt-2">
            <Link
              href="/"
              className="text-xs text-slate-400 hover:text-slate-600 font-bold uppercase transition-colors">
              ← Sair e voltar para a Home
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
