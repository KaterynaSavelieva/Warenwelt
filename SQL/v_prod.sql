USE onlineshop;

CREATE OR REPLACE VIEW v_prod AS
SELECT
    p.product_id,
    p.product,
    p.price,
    p.weight,
    p.category,

    e.brand,
    e.warranty_years,

    c.size,
    b.author,
    b.page_count,

    ar.avg_rating,
    ar.review_count
FROM product p
LEFT JOIN electronics e ON e.product_id = p.product_id
LEFT JOIN clothing   c  ON c.product_id = p.product_id
LEFT JOIN books      b  ON b.product_id = p.product_id
LEFT JOIN (
    SELECT
        product_id,
        ROUND(AVG(rating), 1) AS avg_rating,
        COUNT(*)              AS review_count
    FROM review
    GROUP BY product_id
) ar ON ar.product_id = p.product_id
ORDER BY p.product_id;


SELECT * FROM v_prod;
