USE onlineshop;

CREATE OR REPLACE VIEW v_rating1 AS
SELECT
    r.review_id                     AS review_id,
    r.rating                        AS review_rating,
    r.comment                       AS review_comment,
    r.created_at                    AS review_date,

    c.customer_id                   AS customer_id,
    c.name                          AS customer_name,
    v_rc.customers_review_count     AS customer_total_reviews,
    v_rc.customers_avg_rating       AS customer_average_rating,
    v_rc.customers_min_rating       AS customer_min_rating,
    v_rc.customers_max_rating       AS customer_max_rating,

    p.product_id                    AS product_id,
    p.product                       AS product_name,
    p.category						AS category,
    v_rp.products_review_count      AS product_total_reviews,
    v_rp.products_avg_rating        AS product_average_rating,
    v_rp.products_min_rating        AS product_min_rating,
    v_rp.products_max_rating        AS product_max_rating

FROM review r
JOIN customers c ON c.customer_id = r.customer_id
JOIN product   p ON p.product_id   = r.product_id
LEFT JOIN v_rating_products  v_rp ON v_rp.product_id  = p.product_id
LEFT JOIN v_rating_customers v_rc ON v_rc.customer_id = c.customer_id

-- ORDER BY r.created_at DESC, r.review_id DESC
;

SELECT *
FROM v_rating1
-- WHERE product_id = 1
ORDER BY review_date DESC, review_id DESC;
