CREATE DATABASE IF NOT EXISTS onlineshop CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE onlineshop;
-- drop table keidung;
DROP TABLE IF EXISTS kunden;

DROP TABLE IF EXISTS  elektronik;
DROP TABLE IF EXISTS  kleidung;
DROP TABLE IF EXISTS buch;
DROP TABLE IF EXISTS  produkte;
DROP TABLE  IF EXISTS produkt;

CREATE TABLE IF NOT EXISTS kunden (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(120) NOT NULL,
	email VARCHAR(180) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS produkte (
	produkt_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(160) NOT NULL,
	preis DECIMAL(10,2) NOT NULL,
	gewicht DECIMAL(10,2) NOT NULL,
	kategorie ENUM('elektronik','kleidung','buch') NOT NULL
);

CREATE TABLE IF NOT EXISTS elektronik  (
	produkt_id INT,
	marke VARCHAR(100) NOT NULL,
	garantie_jahre INT NOT NULL,
	FOREIGN KEY (produkt_id) REFERENCES produkte(produkt_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS kleidung  (
	produkt_id INT,
	groesse VARCHAR(20) NOT NULL,
	FOREIGN KEY (produkt_id) REFERENCES produkte(produkt_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS buch  (
	produkt_id INT,
	autor VARCHAR(160) NOT NULL,
	seitenanzahl INT NOT NULL,
	FOREIGN KEY (produkt_id) REFERENCES produkte(produkt_id) ON DELETE CASCADE
);