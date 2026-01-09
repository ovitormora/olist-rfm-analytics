1. O Desafio de Negócio (O Problema)
Imagine que você foi contratado como Cientista de Dados pela Olist (um grande marketplace brasileiro). O Diretor de Marketing tem um problema:

"Temos milhares de clientes na base. Atualmente, gastamos a mesma verba de marketing mandando e-mail para todos eles. Isso é ineficiente. Eu preciso saber quem são meus clientes VIPs para dar tratamento especial, e quem são os clientes que não compram há meses para tentar recuperá-los. Não sei como separar esses grupos."

A Pergunta Chave: Como podemos segmentar a base de clientes automaticamente baseando-nos em seu comportamento de compra para otimizar campanhas de marketing?

2. A Proposta de Solução (A Metodologia RFM)
Não vamos inventar a roda, vamos usar uma metodologia consagrada de Marketing Analytics chamada RFM. Vamos atribuir uma pontuação para cada cliente baseada em três pilares:

R - Recência (Recency): Há quantos dias foi a última compra do cliente?

Quanto menor o número, melhor. (Cliente "quente").

F - Frequência (Frequency): Quantas compras esse cliente já fez no total?

Quanto maior, melhor. (Cliente fiel).

M - Valor Monetário (Monetary): Quanto dinheiro esse cliente já gastou no total?

Quanto maior, melhor. (Cliente "baleia" ou alto valor).

O Produto Final: Entregaremos um Dashboard Interativo (Web App) onde o time de marketing pode ver:

Quem são os "Campeões" (Compram muito, gastam muito e compraram recentemente).

Quem são os "Em Risco" (Gastavam muito, mas sumiram).

Quem são os "Novos Clientes".

Filtros para baixar a lista de e-mails de cada grupo para campanhas.

3. Requisitos de Desenvolvimento
Para executar isso, precisaremos "costurar" várias partes do dataset da Olist.

A. A Base de Dados (Dataset)
Usaremos o Brazilian E-Commerce Public Dataset by Olist (Disponível no Kaggle). Ele é um banco de dados relacional (várias tabelas CSV que se conectam por IDs). As tabelas principais que usaremos:

olist_orders_dataset.csv: Para saber as datas (Recência).

olist_order_items_dataset.csv: Para saber preços (Monetário).

olist_customers_dataset.csv: Para identificar os usuários únicos (Frequência).

B. Tech Stack (Ferramentas)
Como você já é desenvolvedor Python/React, vamos focar em uma stack de Data Science moderna:

Linguagem: Python 3.10+.

Análise e Manipulação: Pandas (a ferramenta principal) e NumPy.

Visualização Estática: Matplotlib e Seaborn (para exploração).

Dashboard/Front-end: Streamlit.

Por que Streamlit? Ele permite criar dashboards web interativos usando apenas Python, sem precisar escrever HTML/CSS/React do zero. É o padrão ouro para portfólios de Data Science hoje.

IDE: VS Code ou Jupyter Notebook.

4. Conhecimento Técnico Necessário
Aqui estão as Hard Skills que vamos exercitar neste projeto:

Data Wrangling (Limpeza e Transformação):

A maior dificuldade será lidar com datas (datetime objects). Calcular a diferença entre "Hoje" e a "Data da Última Compra".

Joins (Merge): Precisaremos juntar a tabela de Pedidos com a de Itens e Clientes (similar ao SQL JOIN).

Estatística Descritiva e Quartis:

Como decidimos o que é uma Recência "boa"? Usaremos quartis (qcut). Vamos dividir os clientes em 4 grupos (notas de 1 a 5) baseados na distribuição dos dados.

Lógica de Negócios:

Criar regras condicionais. Ex: Se (R=5 e F=5), então Cliente = 'Campeão'.

Storytelling de Dados:

Não basta gerar números. Precisamos criar gráficos que expliquem por que aquele segmento é importante.

5. O Diferencial ("A Cereja do Bolo")
Para tornar seu portfólio de Nível Pleno/Sênior, podemos adicionar uma camada extra:

Clusterização com K-Means (Machine Learning): Além de fazer a regra manual (quartis), podemos rodar um algoritmo não supervisionado para deixar a IA encontrar os grupos de clientes sozinha e comparar os resultados.

olist-rfm-analytics/
├── data/
│   ├── raw/          <-- Aqui você vai colocar os arquivos .csv baixados do Kaggle
│   └── processed/    <-- Aqui salvaremos os dados limpos depois
├── notebooks/        <-- Para testes e exploração (Jupyter Notebooks)
├── src/              <-- Código fonte estruturado (funções Python)
├── app.py            <-- Será nosso arquivo principal do Dashboard (Streamlit)
├── requirements.txt  <-- Lista de bibliotecas
└── README.md         <-- Documentação do projeto