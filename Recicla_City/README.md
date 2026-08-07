
# RELATÓRIO TÉCNICO - MISSÃO 2

## **Recicla City: Missão Limpeza**

### **GAME DESIGN DOCUMENT (GDD) — VERSÃO HTML5**

* **Guilda:** Mestres da Gambiarra


* **Integrantes da Guilda:** Kensley Alves de Oliveira, Pedro Paulo Cunha, Tatiana Thomaz, Otávio


* **Disciplina:** Introdução ao Desenvolvimento de Jogos


* **Tecnologia Base:** HTML5, CSS3, JavaScript Nativo (ES6+), Canvas 2D e Web Audio API


* **Plataformas-Alvo:** Web (PC/Mobile) e Dispositivos Móveis via Navegador


* **Data:** Julho de 2026

* **Link:** https://recicla-city-missao-limpeza.vercel.app/

---

## **A. Visão Geral e Metas de Experiência**

### **Resumo do Jogo**

*Recicla City: Missão Limpeza* é um jogo educativo casual de exploração isométrica e gerenciamento de tempo voltado ao público infanto-juvenil. Desenvolvido nativamente em **HTML5, CSS e JavaScript (Canvas 2D)**, o título utiliza arte digital estilizada renderizada em perspectiva isométrica bidimensional com traços *cartoon* para estabelecer uma atmosfera visualmente atraente, lúdica e extremamente leve, capaz de rodar diretamente no navegador de aparelhos móveis e PCs de entrada sem necessidade de instalação.

O núcleo da jogabilidade (*core loop*) consiste em explorar cenários urbanos e naturais poluídos em busca de detritos espalhados, coletá-los por aproximação espacial automática através de comandos de clique/toque ou direcionais (WASD/Setas), gerenciar o limite físico de armazenamento da mochila e retornar aos Postos de Reciclagem para realizar a triagem seletiva correta sob a pressão de um cronômetro regressivo. O jogo divide-se em **4 fases progressivas**, cuja vitória definitiva exige a coleta e separação de 100% dos resíduos da localidade.

### **Logline / Frase de Efeito (The Hook)**

"Corra contra o tempo para limpar as ruas, dominar a arte da reciclagem e transformar cidades poluídas em paraísos ecológicos vibrantes antes que o cronômetro zere!"

### **Plataforma-Alvo e Tecnologia Base**

O jogo foi arquitetado para abranger a Web em plataformas Mobile e PC. A escolha do ecossistema nativo do navegador (**HTML5 Canvas e Web Audio API**) fundamenta-se na portabilidade absoluta e na eliminação de barreiras de instalação. O projeto implementa uma **Arquitetura Orientada a Objetos com um Loop de Jogo Central (`requestAnimationFrame`)**, desacoplada através de um **Padrão de Emissão de Eventos Personalizados (Event Emitter)** em JavaScript. Essa abordagem mitiga gargalos de processamento em CPUs móveis de baixo custo, garantindo uma taxa de quadros estável (60 FPS) e alta responsividade tanto para interações de toque (*touch events*) quanto de mouse/teclado.

### **Meta de Experiência e Alinhamento com a Teoria do Fluxo**

Em consonância com a literatura de Game Design (Fullerton, Cap. 11), a meta de experiência prioritária é instigar um sentimento de "urgência recompensadora". O sistema equilibra dinamicamente as habilidades do público infanto-juvenil com o desafio computacional para sustentá-lo no canal de fluxo (Csikszentmihalyi), mitigando o tédio e a ansiedade através de mecânicas de oposição e feedbacks cinestésicos:

* **Vetor de Tensão (Ansiedade):** Alimentado pela contagem regressiva linear do cronômetro da fase e pela restrição rígida da mochila (capacidade inicial de 10 resíduos, expansível na fase 3). Conforme o estoque se esgota e o tempo decresce, o jogador enfrenta um estresse positivo (*eustress*), impulsionando a otimização de rotas geográficas no mapa.


