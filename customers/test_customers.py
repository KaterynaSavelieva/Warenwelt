from customers.customer_methods import CustomerMethods

cm = CustomerMethods()


# id_tech3 = cm.save_customer(
#     name="Tech GmbHhhh", email="officetech@3hj4144.at", address="Industriestr. 9",  phone="+43732234567",
#     kind="company", password="Tech9999", company_number="98765432111")
#if id_tech3: cm.get_customer(id_tech3)

# load all
#cm.get_all_customers()

# cm.get_customer(2)
# cm.update_customer(customer_id=2, phone="+4377777777")
# cm.get_customer(2)

cm.delete_customer(customer_id=5)

pc=cm.find_customers_by_kind("private")
print (pc)
print(cm.find_customers_by_kind("company"))

cm.close()
