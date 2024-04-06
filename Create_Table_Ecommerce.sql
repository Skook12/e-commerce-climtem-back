/* Tabela de criacao do usuario, no postgre não se pode criar um so com User,
   aí inseri como UserTable */

CREATE TABLE UserTable (
    ID_User SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone BIGINT
);

/* Tabela de criacao do endereco */
CREATE TABLE User_Address (
    ID_User_Address SERIAL PRIMARY KEY,
    ID_User INT REFERENCES UserTable(ID_User),
    num INT,
    complement VARCHAR(255),
    cep VARCHAR(10),
    city VARCHAR(255)
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
   name VARCHAR(255),
   description TEXT,
   value DECIMAL,
   discount DECIMAL
);

/* Tabela de criacao do pedido */
CREATE TABLE User_Order (
  ID_Order SERIAL PRIMARY KEY, 
  ID_User INT REFERENCES UserTable(ID_User), 
  buy_date TIMESTAMP, 
  status VARCHAR (50)
);

/* Tabela de criacao do carrinho */
CREATE TABLE Products_Order (
  ID_Products_Order SERIAL PRIMARY KEY, 
  ID_Order INT REFERENCES User_Order(ID_Order), 
  quantity INT, 
  total_bought DECIMAL
); 

/* Tabela de criacao do pagamento */
CREATE TABLE User_Pagamento(
	ID_User_Pagamento SERIAL PRIMARY KEY,	
	ID_Order INT REFERENCES User_Order(ID_Order),	
	payment_type	VARCHAR (50),	
	expiration DATE
);

/* Tabela de criacao do estoque do produto */
CREATE TABLE Product_Stock(
	ID_Product_Stock	SERIAL	PRIMARY	KEY,	
	ID_Product	INT	REFERENCES	Product(ID_Product),	
	quantity	INT,	
	register_date	TIMESTAMP,	
	modified_date	TIMESTAMP
);
