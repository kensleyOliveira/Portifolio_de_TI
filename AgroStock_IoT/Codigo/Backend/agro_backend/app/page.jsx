
'use client';

import { useEffect, useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

export default function PlataformaTelemetria() {
  const [abaAtiva, setAbaAtiva] = useState('home');

  // Estados do Dashboard Histórico
  const [leituras, setLeituras] = useState([]);
  const [dataInicio, setDataInicio] = useState('');
  const [dataFim, setDataFim] = useState('');
  const [mostrarTemperatura, setMostrarTemperatura] = useState(true);
  const [mostrarUmidade, setMostrarUmidade] = useState(true);
  const [carregandoDashboard, setCarregandoDashboard] = useState(false);

  // Estados da Previsão do Tempo
  const [previsao, setPrevisao] = useState([]);
  const [carregandoPrevisao, setCarregandoPrevisao] = useState(false);

  // ---------------------------------------------------------
  // FUNÇÕES DE BUSCA DE DADOS
  // ---------------------------------------------------------
  const buscarHistorico = async () => {
    setCarregandoDashboard(true);
    try {
      let url = '/api/telemetria';
      if (dataInicio && dataFim) {
        url += `?inicio=${dataInicio}&fim=${dataFim}`;
      }

      const response = await fetch(url);
      const result = await response.json();
      

      if (result.success) {
        const dadosInvertidos = result.data.reverse(); 

        const dadosFormatados = dadosInvertidos.map(item => {
          const dataObjeto = new Date(item.timestamp);

          return {
            ...item,
            dataHora: dataObjeto.toLocaleString('pt-BR', { 
              day: '2-digit', 
              month: '2-digit', 
              hour: '2-digit', 
              minute: '2-digit' 
            }),
            temperatura: parseFloat(item.temperatura),
            umidade: parseFloat(item.umidade)
          };
        });
        setLeituras(dadosFormatados);
      }

    } catch (error) {
      console.error("Erro ao carregar histórico:", error);
    }
    setCarregandoDashboard(false);
  };

  const buscarPrevisaoRegional = async () => {
    setCarregandoPrevisao(true);
    try {
      const response = await fetch('/api/previsao');
      const result = await response.json();

      if (result.success) {
        const formatado = result.data.daily.time.map((dataTempo, index) => ({
          data: new Date(dataTempo).toLocaleDateString('pt-BR', { weekday: 'short', day: '2-digit', month: '2-digit' }),
          tempMax: result.data.daily.temperature_2m_max[index],
          tempMin: result.data.daily.temperature_2m_min[index],
          chuvaProb: result.data.daily.precipitation_probability_max[index]
        }));

        setPrevisao(formatado);
      } else {
        console.error("Erro do servidor:", result.message);
      }
    } catch (error) {
      console.error("Erro ao carregar previsão no frontend:", error);
    }
    setCarregandoPrevisao(false);
  };

  useEffect(() => {
    if (abaAtiva === 'dashboard') buscarHistorico();
    if (abaAtiva === 'previsao' && previsao.length === 0) buscarPrevisaoRegional();
  }, [abaAtiva]);

  // ---------------------------------------------------------
  // COMPONENTES DAS TELAS
  // ---------------------------------------------------------
  
  const TelaHome = () => (
    <div className="animate-fade-in bg-white p-8 rounded-xl shadow-sm border border-gray-100">
      <h2 className="text-3xl font-bold text-green-800 mb-6">Bem-vindo ao Ecossistema de Telemetria</h2>
      <div className="space-y-6 text-gray-700 text-lg leading-relaxed">
        <p>
          Em atividades que dependem diretamente do microclima, como o <strong>monitoramento de lavouras</strong> e o armazenamento de insumos, a falta de dados em tempo real dificulta tomadas de decisão rápidas e assertivas.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
          <div className="bg-green-50 p-6 rounded-lg border border-green-100">
            <h3 className="text-xl font-semibold text-green-700 mb-3">Visão Micro (Borda)</h3>
            <p className="text-sm">
              Sensores IoT alocados na área de interesse realizam leituras hiperlocais de temperatura e umidade. Isso permite acionar irrigações emergenciais ou aplicar preventivos de pragas baseados na realidade exata do solo.
            </p>
          </div>
          <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
            <h3 className="text-xl font-semibold text-blue-700 mb-3">Visão Macro (Previsão)</h3>
            <p className="text-sm">
              A integração com modelos meteorológicos fornece uma visão ampla para os próximos 15 dias. O cruzamento do cenário local com a tendência climática regional transforma a gestão em um planejamento operacional estratégico.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const TelaDashboard = () => (
    <div className="animate-fade-in space-y-6">
      {/* Barra de Filtros */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-wrap gap-6 items-end">
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-600">Data Início</label>
          <input 
            type="date" 
            className="border p-2 rounded-md bg-gray-50 outline-none focus:border-green-500"
            value={dataInicio} onChange={e => setDataInicio(e.target.value)}
          />
        </div>
        <div className="flex flex-col gap-2">
          <label className="text-sm font-semibold text-gray-600">Data Fim</label>
          <input 
            type="date" 
            className="border p-2 rounded-md bg-gray-50 outline-none focus:border-green-500"
            value={dataFim} onChange={e => setDataFim(e.target.value)}
          />
        </div>
        <button 
          onClick={buscarHistorico}
          className="bg-green-600 text-white px-6 py-2 rounded-md font-medium hover:bg-green-700 transition"
        >
          Filtrar Período
        </button>

        {/* Seleção Visual de Métricas */}
        <div className="ml-auto flex gap-4 bg-gray-50 p-2 rounded-lg border">
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input 
              type="checkbox" 
              checked={mostrarTemperatura} 
              onChange={() => setMostrarTemperatura(!mostrarTemperatura)}
              className="accent-red-500 w-4 h-4"
            />
            <span className="text-sm font-medium text-gray-700">Temperatura</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input 
              type="checkbox" 
              checked={mostrarUmidade} 
              onChange={() => setMostrarUmidade(!mostrarUmidade)}
              className="accent-blue-500 w-4 h-4"
            />
            <span className="text-sm font-medium text-gray-700">Umidade</span>
          </label>
        </div>
      </div>

      {/* Gráfico Interativo */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-center text-lg font-bold text-gray-700 mb-4">Temperatura e Umidade - DHT22</h3>
        {carregandoDashboard ? (
          <div className="h-96 flex items-center justify-center text-gray-500">Carregando leituras do banco de dados...</div>
        ) : leituras.length === 0 ? (
          <div className="h-96 flex items-center justify-center text-gray-500">Nenhum dado encontrado para este período.</div>
        ) : (
          <div className="h-[520px] w-full pr-4">
            <ResponsiveContainer width="100%" height="100%">
              {/* Ajuste 1: Aumentado o recuo de "bottom" para 65 para dar teto às datas inclinadas */}
              <LineChart data={leituras} margin={{ top: 10, right: 10, left: 10, bottom: 65 }}>
                <CartesianGrid strokeDasharray="2 2" stroke="#ccc" />
                
                {/* Ajuste 2: Adicionado 'height={60}' para o eixo reservar espaço físico de renderização */}
                <XAxis 
                  dataKey="dataHora" 
                  tick={{ fill: '#333', fontSize: 11 }} 
                  tickMargin={12} 
                  angle={-30}
                  textAnchor="end"
                  height={60} 
                />
                
                {/* Eixo Y Esquerdo (Temperatura) */}
                {mostrarTemperatura && (
                  <YAxis 
                    yAxisId="left"
                    orientation="left"
                    domain={['auto', 'auto']}
                    tick={{ fill: '#ef4444', fontWeight: 'bold' }}
                    label={{ value: 'Temperatura (°C)', angle: -90, position: 'insideLeft', style: { fill: '#ef4444', fontWeight: 'bold' } }}
                  />
                )}

                {/* Eixo Y Direito (Umidade) */}
                {mostrarUmidade && (
                  <YAxis 
                    yAxisId="right"
                    orientation="right"
                    domain={['auto', 'auto']}
                    tick={{ fill: '#3b82f6', fontWeight: 'bold' }}
                    label={{ value: 'Umidade (%)', angle: 90, position: 'insideRight', style: { fill: '#3b82f6', fontWeight: 'bold' } }}
                  />
                )}

                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Legend verticalAlign="top" height={36}/>
                
                {mostrarTemperatura && (
                  <Line 
                    yAxisId="left"
                    type="step" 
                    dataKey="temperatura" 
                    name="Temperatura (°C)" 
                    stroke="#ef4444" 
                    strokeWidth={1.5} 
                    dot={{ r: 2.5, fill: '#ef4444' }} 
                    activeDot={{ r: 5 }} 
                  />
                )}
                
                {mostrarUmidade && (
                  <Line 
                    yAxisId="right"
                    type="monotone" 
                    dataKey="umidade" 
                    name="Umidade (%)" 
                    stroke="#3b82f6" 
                    strokeWidth={1.5} 
                    dot={{ r: 2.5, fill: '#3b82f6' }} 
                    activeDot={{ r: 5 }} 
                  />
                )}
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );

  const TelaPrevisao = () => (
    <div className="animate-fade-in bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Previsão Meteorológica Expandida (15 Dias)</h2>
        <p className="text-gray-500">Planejamento de médio prazo para operações em campo aberto.</p>
      </div>

      {carregandoPrevisao ? (
        <div className="py-20 text-center text-gray-500">Buscando modelos meteorológicos regionais...</div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {previsao.map((dia, i) => (
            <div key={i} className="border border-gray-200 rounded-lg p-4 flex flex-col items-center bg-gray-50 hover:bg-white hover:shadow-md transition">
              <span className="text-sm font-bold text-gray-600 uppercase mb-2">{dia.data}</span>
              <div className="flex gap-3 my-2">
                <span className="text-red-500 font-semibold" title="Máxima">{dia.tempMax}°</span>
                <span className="text-blue-500 font-semibold" title="Mínima">{dia.tempMin}°</span>
              </div>
              <div className="mt-2 pt-2 border-t border-gray-200 w-full text-center">
                <span className="text-xs text-gray-500 block">Prob. Chuva</span>
                <span className="text-sm font-bold text-indigo-600">{dia.chuvaProb}%</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <nav className="bg-green-800 text-white shadow-md">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex space-x-8">
            <button 
              onClick={() => setAbaAtiva('home')}
              className={`py-4 px-2 font-medium border-b-4 transition ${abaAtiva === 'home' ? 'border-green-400 text-white' : 'border-transparent text-green-200 hover:text-white'}`}
            >
              Institucional
            </button>
            <button 
              onClick={() => setAbaAtiva('dashboard')}
              className={`py-4 px-2 font-medium border-b-4 transition ${abaAtiva === 'dashboard' ? 'border-green-400 text-white' : 'border-transparent text-green-200 hover:text-white'}`}
            >
              Dashboard Histórico
            </button>
            <button 
              onClick={() => setAbaAtiva('previsao')}
              className={`py-4 px-2 font-medium border-b-4 transition ${abaAtiva === 'previsao' ? 'border-green-400 text-white' : 'border-transparent text-green-200 hover:text-white'}`}
            >
              Previsão (15 Dias)
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {abaAtiva === 'home' && <TelaHome />}
        {abaAtiva === 'dashboard' && <TelaDashboard />}
        {abaAtiva === 'previsao' && <TelaPrevisao />}
      </main>
    </div>
  );
}