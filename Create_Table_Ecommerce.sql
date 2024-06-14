/* Tabela de criacao do usuario, no postgre não se pode criar um so com User,
   aí inseri como UserTable */

CREATE TABLE UserTable (
    ID_User SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    cpf VARCHAR(11),
    phone BIGINT,
    adm BOOLEAN DEFAULT FALSE
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
   discount DECIMAL,
   highl BOOLEAN,
   height DECIMAL,
   width DECIMAL,
   length DECIMAL,
   weight DECIMAL,
   quantity	INT
);

/* Tabela de criacao do pedido */
CREATE TABLE User_Order (
  ID_Order SERIAL PRIMARY KEY, 
  ID_User INT REFERENCES UserTable(ID_User), 
  buy_date TIMESTAMP,
  status VARCHAR (50),
  payment_type VARCHAR (50),
  expiration DATE,
  total_bought DECIMAL
);

/* Tabela de criacao do carrinho */
CREATE TABLE Products_Order (
  ID_Products_Order SERIAL PRIMARY KEY, 
  ID_Order INT REFERENCES User_Order(ID_Order),
  ID_Product INT REFERENCES Product(ID_Product),
  quantity INT
);

CREATE TABLE Product_Image(
	ID_Product_Image	SERIAL	PRIMARY	KEY,	
	ID_Product	INT	REFERENCES	Product(ID_Product),	
	path VARCHAR(255)
);

INSERT INTO brand (name) VALUES ('N/d');
INSERT INTO category (name) VALUES ('N/d');

CREATE OR REPLACE FUNCTION check_user_duplicates() 
RETURNS TRIGGER AS $$
BEGIN
    -- Check for duplicate email
    IF (SELECT COUNT(*) FROM UserTable WHERE email = NEW.email) > 0 THEN
        RAISE EXCEPTION 'Email em uso: %', NEW.email;
    END IF;

    -- Check for duplicate CPF
    IF (SELECT COUNT(*) FROM UserTable WHERE cpf = NEW.cpf) > 0 THEN
        RAISE EXCEPTION 'CPF em uso: %', NEW.cpf;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_product_on_delete() 
RETURNS TRIGGER AS $$
BEGIN
    IF TG_TABLE_NAME = 'category' THEN
        UPDATE Product
        SET ID_Category = 1
        WHERE ID_Category = OLD.category_id;
    ELSIF TG_TABLE_NAME = 'brand' THEN
        UPDATE Product
        SET ID_Brand = 1
        WHERE ID_Brand = OLD.brand_id;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER category_delete_trigger
BEFORE DELETE ON Category
FOR EACH ROW
EXECUTE FUNCTION update_product_on_delete();

CREATE TRIGGER brand_delete_trigger
BEFORE DELETE ON Brand
FOR EACH ROW
EXECUTE FUNCTION update_product_on_delete();

CREATE TRIGGER check_user_duplicates_trigger
BEFORE INSERT ON UserTable
FOR EACH ROW
EXECUTE FUNCTION check_user_duplicates();

