INSERT INTO customers (name, email, address, phone, kind, password)
VALUES
('Anna Meier', 'anna.meier@example.com', 'Graz, Herrengasse 12', '+436601234567', 'private', 'anna123'),
('Peter Huber', 'peter.huber@example.com', 'Wien, Mariahilferstraße 8', '+436606789012', 'company', 'peter456'),
('Julia König', 'julia.koenig@example.com', 'Linz, Landstraße 20', '+436603334455', 'private', 'julia789'),
('TechPro GmbH', 'office@techpro.at', 'Innsbruck, Hauptstraße 5', '+436607777777', 'company', 'tech999');

INSERT INTO private_customer (customer_id, birthdate)
VALUES
(1, '1990-03-15'),
(3, '1985-10-22');

INSERT INTO company_customer (customer_id, company_number)
VALUES
(2, '123456789'),
(4, '987654321');

INSERT INTO product (product, price, weight, category)
VALUES
('Laptop HP EliteBook', 899.99, 2.3, 'electronics'),
('T-Shirt Cotton Blue', 19.90, 0.25, 'clothing'),
('Der kleine Prinz', 12.50, 0.40, 'books'),
('Smartphone Samsung Galaxy', 699.00, 0.45, 'electronics'),
('Jeans Levi’s 501', 79.90, 0.60, 'clothing'),
('Data Science mit Python', 44.90, 0.90, 'books');

INSERT INTO electronics (product_id, brand, warranty_years)
VALUES
(1, 'HP', 2),
(4, 'Samsung', 2);

INSERT INTO clothing (product_id, size)
VALUES
(2, 'M'),
(5, 'L');

INSERT INTO books (product_id, author, page_count)
VALUES
(3, 'Antoine de Saint-Exupéry', 96),
(6, 'Sebastian Raschka', 512);

INSERT INTO review (customer_id, product_id, rating, comment)
VALUES
(1, 1, 5, 'Super Laptop, sehr schnell!'),
(3, 3, 4, 'Ein schöner Klassiker.'),
(2, 4, 5, 'Sehr gutes Smartphone für den Preis.'),
(4, 5, 3, 'Gute Qualität, aber etwas teuer.');
