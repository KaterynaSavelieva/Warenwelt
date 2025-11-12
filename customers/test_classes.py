from customers import Customer
from private_customer import PrivateCustomer
from company_customer import CompanyCustomer
import sys

# Disable full traceback for cleaner error output
sys.tracebacklimit = 0

print("Running customers validation tests...\n")

try:
    c1 = Customer("Anna Schmidt", "Main Street 5", "anna@mail.at", "+436601234567", "StrongPass1")
    print(c1)
except Exception as e:
    print("Error creating Customer 1:", e)

try:
    p1 = PrivateCustomer("Lena", "Ring 2", "lena@mail.at", "+43660111222", "Password9", "1990-05-20")
    print(p1)
except Exception as e:
    print("Error creating PrivateCustomer 1:", e)

try:
    f1 = CompanyCustomer("ACME GmbH", "Industry Street 10", "info@acme.at", "+43720123456", "Secret12", "123456789")
    print(f1)
except Exception as e:
    print("Error creating CompanyCustomer 1:", e)

#  Invalid test cases (expected to raise validation errors)
print("\nTesting invalid inputs...\n")

try:
    f2 = CompanyCustomer("ACME GmbH", "Industry Street 10", "info@acme.at", "+43720123456", "Secret12", "5§§5555")
    print(f2)
except Exception as e:
    print("Error creating CompanyCustomer 2:", e)

try:
    c2 = Customer("Anna Schmidt", "Main Street 5", "annamail.at", "+436601234567", "StrongPass1")
    print(c2)
except Exception as e:
    print("Error creating Customer 2:", e)

try:
    p2 = PrivateCustomer("Lena", "Ring 2", "lena@mail.at", "+43662222w0111222", "Password9", "1990-05-20")
    print(p2)
except Exception as e:
    print("Error creating PrivateCustomer 2:", e)
