'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    setErro('');

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha }),
      });

      const data = await res.json();

      if (res.ok && data.success) {
        const usuarioParaSalvar = data.user || data.usuario;
        localStorage.setItem('user', JSON.stringify(data.usuario));
        router.push('/dashboard');
      } else {
        setErro(data.error || data.message || 'E-mail ou senha incorretos.');
      }
    } catch (err) {
      setErro('Erro ao conectar com o servidor. Verifique sua conexão.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
      <div className="p-8 bg-white shadow-xl rounded-2xl w-full max-w-md border border-gray-100">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-black text-green-700 uppercase tracking-tighter">
            AgroStock
          </h1>
          <p className="text-gray-500 mt-2 font-medium">Acesse sua gestão rural</p>
        </div>

        {erro && (
          <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-6 text-sm text-center border border-red-200 animate-pulse">
            {erro}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-xs font-bold uppercase text-gray-500 mb-1 ml-1">
              E-mail
            </label>
            <input
              type="email"
              className="w-full border border-gray-300 p-3 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all shadow-sm"
              placeholder="seu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-xs font-bold uppercase text-gray-500 mb-1 ml-1">
              Senha
            </label>
            <input
              type="password"
              className="w-full border border-gray-300 p-3 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all shadow-sm"
              placeholder="••••••••"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-green-600 text-white py-4 rounded-xl font-black uppercase tracking-widest hover:bg-green-700 active:scale-95 transition-all duration-200 shadow-lg shadow-green-200">
            Entrar no Sistema
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-gray-600 font-medium">
          Ainda não tem conta?{' '}
          <a href="/cadastro" className="text-green-600 font-extrabold hover:underline">
            Registrar Minha Fazenda
          </a>
        </div>
      </div>
    </div>
  );
}
