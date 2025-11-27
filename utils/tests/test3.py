import sys
sys.tracebacklimit = 0

from customers import Customer
from private_customer import PrivateCustomer
from company_customer import CompanyCustomer


def make_and_print(label, factory):
    """Create an object and print it nicely, or show the validation error without stopping the test."""
    try:
        obj = factory()
        print(obj)
    except Exception as e:
        print(f"{label}: {e}")


print("Customer class validation test\n")

make_and_print("c1", lambda: Customer(
    "Anna Schmidt", "Main Street 5", "anna@mail.at", "+436601234567", "StrongPass1"
))
make_and_print("p1", lambda: PrivateCustomer(
    "Lena", "Ring 2", "lena@mail.at", "+43660111222", "Password9", "1990-05-20"
))
make_and_print("f1", lambda: CompanyCustomer(
    "ACME GmbH", "Industry Street 10", "info@acme.at", "+43720123456", "Secret12", "123456789"
))

# — intentionally bad case — will show a clear error but won’t stop the test
make_and_print("f2", lambda: CompanyCustomer(
    "ACME GmbH", "Industry Street 10", "info@acme.at", "+43720123456", "Secret12", "$$$$$$$"
))

# next tests will still run
make_and_print("c2", lambda: Customer(
    "Anna Schmidt", "Main Street 5", "annamail.at", "+436601234567", "StrongPass1"
))
make_and_print("p2", lambda: PrivateCustomer(
    "Lena", "Ring 2", "lena@mail.at", "+43662222w0111222", "Password9", "1990-05-20"
))
