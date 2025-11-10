USE onlineshop;
CREATE OR REPLACE VIEW v_cust AS
SELECT 
    cus.*,
	cus_c.company_number,
    cus_p.birthdate,
    pr.*, 
    pr_e.brand, 
    pr_e.warranty_years, 
    pr_c.size, 
    pr_b.author, 
    pr_b.page_count,
    r.rating,
    r.comment,
    r.created_at
FROM customers cus
LEFT JOIN company_customer cus_c ON cus_c.customer_id=cus.customer_id
LEFT JOIN private_customer cus_p ON cus_p.customer_id=cus.customer_id
LEFT JOIN review r 			ON r.customer_id=cus.customer_id
LEFT JOIN product pr 	ON pr.product_id=r.product_id
LEFT JOIN electronics pr_e ON pr_e.product_id = pr.product_id
LEFT JOIN clothing pr_c     ON pr_c.product_id = pr.product_id
LEFT JOIN books pr_b        ON pr_b.product_id = pr.product_id
ORDER BY cus.customer_id;

SELECT * FROM v_cust;

SELECT * FROM company_customer;