* **Vetor de Alívio (Relaxamento e Dopamina):** Contrapõe-se à urgência temporal através de uma atmosfera acústica serena baseada em síntese de áudio e loops musicais sintetizados via *Web Audio API*. Os feedbacks cinestésicos adicionais — efeitos sonoros agudos de "pop" na coleta e o carrilhão cristalino ao segregar os resíduos nas lixeiras corretas — geram uma liberação constante de dopamina.


* **Equilíbrio pelo Feedback de Revitalização:** O elo de estabilização do fluxo é a transformação do cenário em tempo real. À medida que o lixo é limpo, o Canvas renderiza dinamicamente a transição dos biomas: a praia, por exemplo, muda de tons cinzentos e mortos para uma areia amarela vibrante e água azul límpida, fazendo brotar árvores e flores.



---

## **B. Narrativa e Contexto (Storytelling Avançado)**

### **Premissa Dramática**

O universo de *Recicla City* é ambientado em um ecossistema outrora próspero que sofreu um colapso socioambiental devido ao descarte negligente de resíduos. Cidades, parques e praias foram sufocados sob camadas de detritos, fazendo com que o ambiente perdesse sua vivacidade cromática, assumindo uma tonalidade acinzentada e estéril. O jogador assume o papel do **Herói Ecológico**, equipado com a *Mochila Eco-G*, cuja missão é provar que a triagem correta dos materiais e a ação imediata podem reverter fisicamente a degradação do planeta.

### **Jornada do Usuário (Arco Narrativo em 4 Fases)**

A estrutura do arco de progressão narrativa está organicamente entrelaçada à dificuldade crescente das fases do jogo:

* **Fase 1 - Praça Escola (Tutorial e Fundamentos):** O Herói depara-se com o primeiro foco de poluição escolar. Introduz as regras básicas de movimento e a segregação de 3 categorias iniciais (Papel, Metal/Latas e Plástico) com 12 resíduos totais no cenário.


* **Fase 2 - Parque Central (Complexidade Média):** A poluição se alastra para áreas verdes densas, introduzindo a categoria Vidro (totalizando as 4 categorias clássicas). Introduz a mecânica de bônus de aceleração e obstáculos como bancos e flores.


* **Fase 3 - Cidade Ventosa (Desafio Climático):** O cenário urbano traz o Vento Dinâmico, que arrasta folhas de papel e garrafas plásticas pelo mapa. O jogador recebe uma Mochila Expansível para lidar com a movimentação dos 18 resíduos sob cones e barreiras urbanas.


* **Fase 4 - Praia Limpa (O Clímax):** O desafio final ocorre no litoral, enfrentando a dinâmica de correntezas na água. O jogador precisa coletar 20 resíduos sob forte pressão de tempo, e vencê-la restaura as cores definitivas (areia amarela e água azul) de todo o bioma regional.



### **Contexto do Mundo Lúdico e Integração**

A narrativa expressa o seu estado de saúde sistêmico por meio de indicadores visuais diretos renderizados no Canvas. Se o jogador erra a lixeira ou negligencia o lixo, a saturação cromática do cenário cai; se joga com precisão pedagógica, o sol brilha, o bioma ganha flores e árvores, e a Web Audio API expande as trilhas e ritmos sonoros das fases.

---

## **C. Mecânicas e Mecanismos do Sistema**

### **Decomposição de Objetos do Sistema**

O ecossistema de dados em JavaScript é composto por quatro instâncias e classes principais:

1. **Jogador (`HeroEco`):** O agente ativo controlado pelo teclado, mouse ou botões de toque, contendo as coordenadas espaciais e o estado da mochila.


2. **Detrito (`TrashItem`):** Objeto passivo posicionado em coordenadas do mapa contendo um identificador string da sua categoria (ex: `'Papel'`, `'Plastico'`).


3. **Posto de Reciclagem (`RecycleBin`):** Estruturas com caixas de colisão fixas que validam logicamente se o material depositado confere com o tipo aceito.


