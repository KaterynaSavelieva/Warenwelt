USE onlineshop;

SELECT * FROM bestellung_details;
SELECT * FROM bestellung
INNER JOIN bestellung_details ON bestellung_details.order_id=bestellung.order_id;