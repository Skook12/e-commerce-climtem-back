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
CREATE TABLE User_Address (
    ID_User_Address SERIAL PRIMARY KEY,
    ID_User INT REFERENCES UserTable(ID_User),
    numero INT,
    complemento VARCHAR(255),
    cep VARCHAR(10),
    cidade VARCHAR(255)
);

/* Tabela de criacao da marca do produto */
CREATE TABLE Brand (
   brand_id SERIAL PRIMARY KEY,
   name VARCHAR(255)
);

/* Tabela de criacao da categoria do produto */
CREATE TABLE Category (
  category_id SERIAL PRIMARY KEY,
  name VARCHAR (255)
);

/* Tabela de criacao do produto */
CREATE TABLE Product (
   ID_Product SERIAL PRIMARY KEY,
   ID_Brand INT REFERENCES Brand(brand_id),
   ID_Category INT REFERENCES Category(category_id), 
   nome_produto VARCHAR(255),
   descricao TEXT,
   valor DECIMAL,
   desconto DECIMAL
);

/* Tabela de criacao do pedido */
CREATE TABLE Order (
  ID_Order SERIAL PRIMARY KEY, 
  ID_User INT REFERENCES UserTable(ID_User), 
  data_compra TIMESTAMP, 
  status VARCHAR (50)
);

/* Tabela de criacao do carrinho */
CREATE TABLE Products_Order (
  ID_Products_Order SERIAL PRIMARY KEY, 
  ID_Order INT REFERENCES Order(ID_Order), 
  quantidade INT, 
  valor_compra DECIMAL
); 

/* Tabela de criacao do pagamento */
CREATE TABLE User_Pagamento(
	ID_User_Pagamento SERIAL PRIMARY KEY,	
	ID_Oder INT REFERENCES Order(ID_Order),	
	tipo_pagamento	VARCHAR (50),	
	prazo	DATE
);	

/* Tabela de criacao do estoque do produto */
CREATE TABLE Product_Stock(
	ID_Product_Stock	SERIAL	PRIMARY	KEY,	
	ID_Product	INT	REFERENCES	Product(ID_Product),	
	quantidade	INT,	
	data_cadastro	TIMESTAMP,	
	modificado_em	TIMESTAMP
);

CREATE TABLE Product_Image(
	ID_Product_Image	SERIAL	PRIMARY	KEY,	
	ID_Product	INT	REFERENCES	Product(ID_Product),	
	link VARCHAR(255)
);
