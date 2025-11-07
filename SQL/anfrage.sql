USE onlineshop;

CREATE OR REPLACE VIEW v_tab AS
SELECT 
    p.*, 
    e.brand, 
    e.warranty_years, 
    c.size, 
    b.author, 
    b.page_count
FROM product p
LEFT JOIN electronics e ON e.product_id = p.product_id
LEFT JOIN clothing c     ON c.product_id = p.product_id
LEFT JOIN books b        ON b.product_id = p.product_id
ORDER BY p.product_id;

SELECT * FROM v_tab;
