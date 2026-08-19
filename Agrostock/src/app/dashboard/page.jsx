'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [listaUsuarios, setListaUsuarios] = useState([]);
  const [montado, setMontado] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setMontado(true);
    const loggedUser = localStorage.getItem('user');

    if (!loggedUser) {
      router.push('/login');
    } else {
      const parsedUser = JSON.parse(loggedUser);
      setUser(parsedUser);

      if (parsedUser.perfil === 'admin') {
        fetch('/api/admin/usuarios')
          .then((res) => res.json())
          .then((data) => setListaUsuarios(data))
          .catch((err) => console.error('Erro ao carregar usuários', err));
      }
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/');
  };

  if (!montado || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-green-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500 font-medium italic">Sincronizando AgroStock...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-green-800 text-white p-4 shadow-lg flex justify-between items-center sticky top-0 z-50">
        <div className="flex flex-col">
          <h1 className="text-xl font-black flex items-center gap-2 tracking-tighter">
            🌱 AGROSTOCK
            <span className="hidden sm:inline text-[10px] font-normal border-l pl-2 border-green-600 uppercase tracking-widest ml-2">
              {user.nome_fazenda || 'Gestão Rural'}
            </span>
          </h1>
        </div>

        <div className="flex items-center gap-5">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-bold leading-none">{user.nome}</p>
            <p className="text-[10px] text-green-300 uppercase mt-1">
              {user.perfil === 'admin' ? 'Administrador' : user.telefone || user.email}
            </p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 px-4 py-1.5 rounded-lg text-xs font-bold transition-all shadow-md active:scale-95">
            Sair
          </button>
        </div>
      </nav>

      <main className="container mx-auto p-4 md:p-8">
        {user.perfil === 'admin' ? (
          <AdminView usuarios={listaUsuarios} />
        ) : (
          <UserView userData={user} />
        )}
      </main>
    </div>
  );
}

