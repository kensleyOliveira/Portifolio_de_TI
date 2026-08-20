# ATIVIDADE: ARQUITETURA (2)

## Questão 3: Análise de Projeto Anterior

**Projeto de Referência:** Sistema de Gestão de Vendas (E-commerce).

* **Estilo/Padrão Utilizado:**
O projeto utilizou uma **Arquitetura Monolítica** baseada no padrão **MVC (Model-View-Controller)**. Toda a lógica de negócio, autenticação e acesso ao banco de dados residia em um único repositório e era implantada como uma única unidade.
* **Dificuldades Encontradas:**
1. **Manutenção:** À medida que o código crescia, as dependências ficavam "entrelaçadas" (alto acoplamento). Alterar uma regra de cálculo de frete acabava afetando, de forma inesperada, o módulo de estoque.
2. **Escalabilidade:** Para lidar com picos de tráfego na Black Friday, era necessário escalar o monólito inteiro, consumindo recursos de servidor para módulos que nem estavam sendo usados intensamente.
3. **Deploy:** O tempo de build e teste era muito longo. Um erro pequeno em uma interface visual impedia o deploy de correções críticas no backend.

---

## Questão 4: Proposta de Melhoria

Para melhorar o projeto analisado, a evolução natural seria a migração para uma **Arquitetura de Microsserviços** ou a aplicação de **Clean Architecture**.

* **Estilos/Padrões Propostos:**
1. **Microsserviços:** Decompor o monólito em serviços independentes (Ex: Serviço de Catálogo, Serviço de Pagamento, Serviço de Entrega).
2. **Arquitetura Baseada em Eventos (Event-Driven):** Utilizar um *Message Broker* (como RabbitMQ ou Kafka) para comunicação assíncrona.


* **Explicação da Melhoria:**
* **Isolamento de Falhas:** Se o serviço de recomendações cair, o usuário ainda consegue finalizar a compra. No modelo anterior, um erro em qualquer parte poderia derrubar o sistema todo.
* **Escalabilidade Granular:** Poderíamos escalar apenas o serviço de "Pagamento" durante períodos de alta demanda, economizando custos de infraestrutura.
* **Independência de Tecnologia:** Permitiria que a equipe usasse tecnologias diferentes para problemas diferentes (ex: Python para análise de dados e Node.js para o checkout de alta performance).



---

