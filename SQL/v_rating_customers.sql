USE onlineshop;

Create or REPLACE View v_rating_customers as Select	
	c.customer_id,
	c.name,
	COUNT(r.review_id) AS customers_review_count,
	round(AVG(r.rating),1) AS customers_avg_rating,
	MIN(r.rating)AS customers_min_rating,
	MAX(r.rating)AS customers_max_rating
FROM customers c
LEFT JOIN review r ON r.customer_id = c.customer_id
GROUP BY c.customer_id, c.name;