4. **Gerenciador de Tempo (`TimeManager`):** Controlador global baseado no tempo decorrido do loop que monitora a contagem regressiva e aplica as penalidades ou bônus.



### **Atributos e Propriedades do Sistema (Dicionário de Variáveis JS)**

| Objeto | Atributo Técnico | Tipo de Dado | Domínio / Restrição | Descrição Semântica |
| --- | --- | --- | --- | --- |
| `HeroEco` | `x`, `y` | `Number` | Limites da matriz do mapa | Posição no plano de renderização isométrica. |
| `HeroEco` | `mochilaInventario` | `Array` | Max: 10 itens (Fases 1,2,4) ou 15 (Fase 3) | Lista que armazena os tipos de materiais coletados. |
| `HeroEco` | `quantidadeAtual` | `Number` | 0 a capacidade máxima | Contagem de detritos armazenados no momento. |
| `HeroEco` | `pontuacaoTotal` | `Number` | 0 a $\infty$ | Score acumulado do jogador no nível. |
| `HeroEco` | `multiplicadorCombo` | `Number` | 1 a 5 | Fator multiplicador para acertos seguidos nas lixeiras. |
| `TrashItem` | `tipoMaterial` | `String` | `'Papel'`, `'Plastico'`, `'Vidro'`, `'Metal'` | Categoria do resíduo para validação. |
| `RecycleBin` | `tipoAceito` | `String` | `'Papel'`, `'Plastico'`, `'Vidro'`, `'Metal'` | Filtro lógico da lixeira correspondente. |
| `TimeManager` | `tempoRestante` | `Number` | 0.0 a tempo inicial da fase | Segundos restantes em contagem decrescente linear. |

### **Comportamentos e Regras Formais (Loop de Controle em JavaScript)**

#### **Algoritmo de Coleta por Aproximação Espacial:**

Dentro da função de atualização executada a cada frame do jogo, o sistema calcula a distância euclidiana entre o jogador e os resíduos ativos:

```javascript
function verificarColeta(hero, listaDetritos) {
    listaDetritos.forEach((detrito, index) => {
        // Cálculo de distância euclidiana no plano do Canvas
        let dist = Math.sqrt(Math.pow(hero.x - detrito.x, 2) + Math.pow(hero.y - detrito.y, 2));
        
        if (dist <= 40) { // Raio de aproximação física em pixels
            if (hero.quantidadeAtual < hero.capacidadeMaximaMochila) {
                hero.mochilaInventario.push(detrito.tipoMaterial);
                hero.quantidadeAtual++;
                listaDetritos.splice(index, 1); // Remove o detrito do mapa
                
                EventManager.emit('mochila_alterada', hero);
                AudioManager.playSFX('pop_coleta');
            } else {
                EventManager.emit('alerta_hud', 'Mochila Cheia! Vá até a Base!');
                AudioManager.playSFX('erro_mochila_cheia');
            }
        }
    });
}

```

#### **Algoritmo de Depósito e Validação Seletiva Pedagógica:**

Quando o jogador colide com uma lixeira e interage (via clique de mouse, toque ou aproximação), a mochila é processada sequencialmente:

```javascript
function processarDescarte(hero, lixeira) {
    while (hero.mochilaInventario.length > 0) {
        let item = hero.mochilaInventario.pop(); // Estrutura LIFO / Remoção do último coletado
        
        if (item === lixeira.tipoAceito) {
            // Depósito Correto: Concede pontos, tempo e combo
            hero.pontuacaoTotal += 100 * hero.multiplicadorCombo;
            TimeManager.tempoRestante = Math.min(TimeManager.tempoMaximo, TimeManager.tempoRestante + 5);
            hero.multiplicadorCombo = Math.min(5, hero.multiplicadorCombo + 1);
            
            RenderEngine.dispararParticulasRevitalizacao(lixeira.x, lixeira.y);
            AudioManager.playSFX('carrilhao_acerto');
        } else {
            // Depósito Incorreto: Quebra o combo e penaliza o tempo restante
            TimeManager.tempoRestante = Math.max(0, TimeManager.tempoRestante - 8);
            hero.multiplicadorCombo = 1;
            
            AudioManager.playSFX('som_grave_erro');
        }
    }
    hero.quantidadeAtual = 0;
    EventManager.emit('mochila_alterada', hero);
    EventManager.emit('score_atualizado', hero);
}

```

