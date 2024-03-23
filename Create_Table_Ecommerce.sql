/* Tabela de criacao do usuario, no postgre não se pode criar um so com User,
   aí inseri como UserTable */

CREATE TABLE UserTable (
    ID_User SERIAL PRIMARY KEY,
    nome VARCHAR(255),
    email VARCHAR(255),
    senha VARCHAR(255),
    telefone BIGINT
);

/* Tabela de criacao do endereco */
CREATE TABLE User_Endereco (
    ID_User_Endereco SERIAL PRIMARY KEY,
    ID_User INT REFERENCES UserTable(ID_User),
    numero INT,
    complemento VARCHAR(255),
    cep VARCHAR(10),
    cidade VARCHAR(255)
);

/* Tabela de criacao da marca do produto */
CREATE TABLE Produto_Marca (
   ID_Produto_Marca SERIAL PRIMARY KEY,
   nome VARCHAR(255)
);

/* Tabela de criacao da categoria do produto */
CREATE TABLE Produto_Categoria (
  ID_Produto_Categoria SERIAL PRIMARY KEY,
  nome VARCHAR (255)
);

/* Tabela de criacao do produto */
CREATE TABLE Produto (
   ID_Produto SERIAL PRIMARY KEY,
   ID_Marca INT REFERENCES Produto_Marca(ID_Produto_Marca),
   ID_Categoria INT REFERENCES Produto_Categoria(ID_Produto_Categoria), 
   nome_produto VARCHAR(255),
   descricao TEXT,
   valor DECIMAL,
   desconto DECIMAL
);

/* Tabela de criacao do pedido */
CREATE TABLE Pedido (
  ID_Pedido SERIAL PRIMARY KEY, 
  ID_User INT REFERENCES UserTable(ID_User), 
  data_compra TIMESTAMP, 
  status VARCHAR (50)
);

/* Tabela de criacao do carrinho */
CREATE TABLE Produtos_Pedido (
  ID_Produtos_Pedido SERIAL PRIMARY KEY, 
  ID_Pedido INT REFERENCES Pedido(ID_Pedido), 
  quantidade INT, 
  valor_compra DECIMAL
); 

/* Tabela de criacao do pagamento */
CREATE TABLE User_Pagamento(
	ID_User_Pagamento SERIAL PRIMARY KEY,	
	ID_Pedido INT REFERENCES Pedido(ID_Pedido),	
	tipo_pagamento	VARCHAR (50),	
	prazo	DATE
);	

/* Tabela de criacao do estoque do produto */
CREATE TABLE Produto_Estoque(
	ID_Produto_Estoque	SERIAL	PRIMARY	KEY,	
	ID_Produto	INT	REFERENCES	Produto(ID_Produto),	
	quantidade	INT,	
	data_cadastro	TIMESTAMP,	
	modificado_em	TIMESTAMP
);
