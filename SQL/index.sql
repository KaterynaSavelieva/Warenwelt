USE onlineshop;
CREATE INDEX idx_review_customer  ON review(customer_id);
CREATE INDEX idx_review_product   ON review(product_id);
CREATE INDEX idx_electronics_pid  ON electronics(product_id);
CREATE INDEX idx_clothing_pid     ON clothing(product_id);
CREATE INDEX idx_books_pid        ON books(product_id);