### **Condições de Fim de Jogo (Vitória e Derrota)**

* **Condição de Vitória:** Avaliada quando o comprimento do array contendo os resíduos ativos do mapa torna-se igual a zero (`listaDetritos.length === 0`), contanto que `TimeManager.tempoRestante > 0`. O loop congela, computa as estrelas com base no tempo economizado e exibe a tela de vitória sobre o mapa totalmente florido e colorido.


* **Condição de Derrota (Game Over):** Disparada assim que `TimeManager.tempoRestante <= 0`. O ciclo de jogabilidade é interrompido, os controles do jogador são congelados, o Canvas aplica um filtro global de escala de cinza e a tela de derrota oferece o botão de reiniciar junto a uma dica ecológica.



---

## **D. Anatomia da Interface e Fluxo Visual (Storyboard)**

### **Fluxograma de Sequência de Telas**

A arquitetura de telas é gerenciada por manipulação direta de contêineres e visibilidade no DOM (Document Object Model) através do CSS, garantindo transições instantâneas:

```
[ TELA DE MENU ] ──(Toque em Iniciar)──> [ SELEÇÃO DE FASES ] ──(Escolha)──> [ TUTORIAL ILUSTRADO ]
                                                                                   │
                                                                           (Iniciar Nível)
                                                                                   ▼
[ TELA DE DERROTA ] <──(Tempo Esgotado)─── [ CORE GAMEPLAY CANVAS ] <─────── [ CORE LOOP ]
(Botão Reiniciar / Dica Eco)                    │
                                           (Limpeza 100%)
                                                ▼
                                        [ TELA DE VITÓRIA ] ──> (Libera Fase Seguinte)

```

### **Mapeamento do HUD (Responsivo - Mobile/PC)**

O HUD é sobreposto ao elemento `<canvas>` utilizando elementos HTML semânticos estruturados em uma camada superior gerenciada por CSS flexbox/grid para garantir legibilidade:

* **Canto Superior Esquerdo - Painel do Cronômetro:** Um display numérico digital alimentado por uma barra de progresso em formato de arco CSS (`concentric-gradient`). A barra adota uma coloração reativa: Verde acima de 30 segundos, Amarelo entre 11 e 30 segundos, e Vermelho piscante nos 10 segundos finais, sincronizado com o compasso acústico acelerado do áudio.


* **Canto Superior Direito - Placar e Combo:** Renderiza a pontuação atual em texto ampliado com fontes sem serifa de alta legibilidade. O indicador de combo (ex: `"Combo 5x!"`) surge dinamicamente através de animações CSS de pulsação e escala.


* **Canto Inferior Central - Slots da Mochila (Inventário):** Uma linha horizontal contendo de 10 a 15 caixas quadradas (`<div>` estilizadas). Conforme os detritos são inseridos, imagens em miniatura do resíduo preenchem os blocos sequencialmente. Ao atingir a capacidade máxima, uma animação de vibração visual e a mensagem `"Mochila Cheia!"` alertam o usuário.



### **Feedback Sinestésico, Dinâmico e Diegético**

A renderização gráfica no Canvas simula a revitalização através do gerenciamento de opacidade de texturas sobrepostas. Cada quadrante limpo decresce a transparência da camada poluída acinzentada, revelando de forma fluida a camada inferior com cores quentes e elementos naturais nativos gerados proceduralmente (como grama e flores). O feedback tátil para dispositivos móveis é simulado através da API de Vibração do Navegador (`navigator.vibrate(15)`), gerando um pulso sutil ao coletar lixos por proximidade.

---

## **E. Arquitetura Tecnológica e de Dados**

### **Estrutura de Classes e Módulos do Código JavaScript (ES6)**

