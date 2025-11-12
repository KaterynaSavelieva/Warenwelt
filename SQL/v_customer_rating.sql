USE onlineshop;
CREATE OR REPLACE VIEW v_customer_rating AS
SELECT
    c.customer_id,
    c.name,
    COUNT(r.review_id)           AS reviews_count,
    ROUND(AVG(r.rating), 2)      AS avg_rating,
    MIN(r.rating)                AS min_rating,
    MAX(r.rating)                AS max_rating,
    ROUND(SUM(r.rating), 2)      AS sum_rating
FROM customers AS c
LEFT JOIN review AS r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.name
ORDER BY avg_rating DESC;

SELECT * FROM v_customer_rating;
