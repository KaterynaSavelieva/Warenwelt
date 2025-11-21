INSERT INTO customers (name, email, address, phone, kind, password) VALUES
('Anna Müller', 'anna.mueller@example.com', 'Wien, Hauptstr. 12', '+436601234567', 'private', 'pass123'),
('Markus Steiner', 'markus.steiner@example.com', 'Graz, Lindenweg 5', '+436609876543', 'private', 'abc456'),
('Peter König', 'peter.koenig@example.com', 'Salzburg, Mozartplatz 3', '+436701112223', 'private', 'pw789'),
('Müller GmbH', 'office@mueller-gmbh.at', 'Linz, Industriestr. 45', '+43732123456', 'company', 'mueller2024'),
('TechWorld OG', 'contact@techworld.at', 'Wien, Schubertring 1', '+431232323', 'company', 'tw2024'),
('Sabine Gruber', 'sabine.gruber@example.com', 'Klagenfurt, Seeweg 7', '+436771231231', 'private', 'sab2024'),
('Lisa Baum', 'lisa.baum@example.com', 'Villach, Gartenweg 9', '+436751234567', 'private', 'baum777'),
('Johann Bauer', 'johann.bauer@example.com', 'Graz, Feldgasse 10', '+436609999999', 'private', 'jbpass'),
('FashionPro KG', 'info@fashionpro.at', 'Wien, Modegasse 2', '+431555777', 'company', 'fashion22'),
('BookPlanet GmbH', 'service@bookplanet.at', 'Salzburg, Buchweg 8', '+43662888888', 'company', 'books333'),
('Maria Huber', 'maria.huber@example.com', 'Innsbruck, Sonnenstr. 4', '+43664111222', 'private', 'mh2025'),
('Klaus Berger', 'klaus.berger@example.com', 'Linz, Gartenstr. 20', '+43660444555', 'private', 'kb999'),
('EcoEnergy GmbH', 'office@ecoenergy.at', 'Graz, Solarstr. 5', '+43316111111', 'company', 'eco333'),
('SmartSystems AG', 'office@smartsys.at', 'Wien, Techstr. 12', '+431787878', 'company', 'smart444'),
('Helga Mayr', 'helga.mayr@example.com', 'St. Pölten, Am Platz 6', '+43666999888', 'private', 'hm111'),
('Sandra Leitner', 'sandra.leitner@example.com', 'Villach, Bergstr. 8', '+43666112233', 'private', 'sl2025'),
('NextTech GmbH', 'sales@nexttech.at', 'Graz, Innovationstr. 9', '+4331666666', 'company', 'ntpass'),
('ArtHouse OG', 'info@arthouse.at', 'Wien, Galerieplatz 3', '+431222333', 'company', 'art555'),
('Thomas Winkler', 'thomas.winkler@example.com', 'Linz, Donauweg 11', '+436604321123', 'private', 'twpass'),
('Bioprodukte GmbH', 'office@bioprodukte.at', 'Graz, Marktstr. 5', '+43316777777', 'company', 'bio2025');

INSERT INTO private_customer (customer_id, birthdate) VALUES
(1, '1990-05-10'), (2, '1985-07-21'), (3, '1992-03-15'),
(6, '1989-10-05'), (7, '1998-11-22'), (8, '1980-02-02'),
(11, '1994-09-17'), (12, '1983-06-09'), (15, '1975-08-30'),
(16, '2000-12-11'), (19, '1988-04-04');

INSERT INTO company_customer (customer_id, company_number) VALUES
(4, 'ATU12345678'),
(5, 'ATU87654321'),
(9, 'ATU11122233'),
(10, 'ATU33344455'),
(13, 'ATU55566677'),
(14, 'ATU88899900'),
(17, 'ATU12121212'),
(18, 'ATU34343434'),
(20, 'ATU56565656');


INSERT INTO product (product, price, weight, category) VALUES
('Laptop Lenovo IdeaPad', 899.99, 1.8, 'electronics'),
('Smartphone Samsung S24', 999.00, 0.4, 'electronics'),
('Bluetooth Kopfhörer Sony', 149.99, 0.2, 'electronics'),
('Winterjacke Damen', 129.90, 1.2, 'clothing'),
('Jeans Herren Slim Fit', 79.50, 0.8, 'clothing'),
('Kinder T-Shirt', 19.99, 0.3, 'clothing'),
('Roman "Der Fluss"', 14.99, 0.5, 'books'),
('Kochbuch Vegan Life', 24.50, 0.7, 'books'),
('Notebook Acer Aspire', 699.99, 2.0, 'electronics'),
('Tastatur Logitech', 59.99, 0.6, 'electronics'),
('Sommerkleid', 49.99, 0.5, 'clothing'),
('Pullover Wolle', 89.00, 1.0, 'clothing'),
('Roman "Im Winter"', 17.90, 0.6, 'books'),
('Kinderbuch "Tiere"', 12.99, 0.4, 'books'),
('Smartwatch Apple SE', 349.00, 0.3, 'electronics'),
('Monitor Dell 24"', 189.99, 3.5, 'electronics'),
('Sneakers Nike Air', 119.00, 0.9, 'clothing'),
('Hose Damen Elegant', 69.90, 0.7, 'clothing'),
('Fachbuch "Python Basics"', 35.00, 0.8, 'books'),
('Roman "Schatten der Zeit"', 18.50, 0.6, 'books');

