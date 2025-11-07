CREATE DATABASE IF NOT EXISTS onlineshop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE onlineshop;
-- drop table keidung;
DROP TABLE IF EXISTS kunden;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS  elektronik;
DROP TABLE IF EXISTS  kleidung;
DROP TABLE IF EXISTS buch;


DROP TABLE IF EXISTS electronics;
DROP TABLE IF EXISTS clothing;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS private_customer;
DROP TABLE IF EXISTS company_customer;
DROP TABLE IF EXISTS customers;

DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS  produkte;
DROP TABLE  IF EXISTS produkt;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    email       VARCHAR(180) NOT NULL UNIQUE,
    address     VARCHAR(180),
    phone       VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS private_customer (
    customer_id INT PRIMARY KEY,
    birthdate DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company_customer (
	customer_id INT PRIMARY KEY,
    company_number VARCHAR(32) NOT NULL,
    UNIQUE (company_number),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(160) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    weight DECIMAL(10,2) NOT NULL,
    category ENUM('electronics','clothing','book') NOT NULL
);

CREATE TABLE IF NOT EXISTS electronics (
    product_id INT,
    brand VARCHAR(100) NOT NULL,
    warranty_years INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clothing (
    product_id INT,
    size VARCHAR(20) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS books (
    product_id INT,
    author VARCHAR(160) NOT NULL,
    page_count INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment VARCHAR(255),
    created_at DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE ON UPDATE CASCADE
);
