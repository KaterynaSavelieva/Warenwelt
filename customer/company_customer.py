from customer import Customer
from validator import Validator


class CompanyCustomer(Customer):
    def __init__(self, name: str, address: str, email: str, phone: str, password: str, company_number: str):
        super().__init__(name, address, email, phone, password)
        self._company_number = Validator.validate_company_number(company_number)

    # --- property with re-validation ---
    @property
    def company_number(self) -> str:
        return self._company_number

    @company_number.setter
    def company_number(self, value: str) -> None:
        self._company_number = Validator.validate_company_number(value)

    def __str__(self) -> str:
        return (
            f"CompanyCustomer(ID: {self.id}, Name: {self.name}, "
            f"Email: {self.email}, Phone: {self.phone}, "
            f"Company number: {self.company_number}, "
            f"Password: {self.get_password_masked()})"
        )
