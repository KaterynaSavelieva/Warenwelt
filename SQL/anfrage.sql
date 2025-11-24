USE onlineshop;

SELECT * FROM order_items;
SELECT * FROM orders
INNER JOIN order_items ON orders.order_id=order_items.order_id;

SELECT * FROM review ORDER BY review_id DESC;