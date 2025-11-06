CREATE DATABASE IF NOT EXISTS onlineshop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE onlineshop;
-- drop table keidung;
DROP TABLE IF EXISTS kunden;

DROP TABLE IF EXISTS  elektronik;
DROP TABLE IF EXISTS  kleidung;
DROP TABLE IF EXISTS buch;
DROP TABLE IF EXISTS  produkte;
DROP TABLE  IF EXISTS produkt;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS electronics;
DROP TABLE IF EXISTS clothing;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS product;


CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    weight DECIMAL(10,2) NOT NULL,
    category ENUM('electronics','clothing','book') NOT NULL
);

CREATE TABLE IF NOT EXISTS electronics (
    id INT,
    brand VARCHAR(100) NOT NULL,
    warranty_years INT NOT NULL,
    FOREIGN KEY (id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clothing (
    id INT,
    size VARCHAR(20) NOT NULL,
    FOREIGN KEY (id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS books (
    id INT,
    author VARCHAR(160) NOT NULL,
    page_count INT NOT NULL,
    FOREIGN KEY (id) REFERENCES product(id) ON DELETE CASCADE
);