function UserView({ userData }) {
  const [estoque, setEstoque] = useState([]);
  const [valorTotalGeral, setValorTotalGeral] = useState(0);
  const [dadosFazenda, setDadosFazenda] = useState(userData);
  const [showModal, setShowModal] = useState(false);
  const [idParaAjuste, setIdParaAjuste] = useState(null);
  const [motivo, setMotivo] = useState('');

  const carregarDadosCompletos = useCallback(async () => {
    try {
      const resEstoque = await fetch(`/api/estoque?usuario_id=${userData.id}`);
      const dataEstoque = await resEstoque.json();

      if (Array.isArray(dataEstoque)) {
        setEstoque(dataEstoque);
        const totalAprovado = dataEstoque
          .filter((item) => item.status === 'aprovado')
          .reduce((acc, item) => acc + (parseFloat(item.valor_estimado) || 0), 0);
        setValorTotalGeral(totalAprovado);
      }

      const resUser = await fetch(`/api/admin/usuarios/${userData.id}`);
      if (resUser.ok) {
        const dataUser = await resUser.json();
        setDadosFazenda(dataUser);
      }
    } catch (err) {
      console.error('Erro ao sincronizar dashboard:', err);
    }
  }, [userData.id]);

  useEffect(() => {
    if (userData?.id) carregarDadosCompletos();
  }, [userData, carregarDadosCompletos]);

  const excluirItemRejeitado = async (itemId) => {
    if (!confirm('Deseja remover este item rejeitado? Isso não pode ser desfeito.')) return;
    try {
      const res = await fetch(`/api/admin/estoque/${itemId}`, { method: 'DELETE' });
      if (res.ok) setEstoque((prev) => prev.filter((item) => item.id !== itemId));
    } catch (err) {
      console.error('Erro ao excluir:', err);
    }
  };

  const enviarSolicitacao = async () => {
    if (!motivo.trim()) return alert('Por favor, descreva o motivo.');
    try {
      const res = await fetch('/api/solicitacoes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario_id: userData.id, estoque_id: idParaAjuste, motivo }),
      });
      if (res.ok) {
        alert('Solicitação enviada!');
        setShowModal(false);
        setMotivo('');
      }
    } catch (err) {
      console.error(err);
    }
  };

  const formatarMoeda = (valor) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(
      valor || 0
    );
  };

  const processarDadosGrafico = () => {
    const categoriasMap = {};

    const itensAprovados = estoque.filter((item) => item.status === 'aprovado');

    itensAprovados.forEach((item) => {
      let nomeCat = item.categoria;

      if (!nomeCat || nomeCat === 'Não Categorizado') {
        const nomeProd = (item.nome || '').toLowerCase();

        if (nomeProd.includes('npk') || nomeProd.includes('fertilizante')) {
          nomeCat = 'Fertilizantes';
        } else if (nomeProd.includes('glifosato') || nomeProd.includes('herbicida')) {
          nomeCat = 'Herbicidas';
        } else if (nomeProd.includes('semente') || nomeProd.includes('milho')) {
          nomeCat = 'Sementes';
        } else if (nomeProd.includes('extravon') || nomeProd.includes('adjuvante')) {
          nomeCat = 'Adjuvante';
        } else {
          nomeCat = 'Outros';
        }
      }

      const valor = parseFloat(item.valor_estimado) || 0;

      if (categoriasMap[nomeCat]) {
        categoriasMap[nomeCat] += valor;
      } else {
        categoriasMap[nomeCat] = valor;
      }
    });

    if (Object.keys(categoriasMap).length === 0) {
      return { labels: [], datasets: [] };
    }

    return {
      labels: Object.keys(categoriasMap),
      datasets: [
        {
          data: Object.values(categoriasMap),
          backgroundColor: ['#166534', '#ef4444', '#f59e0b', '#3b82f6', '#6b7280'],
          borderWidth: 2,
          borderColor: '#ffffff',
          hoverOffset: 15,
        },
      ],
    };
  };

  const optionsGrafico = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: { usePointStyle: true, font: { size: 10, weight: 'bold' } },
      },
    },
    cutout: '70%',
    maintainAspectRatio: false,
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-500">
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="space-y-1">
          <h2 className="text-3xl font-black text-gray-900 tracking-tight">
            Olá, {dadosFazenda?.nome?.split(' ')[0] || 'Produtor'}!
          </h2>
          <div className="flex items-center gap-2 text-gray-500 font-medium">
            <span className="text-xl">📍</span>
            <p>{dadosFazenda?.nome_fazenda || 'Sua Fazenda'}</p>
          </div>
        </div>

        <div className="bg-green-50 px-6 py-4 rounded-2xl border border-green-100 shadow-inner min-w-[240px]">
          <p className="text-[10px] uppercase font-black text-green-600 tracking-widest mb-1">
            Patrimônio Aprovado
          </p>
          <p className="text-3xl font-black text-green-800 tracking-tighter">
            {formatarMoeda(valorTotalGeral)}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col justify-center">
          <h3 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-4">
            Divisão por Categoria
          </h3>
          <div className="h-[250px]">
            {valorTotalGeral > 0 ? (
              <Doughnut data={processarDadosGrafico()} options={optionsGrafico} />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-300 italic text-sm text-center px-10">
                Aguardando aprovação de itens para exibir a distribuição de patrimônio...
              </div>
            )}
          </div>
        </div>

        <div className="bg-green-800 rounded-3xl p-8 text-white flex flex-col justify-between relative overflow-hidden shadow-xl shadow-green-100">
          <div className="relative z-10">
            <h3 className="text-green-300 font-black text-[10px] uppercase tracking-[0.2em] mb-2">
              Status de Operação
            </h3>
            <p className="text-2xl font-bold leading-tight">
              Sua fazenda possui {estoque.filter((i) => i.status === 'pendente').length} itens
              aguardando análise.
            </p>
          </div>
          <div className="mt-8 relative z-10">
            <Link
              href="/dashboard/novo-insumo"
              className="block w-full bg-white text-green-800 text-center py-4 rounded-2xl font-black text-xs uppercase hover:bg-green-50 transition-all shadow-lg active:scale-95">
              Aumentar Inventário
            </Link>
          </div>
          <div className="absolute -right-10 -bottom-10 w-40 h-40 bg-green-700 rounded-full opacity-50"></div>
        </div>
      </div>

      <div className="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
        <div className="p-6 border-b border-gray-50 flex flex-col sm:flex-row justify-between items-center gap-4 bg-gray-50/50">
          <h3 className="text-xl font-bold text-gray-800">Meu Inventário</h3>
          <Link
            href="/dashboard/novo-insumo"
            className="w-full sm:w-auto bg-green-600 text-white px-6 py-3 rounded-xl hover:bg-green-700 font-bold transition-all shadow-lg active:scale-95">
            + Novo Lançamento
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-white text-gray-400 uppercase text-[10px] font-black tracking-widest border-b">
              <tr>
                <th className="p-6">Insumo</th>
                <th className="p-6 text-center">Quantidade</th>
                <th className="p-6 text-center">Status / Observação</th>
                <th className="p-6">Subtotal</th>
                <th className="p-6 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {estoque.length > 0 ? (
                estoque.map((item) => (
                  <tr key={item.id} className="hover:bg-green-50/30 transition-colors group">
                    <td className="p-6">
                      <p className="font-bold text-gray-800 group-hover:text-green-700">
                        {item.nome}
                      </p>
                      <p className="text-[9px] text-gray-400 uppercase">
                        {item.categoria || 'Geral'}
                      </p>
                    </td>
                    <td className="p-6 text-center font-medium">
                      {item.quantidade}{' '}
                      <span className="text-[10px] text-gray-400 uppercase">{item.unidade}</span>
                    </td>
                    <td className="p-6">
                      <div className="flex flex-col items-center gap-2">
                        <span
                          className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${
                            item.status === 'aprovado'
                              ? 'bg-green-100 text-green-700'
                              : item.status === 'rejeitado'
                                ? 'bg-red-100 text-red-700'
                                : 'bg-yellow-100 text-yellow-700'
                          }`}>
                          {item.status || 'pendente'}
                        </span>
                        {item.status === 'rejeitado' && item.motivo_rejeicao && (
                          <p className="text-[9px] text-red-500 italic text-center max-w-[150px]">
                            "{item.motivo_rejeicao}"
                          </p>
                        )}
                      </div>
                    </td>
                    <td className="p-6 font-black text-green-700">
                      {formatarMoeda(item.valor_estimado)}
                    </td>
                    <td className="p-6 text-right">
                      {item.status === 'aprovado' ? (
                        <button
                          onClick={() => {
                            setIdParaAjuste(item.id);
                            setShowModal(true);
                          }}
                          className="text-orange-600 font-bold text-[10px] uppercase border-b border-orange-200">
                          Solicitar Ajuste
                        </button>
                      ) : item.status === 'rejeitado' ? (
                        <div className="flex justify-end gap-3">
                          <Link
                            href="/dashboard/novo-insumo"
                            className="bg-blue-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold">
                            Corrigir
                          </Link>
                          <button
                            onClick={() => excluirItemRejeitado(item.id)}
                            className="text-gray-400 hover:text-red-600">
                            🗑️
                          </button>
                        </div>
                      ) : (
                        <span className="text-gray-300 text-[10px] font-bold uppercase italic">
                          Em análise...
                        </span>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="p-20 text-center text-gray-300 italic text-sm">
                    Nenhum insumo encontrado.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-[100] p-4">
          <div className="bg-white p-8 rounded-3xl max-w-md w-full shadow-2xl">
            <h3 className="text-xl font-black text-gray-800 mb-2 uppercase">Solicitar Ajuste</h3>
            <textarea
              className="w-full border-2 border-gray-100 rounded-2xl p-4 outline-none focus:border-orange-500 bg-gray-50 mb-6 h-36 text-sm"
              placeholder="Descreva o que precisa ser alterado..."
              value={motivo}
              onChange={(e) => setMotivo(e.target.value)}
            />
            <div className="flex gap-3">
              <button
                onClick={enviarSolicitacao}
                className="flex-1 bg-orange-600 text-white py-4 rounded-2xl font-black text-xs uppercase">
                Enviar
              </button>
              <button
                onClick={() => setShowModal(false)}
                className="px-6 py-4 font-bold text-gray-400 text-xs uppercase">
                Voltar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function AdminView({ usuarios = [] }) {
  const formatarMoeda = (valor) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0);
  const patrimonioGlobal = usuarios.reduce(
    (acc, user) => acc + (parseFloat(user.patrimonio_total) || 0),
    0
  );

  return (
    <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-3xl font-black text-gray-800 tracking-tight uppercase">
            Painel Gestor
          </h2>
          <p className="text-gray-500 font-medium">Visão consolidada do sistema</p>
        </div>
        <div className="bg-green-800 text-white px-8 py-5 rounded-3xl shadow-2xl border-b-8 border-green-900 flex flex-col items-end">
          <p className="text-[10px] uppercase font-black text-green-300 tracking-widest mb-1">
            Patrimônio Global
          </p>
          <p className="text-3xl font-black">{formatarMoeda(patrimonioGlobal)}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 hover:shadow-xl transition-all">
          <h3 className="text-gray-400 font-black uppercase text-[10px] tracking-widest">
            Fazendas
          </h3>
          <p className="text-6xl font-black mt-2 text-gray-900 tracking-tighter">
            {usuarios.length}
          </p>
          <Link
            href="/admin/usuarios"
            className="mt-8 flex items-center gap-2 text-blue-600 text-xs font-black uppercase">
            Gerenciar Produtores <span>→</span>
          </Link>
        </div>

        <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border border-gray-100 hover:shadow-xl transition-all">
          <h3 className="text-gray-400 font-black uppercase text-[10px] tracking-widest">
            Insumos
          </h3>
          <p className="text-6xl font-black mt-2 text-gray-900 italic tracking-tighter">Ativo</p>
          <Link
            href="/produtos"
            className="mt-8 flex items-center gap-2 text-green-600 text-xs font-black uppercase">
            Editar Catálogo <span>→</span>
          </Link>
        </div>

        <div className="bg-white p-8 rounded-[2.5rem] shadow-sm border-t-8 border-orange-500 hover:shadow-xl transition-all">
          <h3 className="text-gray-400 font-black uppercase text-[10px] tracking-widest">
            Ações Rápidas
          </h3>
          <div className="mt-6 flex flex-col gap-3">
            <Link
              href="/admin/aprovacoes"
              className="bg-orange-50 text-orange-700 p-3 rounded-xl text-[10px] font-black hover:bg-orange-600 hover:text-white transition-all uppercase flex justify-between">
              Aprovar Insumos <span>→</span>
            </Link>
            <Link
              href="/admin/solicitacoes"
              className="bg-red-50 text-red-700 p-3 rounded-xl text-[10px] font-black hover:bg-red-600 hover:text-white transition-all uppercase flex justify-between">
              Pedidos de Exclusão <span>→</span>
            </Link>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-[2.5rem] shadow-xl border border-gray-100 overflow-hidden">
        <div className="p-8 bg-gray-50/50 border-b border-gray-100">
          <h3 className="font-black text-gray-800 uppercase text-xs tracking-[0.2em]">
            Rank de Patrimônio
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="text-[10px] font-black text-gray-400 uppercase tracking-widest border-b">
              <tr>
                <th className="p-8">Identificação</th>
                <th className="p-8">Capital</th>
                <th className="p-8 text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {usuarios.map((produtor) => (
                <tr key={produtor.id} className="hover:bg-gray-50/80 transition-all group">
                  <td className="p-8">
                    <p className="font-black text-gray-800 text-lg group-hover:text-green-800">
                      {produtor.nome}
                    </p>
                    <p className="text-[10px] text-green-600 font-black uppercase">
                      {produtor.nome_fazenda}
                    </p>
                  </td>
                  <td className="p-8">
                    <p className="font-black text-gray-900 text-xl">
                      {formatarMoeda(produtor.patrimonio_total)}
                    </p>
                  </td>
                  <td className="p-8 text-right">
                    <Link
                      href={`/admin/usuarios/${produtor.id}`}
                      className="inline-block bg-gray-900 text-white px-6 py-3 rounded-2xl text-[10px] font-black hover:bg-green-700 transition-all uppercase shadow-lg">
                      Inspecionar
                    </Link>
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
