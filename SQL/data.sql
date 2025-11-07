USE onlineshop;

INSERT INTO customers (name, email, address, phone) VALUES
('Anna Meier', 'anna.meier@mail.com', 'Hauptstrasse 12, Graz', '+436601112223'),
('Peter Schmidt', 'peter.schmidt@mail.com', 'Bahnhofstrasse 45, Wien', '+436602223334'),
('Tech Solutions GmbH', 'office@techsolutions.at', 'Industriestrasse 5, Linz', '+43732234567'),
('Fashion Boutique OG', 'kontakt@fashionboutique.at', 'Graben 9, Salzburg', '+43662222111'),
('Julia Bauer', 'julia.bauer@mail.com', 'Kirchweg 8, Innsbruck', '+436603334445');

INSERT INTO private_customer (customer_id, birthdate) VALUES
(1, '1990-03-15'),
(2, '1985-07-21'),
(5, '1998-11-30');

INSERT INTO company_customer (customer_id, company_number) VALUES
(3, '987654321'),
(4, '123456789');

INSERT INTO product (product, price, weight, category) VALUES
('Smartphone Galaxy X', 699.99, 0.25, 'electronics'),
('Laptop ProBook 15', 1199.50, 1.8, 'electronics'),
('Winterjacke Damen', 149.90, 1.2, 'clothing'),
('T-Shirt Herren Blau', 29.99, 0.3, 'clothing'),
('Roman – Der Berg', 19.99, 0.5, 'book'),
('Kochbuch – Österreichische Küche', 34.50, 0.8, 'book');

INSERT INTO electronics (product_id, brand, warranty_years) VALUES
(1, 'Samsung', 2),
(2, 'HP', 3);

INSERT INTO clothing (product_id, size) VALUES
(3, 'M'),
(4, 'L');

INSERT INTO books (product_id, author, page_count) VALUES
(5, 'Thomas Huber', 320),
(6, 'Martina Koch', 210);

INSERT INTO review (customer_id, product_id, rating, comment, created_at) VALUES
(1, 1, 5, 'Super Smartphone! Sehr zufrieden.', '2025-11-01'),
(2, 2, 4, 'Gute Leistung, aber Akku könnte besser sein.', '2025-11-02'),
(3, 3, 5, 'Sehr gute Qualität und schneller Versand.', '2025-11-03'),
(5, 5, 4, 'Schöne Geschichte, etwas lang.', '2025-11-04'),
(4, 4, 5, 'Top Qualität, angenehmer Stoff.', '2025-11-05');
