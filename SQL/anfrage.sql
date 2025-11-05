USE onlineshop;

SELECT p.*, e.marke, e.garantie_jahre, k.groesse, b.autor, b.seitenanzahl
FROM produkte p
LEFT JOIN elektronik e ON e.produkt_id = p.produkt_id
LEFT JOIN kleidung  k ON k.produkt_id = p.produkt_id
LEFT JOIN buch      b ON b.produkt_id = p.produkt_id
ORDER BY p.produkt_id;
