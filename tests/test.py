from pydantic import ValidationError
from customer import Customer
from private_customer import PrivateCustomer
from company_customer import CompanyCustomer


def run_case(title, factory):
    """Try to create an object and print the result or a short error message."""
    try:
        obj = factory()  # Attempt to create the object
        print(f"OK  [{title}]: {obj}")
    except ValidationError as e:
        # Get the first validation message safely
        msg = e.errors()[0].get("msg", str(e))
        print(f"ERR [{title}]: {msg}")
    except Exception as e:
        print(f"ERR [{title}]: {e}")


# --- Valid cases ---
run_case("Customer (valid data)",
         lambda: Customer("Anna Schmidt", "Main Street 5", "anna@mail.at",
                          "+436601234567", "StrongPass1"))

run_case("PrivateCustomer (valid data)",
         lambda: PrivateCustomer("Lena", "Ring 2", "lena@mail.at",
                                 "+43660111222", "Password9", "1990-05-20"))

run_case("CompanyCustomer (valid data)",
         lambda: CompanyCustomer("ACME GmbH", "Industry Street 10", "info@acme.at",
                                 "+43720123456", "Secret12", "123456789"))

# --- Invalid cases ---
run_case("Customer (invalid email)",
         lambda: Customer("Anna Schmidt", "Main Street 5", "annamail.at",
                          "+436601234567", "StrongPass1"))

run_case("PrivateCustomer (invalid phone)",
         lambda: PrivateCustomer("Lena", "Ring 2", "lena@mail.at",
                                 "+43662222w0111222", "Password9", "1990-05-20"))

run_case("CompanyCustomer (invalid company number)",
         lambda: CompanyCustomer("ACME GmbH", "Industry Street 10", "info@acme.at",
                                 "+43720123456", "Secret12", "sdfd"))