A fim de manter o código limpo, de alta performance e modularizado sem as amarras de uma engine pesada, o projeto divide-se em classes independentes orientadas a objetos:

```
[ index.html / main.js ] (Ponto de entrada do script e inicialização do Canvas)
   │
   ├── [ classes / GameLoop.js ] (Controlador central do requestAnimationFrame)
   ├── [ classes / InputHandler.js ] (Captura Keyboard WASD/Setas, Mouse Click e Touch Events)
   ├── [ classes / Vector2.js ] (Estrutura matemática para gerenciamento de coordenadas)
   ├── [ classes / EntityManager.js ] (Instancia, gerencia e desenha Player, TrashItems e Bins)
   │      ├── Player.js (Classe do Herói, lógica da mochila array push/pop)
   │      ├── TrashItem.js (Classe dos resíduos espalhados no Canvas)
   │      └── RecycleBin.js (Classe das lixeiras e caixas de colisão de triagem)
   ├── [ services / AudioManager.js ] (Web Audio API - Sintetizadores de osciladores para SFX/BGM)
   ├── [ services / LevelManager.js ] (Dados de calibração, tempo e resíduos das 4 fases)
   └── [ services / EventManager.js ] (Emissor de eventos customizados pub/sub para desacoplamento)

```

### **Comunicação Desacoplada por Eventos Customizados**

Para evitar dependências cruzadas entre classes (acoplamento rígido), a arquitetura utiliza o padrão *Publish-Subscribe* através de um objeto global `EventManager`.

Quando o `InputHandler` detecta comandos direcionais, ele apenas altera os vetores de velocidade do `Player`. Quando uma colisão de descarte ocorre, a classe `RecycleBin` dispara um evento: `EventManager.emit('item_reciclado', { correto: true, tipo: 'Vidro' })`. O `LevelManager` escuta esse sinal para computar o progresso da fase; o `AudioManager` altera imediatamente a frequência do oscilador para gerar o som de acerto; e o módulo de renderização dispara o efeito visual de revitalização das flores. Isso permite a substituição ou modificação completa de partes visuais ou sonoras sem quebrar as regras de programação lógica da física ou lógica de dados do jogo.

---

## **F. Cronograma de Produção (Backlog de 30 Dias Atualizado)**

### **Divisão de Papéis da Guilda**

* **Ferreiro / Alquimista (Kensley Alves de Oliveira):** Arquitetura estrutural de software orientada a objetos em JS, codificação da máquina de estados do Loop principal, implementação das matrizes lógicas e de colisão no Canvas 2D, e desenvolvimento do sistema de inventário array (push/pop).


* **Mago / Bardo (Pedro Paulo Cunha e Tatiana):** Design de interface IHC e estilização do HUD responsivo em HTML/CSS, exportação e otimização das folhas de *sprites* isométricas cartoon, codificação dos sintetizadores de ondas na Web Audio API para música e efeitos sonoros.


* **Patrulheiro / Clérigo (Thomaz Otávio e suporte de toda a guilda):** Game Design de fases, balanceamento das fórmulas matemáticas de aceleração, vento, correnteza e modo assistência adaptativo, playtesting de navegadores e relatórios de QA.



### **Entregáveis Semanais do Cronograma**