INSERT INTO electronics (product_id, brand, warranty_years) VALUES
(1, 'Lenovo', 2),
(2, 'Samsung', 2),
(3, 'Sony', 1),
(9, 'Acer', 2),
(10, 'Logitech', 1),
(15, 'Apple', 2),
(16, 'Dell', 3);


INSERT INTO clothing (product_id, size) VALUES
(4, 'M'), (5, 'L'), (6, 'S'),
(11, 'M'), (12, 'L'), (17, '42'), (18, '38');


INSERT INTO books (product_id, author, page_count) VALUES
(7, 'Jonas Winter', 320),
(8, 'Lisa Koch', 210),
(13, 'Eva Sommer', 280),
(14, 'Thomas Klein', 140),
(19, 'Max Meier', 250),
(20, 'Anna Schulz', 400);


INSERT INTO review (customer_id, product_id, rating, comment) VALUES
(1, 1, 5, 'Sehr zufrieden mit dem Laptop!'),
(2, 2, 4, 'Gutes Handy, aber Akku könnte besser sein.'),
(3, 4, 5, 'Super warme Jacke!'),
(7, 7, 4, 'Interessanter Roman.'),
(11, 8, 5, 'Tolle Rezepte!'),
(12, 10, 4, 'Gute Tastatur, aber laut.'),
(15, 15, 5, 'Liebe meine neue Smartwatch!'),
(16, 17, 5, 'Bequem und modern.'),
(8, 13, 3, 'Ganz ok, aber etwas langweilig.'),
(19, 19, 5, 'Sehr hilfreich für Anfänger!');

INSERT INTO orders (customer_id, order_date, total) VALUES
(1, '2025-10-01 10:15:00', 899.99),
(2, '2025-10-03 09:20:00', 999.00),
(3, '2025-10-05 14:45:00', 129.90),
(4, '2025-10-06 16:10:00', 149.99),
(5, '2025-10-07 11:35:00', 245.00),
(6, '2025-10-09 09:10:00', 149.99),
(7, '2025-10-10 13:25:00', 259.80),
(8, '2025-10-11 16:40:00', 79.50),
(9, '2025-10-12 11:15:00', 1299.00),
(10, '2025-10-13 18:05:00', 64.49),
(11, '2025-10-14 10:00:00', 139.00),
(12, '2025-10-15 12:20:00', 374.00),
(13, '2025-10-16 09:55:00', 999.00),
(14, '2025-10-17 14:45:00', 769.98),
(15, '2025-10-18 10:10:00', 168.99),
(16, '2025-10-19 17:30:00', 59.99),
(17, '2025-10-20 11:50:00', 184.90),
(18, '2025-10-21 15:35:00', 208.50),
(19, '2025-10-22 09:05:00', 119.00),
(20, '2025-10-23 13:40:00', 284.98),
(1, '2025-10-24 16:25:00', 35.00),
(2, '2025-10-25 10:30:00', 49.99),
(3, '2025-10-26 18:50:00', 1048.99),
(4, '2025-10-27 12:05:00', 37.49),
(5, '2025-10-28 09:20:00', 228.90);

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 899.99),
(2, 2, 1, 999.00),
(3, 4, 1, 129.90),
(4, 3, 1, 149.99),
(5, 8, 1, 24.50),
(6, 3, 1, 149.99),
(7, 4, 2, 129.90),
(8, 5, 1, 79.50),
(9, 1, 1, 899.99),
(9, 15, 1, 399.01),
(10, 14, 1, 12.99),
(10, 7, 1, 14.99),
(10, 8, 1, 36.51),
(11, 12, 1, 89.00),
(11, 6, 1, 19.99),
(11, 18, 1, 30.01),
(12, 16, 2, 189.99),
(13, 2, 1, 999.00),
(14, 9, 1, 699.99),
(14, 10, 1, 69.99),
(15, 11, 1, 49.99),
(15, 17, 1, 119.00),
(16, 19, 1, 35.00),
(17, 11, 1, 49.99),
(18, 15, 1, 349.00),
(18, 10, 1, 59.99),
(18, 6, 1, 19.99),
(19, 17, 1, 119.00),
(20, 4, 1, 129.90),
(20, 12, 1, 89.00),
(20, 7, 1, 66.08);




