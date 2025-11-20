USE onlineshop;
CREATE OR REPLACE VIEW v_customers AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.address,
    c.phone,
    c.kind,

    CONCAT_WS(' / ', c_c.company_number, DATE_FORMAT(c_p.birthdate, '%Y-%m-%d'))AS "Company Number/ Birthdate"
FROM customers c
LEFT JOIN company_customer c_c ON c_c.customer_id=c.customer_id
LEFT JOIN private_customer c_p ON c_p.customer_id=c.customer_id
ORDER BY c.customer_id;

SELECT * FROM v_customers;

-- SELECT * FROM company_customer;
