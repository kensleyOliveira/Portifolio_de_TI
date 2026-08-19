'use client';
import Link from 'next/link';

export default function LandingPage() {
  const iniciarSlideShow = (e) => {
    e.preventDefault();
    const url = '/Agrostock_Financial_Intelligence.pdf#toolbar=0&navpanes=0&view=Fit';

    window.open(
      url,
      'ApresentacaoAgrostock',
      'fullscreen=yes,menubar=no,status=no,titlebar=no,toolbar=no'
    );
  };

  return (
    <div className="min-h-screen bg-white text-gray-800 font-sans">
      <nav className="flex justify-between items-center px-8 py-6 bg-white shadow-sm sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🌱</span>
          <span className="text-2xl font-black text-green-700 tracking-tighter uppercase">
            AgroStock
          </span>
        </div>
        <div className="flex gap-6">
          <Link
            href="/login"
            className="px-8 py-2 bg-green-600 text-white font-bold rounded-full hover:bg-green-700 transition shadow-md">
            Entrar no Sistema
          </Link>
        </div>
      </nav>

      <header className="container mx-auto px-8 py-20 flex flex-col md:flex-row items-center justify-between gap-12">
        <div className="md:w-1/2 space-y-6">
          <h1 className="text-5xl md:text-7xl font-black text-gray-900 leading-tight">
            Inteligência <span className="text-green-600">Financeira</span> no seu estoque.
          </h1>
          <p className="text-xl text-gray-600 leading-relaxed">
            O AgroStock transforma insumos em dados estratégicos. Monitore seu patrimônio agrícola
            com precisão, evite desperdícios e potencialize sua rentabilidade através da
            digitalização.
          </p>
          <div className="flex gap-4 pt-4">
            <Link
              href="/cadastro"
              className="px-8 py-4 bg-green-600 text-white text-lg font-bold rounded-xl hover:bg-green-700 transition shadow-lg">
              Registrar Minha Fazenda
            </Link>
            <a
              href="/Agrostock_Financial_Intelligence.pdf#toolbar=0&navpanes=0&scrollbar=0&view=Fit"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 border-2 border-green-600 text-green-700 text-lg font-bold rounded-xl hover:bg-green-50 transition flex items-center gap-2">
              <button
                onClick={iniciarSlideShow}
                className="px-8 py-4 border-2 border-green-600 text-green-700 text-lg font-bold rounded-xl hover:bg-green-50 transition flex items-center gap-2">
                <span>📊</span> Acessar Painel de Marketing
              </button>
            </a>
          </div>
        </div>

        <div className="md:w-1/2">
          <div className="relative bg-green-100 rounded-3xl p-8 overflow-hidden shadow-2xl">
            <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
              <div className="flex justify-between border-b pb-2">
                <span className="font-bold">Patrimônio em Fertilizantes</span>
                <span className="text-green-600 font-bold">R$ 45.200,00</span>
              </div>
              <div className="flex justify-between border-b pb-2">
                <span className="font-bold">Sementes em Estoque</span>
                <span className="text-green-600 font-bold">R$ 12.800,00</span>
              </div>
              <div className="w-full bg-gray-100 h-4 rounded-full overflow-hidden">
                <div className="bg-green-500 w-full h-full"></div>
              </div>
              <p className="text-xs text-gray-400 text-center uppercase tracking-widest">
                Interface de Inteligência Financeira Agro
              </p>
            </div>
          </div>
        </div>
      </header>
      <section className="bg-gray-50 py-24">
        <div className="container mx-auto px-8">
          <h2 className="text-3xl font-bold text-center mb-16">Diferenciais Estratégicos</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-bold mb-2">Visão de Capital</h3>
              <p className="text-gray-600">
                Transforme a contagem de sacas em valor líquido. Tenha o balanço real do seu
                investimento no campo a qualquer momento.
              </p>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center">
              <div className="text-4xl mb-4">📉</div>
              <h3 className="text-xl font-bold mb-2">Redução de Custos</h3>
              <p className="text-gray-600">
                Identifique excessos e gargalos na gestão de insumos, otimizando o fluxo de caixa da
                sua safra.
              </p>
            </div>
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 text-center">
              <div className="text-4xl mb-4">✅</div>
              <h3 className="text-xl font-bold mb-2">Auditoria e Rigor</h3>
              <p className="text-gray-600">
                Lançamentos validados por gestores, garantindo que os dados do seu inventário sejam
                100% confiáveis.
              </p>
            </div>
          </div>
        </div>
      </section>

      <footer className="py-12 border-t border-gray-100 text-center text-gray-500 text-sm bg-gray-50">
        <p>© 2026 AgroStock - Inteligência em Gestão Rural.</p>
        <div className="mt-4 flex justify-center gap-6">
          <Link href="/cadastro-gestor" className="hover:text-green-700 font-bold transition">
            Área do Gestor (Novo Cadastro)
          </Link>
          <span className="text-gray-300">|</span>
          <p className="font-bold text-green-700">Otimizando o Futuro do Agronegócio.</p>
        </div>
      </footer>
    </div>
  );
}
