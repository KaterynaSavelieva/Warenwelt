USE onlineshop;

CREATE OR REPLACE VIEW v_rating_products as Select	
	p.product_id,
	p.product,
	COUNT(r.review_id) AS products_review_count,
	round(AVG(r.rating),1) AS products_avg_rating,
	MIN(r.rating)AS products_min_rating,
	MAX(r.rating)AS products_max_rating
FROM product p
LEFT JOIN review r ON r.product_id = p.product_id
GROUP BY p.product_id, p.product;


