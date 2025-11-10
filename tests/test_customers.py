from customer.customer_methods import CustomerMethods

cm = CustomerMethods()


id_tech3 = cm.save_customer(
    name="Tech GmbHhhh",
    email="officetech@3hj4144.at",
    address="Industriestr. 9",
    phone="+43732234567",
    kind="company",
    password="Tech9999",          # 🔸 ДОДАНО
    company_number="98765432111",
)

if id_tech3: cm.get_customer(id_tech3)

# load all
cm.get_all_customers()

cm.close()
