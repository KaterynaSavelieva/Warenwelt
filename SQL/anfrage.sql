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
LEFT JOIN electronics e ON e.id = p.id
LEFT JOIN clothing c     ON c.id = p.id
LEFT JOIN books b        ON b.id = p.id
ORDER BY p.id;

SELECT * FROM v_tab;
