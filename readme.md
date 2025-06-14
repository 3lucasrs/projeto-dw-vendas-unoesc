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

---

## 6. Como Executar o Projeto

Siga os passos abaixo para configurar o ambiente e executar o projeto em uma máquina nova.

### Pré-requisitos

- **Python 3.x:** [Download](https://www.python.org/downloads/) (Lembre-se de marcar **"Add Python to PATH"** durante a instalação).
- **PostgreSQL:** [Download](https://www.postgresql.org/download/)
- **DBeaver (ou outra ferramenta de BD):** [Download](https://dbeaver.io/download/)

### Passos para Execução

1.  **Clonar o Repositório**
    Abra um terminal e clone o projeto do GitHub:

    ```bash
    git clone https://github.com/3lucasrs/projeto-dw-vendas-unoesc.git
    cd projeto-dw-vendas-unoesc
    ```

2.  **Instalar Bibliotecas Python**
    No terminal, dentro da pasta do projeto, instale as dependências:

    ```bash
    pip install pandas sqlalchemy psycopg2-binary scikit-learn
    ```

3.  **Configurar o Banco de Dados**

    - Abra o DBeaver e conecte-se ao seu servidor PostgreSQL (use o banco de dados padrão `postgres` para a conexão inicial).
    - Execute o seguinte comando SQL para criar o banco de dados do projeto:
      ```sql
      CREATE DATABASE dw_vendas;
      ```
    - **Importante:** Desconecte e reconecte ao servidor, mas desta vez, selecione `dw_vendas` como o banco de dados.
    - Com a conexão ativa no `dw_vendas`, abra e execute o script `scripts/criar_banco.sql` para criar todas as tabelas.

4.  **Executar o Processo de ETL**

    - Abra o arquivo `scripts/processo_etl.py` em um editor de texto.
    - Na linha `db_password = 'root'`, substitua `'root'` pela senha que você configurou para o seu PostgreSQL.
    - No terminal, execute o script:
      ```bash
      python scripts/processo_etl.py
      ```
    - Aguarde a execução ser concluída.

5.  **Executar a Análise Estatística**
    - Abra o arquivo `scripts/modelo_estatistico.py`.
    - Altere a senha na linha `db_password = 'root'` para a sua senha do PostgreSQL.
    - No terminal, execute o script:
      ```bash
      python scripts/modelo_estatistico.py
      ```
    - O resultado da análise de vendas por categoria será exibido no terminal.
