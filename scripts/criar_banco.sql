-- Criar as tabelas no db dw_vendas
DROP TABLE IF EXISTS fatovendas;

DROP TABLE IF EXISTS dimtempo;

DROP TABLE IF EXISTS dimproduto;

DROP TABLE IF EXISTS dimcliente;

DROP TABLE IF EXISTS dimlocal;

CREATE TABLE
  dimproduto (
    id_produto SERIAL PRIMARY KEY,
    id_produto_original VARCHAR(50) NOT NULL UNIQUE,
    nomeproduto VARCHAR(255),
    categoria VARCHAR(100),
    subcategoria VARCHAR(100)
  );

CREATE TABLE
  dimcliente (
    id_cliente SERIAL PRIMARY KEY,
    id_cliente_original VARCHAR(50) NOT NULL UNIQUE,
    nomecliente VARCHAR(255),
    segmento VARCHAR(100)
  );

CREATE TABLE
  dimlocal (
    id_local SERIAL PRIMARY KEY,
    id_local_original VARCHAR(255) NOT NULL UNIQUE,
    cidade VARCHAR(100),
    estado VARCHAR(100),
    pais VARCHAR(100),
    regiao VARCHAR(100)
  );

CREATE TABLE
  dimtempo (
    datacompleta DATE PRIMARY KEY,
    ano INT NOT NULL,
    mes INT NOT NULL,
    dia INT NOT NULL,
    trimestre INT NOT NULL
  );

CREATE TABLE
  fatovendas (
    id_venda SERIAL PRIMARY KEY,
    id_pedido_original VARCHAR(50),
    id_data DATE REFERENCES dimtempo (datacompleta),
    id_produto INT REFERENCES dimproduto (id_produto),
    id_cliente INT REFERENCES dimcliente (id_cliente),
    id_local INT REFERENCES dimlocal (id_local),
    valorvenda DECIMAL(10, 2)
  );

SELECT
  'Tabelas do Data Warehouse criadas!' as status;