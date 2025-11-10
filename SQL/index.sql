CREATE INDEX idx_customers_name ON customers (name);
CREATE INDEX idx_customers_kind ON customers (kind);

CREATE INDEX idx_company_customer_number ON company_customer (company_number);

CREATE INDEX idx_product_name ON product (product);
CREATE INDEX idx_product_category ON product (category);
CREATE INDEX idx_product_price ON product (price);

CREATE INDEX idx_electronics_brand ON electronics (brand);
CREATE INDEX idx_clothing_size ON clothing (size);
CREATE INDEX idx_books_author ON books (author);

CREATE INDEX idx_review_customer ON review (customer_id);
CREATE INDEX idx_review_product ON review (product_id);
CREATE INDEX idx_review_rating ON review (rating);
CREATE INDEX idx_review_date ON review (created_at);
