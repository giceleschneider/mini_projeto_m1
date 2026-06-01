# Mini Projeto de Processamento de Dados Olist

## Visão Geral
Este projeto faz o processamento de dados de produtos e ordens do Olist, realizando validações e tratamentos em registros CSV.

## Processamento de Dados
O projeto realiza os seguintes tratamentos:

- **Tratamento de Categorias**: Preenche categorias vazias com "sem categoria", converte para minúsculas e remove caracteres especiais e espaços vazios no começo e no fim das categorias.
- **Verificação de Entregas**: Analisa a relação entre datas de entrega vazias e cancelamentos, calculando percentuais, que possibilitam uma visão de negócios para tomadas de decisões e tratativas.
- **Conversão de Datas**: Converte datas de aprovação para o formato PT-BR (dd/mm/aaaa).
- **Tratamento de Dimensões**: Preenche dimensões vazias (comprimento, altura, largura e peso) com a média da categoria. Produtos sem dados de categoria são removidos

### Reflexão Teórica sobre Machine Learning
A limpeza e preparação correta dos dados é fundamental para o desenvolvimento de modelos de Inteligência Artificial robustos e confiáveis. Quando aplicamos uma lógica de programação rigorosa na remoção de valores ausentes, normalização de formatos e tratamento de outliers, garantimos que o modelo treine sobre dados de qualidade, reduzindo significativamente o risco de overfitting. Além disso, a limpeza deliberada de dados diminui vieses introduzidos por registros inconsistentes ou mal preenchidos, que poderiam levar a predições enviesadas e injustas.

## Requisitos
- Python 3.14

## Bibliotecas Utilizadas
O projeto utiliza apenas bibliotecas da biblioteca padrão do Python:
- `csv`
- `re`
- `datetime`

## Estrutura do Projeto
Arquitetura do projeto considerando os arquivos principais e a pasta de dados:

- `main.py`
  - Ponto de entrada do projeto.
  - Importa funções de processamento de `funcoes.py`.
  - Carrega arquivos CSV em `./data/`.
  - Executa relatórios e tratamentos de dados.

- `funcoes.py`
  - Contém todas as funções de leitura e tratamento de dados.
  - Funções principais:
    - `importador_csv(nome_arquivo)`
    - `relatorio_produto_categoria_sem_tratamento(lista_produtos)`
    - `tratamento_categoria_produto(lista_produtos)`
    - `verifica_relacao_data_entrega_e_cancelamentos(lista_ordens)`
    - `tratativa_data_para_ptbr(lista_ordens)`
    - `tratativa_dimensoes_produto(lista_produtos)`

- `data/`
  - Contém os datasets utilizados pelo projeto.
  - Arquivos usados:
    - `olist_products_dataset.csv`
    - `olist_orders_dataset.csv`

## Como Executar
1. Abra um terminal na pasta do projeto.
2. Execute o comando:

```bash
python main.py
```

3. O script irá carregar os arquivos CSV a partir de `./data/` e imprimir relatórios e contagens de processamento no terminal.
