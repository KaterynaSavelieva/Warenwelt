USE onlineshop;

-- Kunden
INSERT INTO kunden(name, email) VALUES
('Max Mustermann','max@example.com'),
('Anna Test','anna@example.com');

-- Produkt: Elektronik
INSERT INTO produkte(name, preis, gewicht, kategorie)
VALUES ('Laptop X15', 1299.90, 1.80, 'elektronik');
INSERT INTO elektronik(produkt_id, marke, garantie_jahre)
VALUES (LAST_INSERT_ID(), 'Acme', 2);

-- Produkt: Kleidung
INSERT INTO produkte(name, preis, gewicht, kategorie)
VALUES ('Pullover', 39.90, 0.45, 'kleidung');
INSERT INTO kleidung(produkt_id, groesse)
VALUES (LAST_INSERT_ID(), 'L');

-- Produkt: Buch
INSERT INTO produkte(name, preis, gewicht, kategorie)
VALUES ('Python Basics', 24.50, 0.60, 'buch');
INSERT INTO buch(produkt_id, autor, seitenanzahl)
VALUES (LAST_INSERT_ID(), 'M. Meyer', 220);