| Fase | Foco Estratégico | Responsável Técnico | Tarefas Detalhadas do Backlog (Prontas para Execução) |
| --- | --- | --- | --- |
| **Semana 1** | Protótipo Base e Loop JS | Ferreiro / Alquimista | Criação do repositório Git, inicialização do esqueleto HTML5/CSS e implementação do loop principal estável em `requestAnimationFrame` a 60 FPS. |
|  |  | Mago / Bardo | Criação do protótipo estático do HUD responsivo em CSS Grid/Flexbox e validação de legibilidade em telas móveis. |
|  |  | Patrulheiro / Clérigo | Levantamento do mapeamento da matriz de coordenadas e balanceamento inicial de resíduos por fase. |
| **Semana 2** | Movimentação e Inventário | Ferreiro / Alquimista | Codificação do `InputHandler` (WASD, Setas, Clicks de Mouse e botões Touch) e desenvolvimento da lógica Array para a mochila Eco-G. |
|  |  | Mago / Bardo | Renderização e cálculo do posicionamento isométrico (conversão de coordenadas Cartesianas X/Y para Isométricas IsoX/IsoY) no Canvas. |
|  |  | Patrulheiro / Clérigo | Condução de testes de estresse (*Smoke Tests*) para garantir que o limite de slots bloqueia firmemente novas coletas automáticas. |
| **Semana 3** | Integração Áudio e Mecânicas | Mago / Bardo | Programação dos nós de osciladores e ganho na Web Audio API para reproduzir o som dinâmico de vento, aceleração e batimentos. |
|  |  | Ferreiro / Alquimista | Integração do algoritmo das mecânicas especiais (Vento na fase 3, Correnteza na fase 4 e Mochila Expansível). |
|  |  | Patrulheiro / Clérigo | Configuração das caixas de diálogo dos tutoriais ilustrados que surgem antes do início de cada nível. |
| **Semana 4** | Calibração, QA e Deploy | Toda a Guilda | Execução das rotinas de testes e QA entre múltiplos navegadores desktop e móveis (Chrome, Safari, Edge e Firefox). |
|  |  | Patrulheiro / Clérigo | Ajuste fino das variáveis do Facilitador Adaptativo (Modo Assistência ativado após 2 derrotas, concedendo +35% de tempo e menos lixo). |
|  |  | Ferreiro / Alquimista | Otimização do arquivo final consolidado (HTML/CSS/JS integrados), empacotamento do ZIP estável e publicação em ambiente de nuvem de acesso público (GitHub Pages). |

---

## **G. Configuração e Calibração Atual das Fases**

* **Fase 1 - Praça Escola:** Tempo: 170s | 12 Resíduos | Categorias: Papel, Metal, Plástico.


* **Fase 2 - Parque Central:** Tempo: 190s | 14 Resíduos | Categorias: 4 Categorias Clássicas (introduz Vidro) + Obstáculos e Aceleração.


* **Fase 3 - Cidade Ventosa:** Tempo: 185s | 18 Resíduos | Mecânicas: Vento Dinâmico (itens móveis), Cones e Mochila Extensível (15 slots).


* **Fase 4 - Praia Limpa:** Tempo: 135s | 20 Resíduos | Mecânicas: Areia, Água com Correnteza Física e Revitalização Amarela/Azul Completa.



> 💡 **Facilitador Adaptativo Habilitado:** Se o jogador falhar duas vezes consecutivas, a terceira tentativa iniciará o Modo Assistência: +35% de tempo disponível, mochila ampliada de largada, redução de 4 detritos na meta e remoção de colisões de obstáculos complexos do cenário.
 
 

---

## **Apêndice: Transparência e Uso de IA Generativa**

| ID | Prompt Fornecido pela Guilda (Input) | Resposta do Modelo Utilizado (Output Adaptado) | Finalidade e Aplicação no GDD |
| --- | --- | --- | --- |
| **01** | "Como migrar uma arquitetura desacoplada de nós e sinais da Godot 4 para JavaScript puro rodando em uma aplicação web com Canvas 2D?" | Forneceu o design pattern de um EventEmitter nativo em JavaScript ES6 e a lógica de substituição do loop físico da engine por rotinas baseadas em `requestAnimationFrame`. | Utilizado como fundação de engenharia para reestruturar as seções C.3 e E.2 após a mudança tecnológica do projeto. |
| **02** | "Forneça formas eficientes de simular colisão e aproximação de itens em mapas isométricos 2D renderizados via matriz no Canvas HTML5." | Detalhou a equação de distância euclidiana adaptada para eixos isométricos transformados em pixels com o método de remoção por índice através de `splice()`. | Aplicado na documentação dos comportamentos lógicos e no algoritmo de coleta espacial descritos na seção C.3 do documento. |