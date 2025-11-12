CREATE OR REPLACE VIEW v_rating_summary_for_product AS
SELECT
    p.product_id,
    p.product,
    COUNT(r.review_id)           AS reviews_count,
    ROUND(AVG(r.rating), 2)      AS avg_rating,
    MIN(r.rating)                AS min_rating,
    MAX(r.rating)                AS max_rating,
    ROUND(SUM(r.rating), 2)      AS sum_rating
FROM product AS p
LEFT JOIN review AS r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product
ORDER BY avg_rating DESC;

SELECT * FROM v_product_rating;
-- drop view v_product_rating;
