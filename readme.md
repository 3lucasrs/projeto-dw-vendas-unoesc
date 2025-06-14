# Projeto Final: Data Warehouse e Análise de Vendas

## 1. Visão Geral do Projeto

Este projeto, desenvolvido como atividade avaliativa, demonstra o ciclo completo de uma solução de dados, desde a coleta até a análise. O objetivo foi construir um **Data Warehouse** centralizado utilizando **PostgreSQL**, desenvolver um processo de **ETL (Extração, Transformação e Carga)** com **Python** para alimentar o DW e, por fim, aplicar uma **análise estatística** para extrair insights de negócio a partir dos dados consolidados.

**Tecnologias Utilizadas:**

- **Linguagem de Programação:** Python
- **Bibliotecas:** Pandas, SQLAlchemy, Psycopg2
- **Sistema de Banco de Dados:** PostgreSQL
- **Ferramenta de Gestão:** DBeaver

---

## 2. Base de Dados (Dataset)

A base de dados escolhida foi a **"Superstore Sales Dataset"**, um conjunto de dados público que simula transações de vendas de uma rede de lojas. Este dataset foi selecionado por conter as dimensões essenciais para a modelagem de um Data Warehouse, como informações de produtos, clientes e localização das vendas.

- **Fonte do Dataset:** [Kaggle - Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)

---

## 3. Criação do Data Warehouse

O Data Warehouse foi projetado com um **esquema estrela (Star Schema)**, uma arquitetura otimizada para consultas analíticas rápidas. O esquema é composto pelas seguintes tabelas:

#### Tabelas de Dimensão:

- `dimproduto`: Armazena os atributos descritivos dos produtos (nome, categoria, subcategoria).
- `dimcliente`: Contém os dados dos clientes (nome, segmento).
- `dimlocal`: Guarda as informações geográficas das vendas (cidade, estado, região).
- `dimtempo`: Consolida os atributos de data (ano, mês, dia, trimestre).

#### Tabela Fato:

- `fatovendas`: É a tabela central que armazena as métricas quantitativas do negócio (neste caso, `valorvenda`) e se conecta a todas as tabelas de dimensão através de chaves estrangeiras.

---

## 4. Processo de ETL

Um script Python (`processo_etl.py`) foi desenvolvido para automatizar a extração, transformação e carga dos dados. O processo funciona da seguinte forma:

1.  **Extração:** Os dados são lidos do arquivo `superstore_sales.csv`.
2.  **Transformação:**
    - Os nomes das colunas são padronizados para facilitar a manipulação.
    - Os dados são limpos, removendo espaços em branco desnecessários.
    - As informações para cada dimensão são isoladas e as duplicatas são removidas.
3.  **Carga:**
    - O script se conecta ao Data Warehouse no PostgreSQL.
    - Para cada tabela de dimensão, ele verifica quais registros já existem e insere apenas os novos, o que torna o processo **idempotente** (pode ser executado várias vezes sem gerar erros ou duplicatas).
    - A tabela `fatovendas` é totalmente limpa e recarregada a cada execução para garantir a consistência dos dados, relacionando as vendas com as chaves corretas das tabelas de dimensão.

---

## 5. Modelo Estatístico e Resultados

O escopo inicial previa um modelo de regressão, mas o dataset utilizado não continha as variáveis preditoras necessárias (como `lucro`, `quantidade` ou `desconto`). Assim, o projeto foi adaptado para realizar uma **análise estatística descritiva**, um pilar fundamental de qualquer projeto de dados.

O script `modelo_estatistico.py` realiza uma consulta no Data Warehouse, unindo a tabela de fatos com a dimensão de produtos para agregar os dados.

#### Resultado Alcançado:

A análise calculou o total de vendas por categoria de produto, fornecendo um insight claro sobre o desempenho de cada uma. Os resultados foram os seguintes:

| Categoria           | Total de Vendas |
| ------------------- | --------------- |
| **Technology**      | R$ 827.455,94   |
| **Furniture**       | R$ 728.658,75   |
| **Office Supplies** | R$ 705.422,28   |

Essa análise simples, porém poderosa, demonstra o valor do Data Warehouse ao permitir que perguntas de negócio sejam respondidas de forma rápida e precisa.
