from typing import Optional
from .customer import Customer
from .validator import Validator


class CompanyCustomer(Customer):
    def __init__(
        self,
        name: str,
        address: Optional[str],
        email: str,
        phone: Optional[str],
        password: str,
        company_number: str,
        customer_id: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            address=address,
            email=email,
            phone=phone,
            password=password,
            kind="company",
            customer_id=customer_id,
        )
        self._company_number = Validator.validate_company_number(company_number)

    @property
    def company_number(self) -> str:
        return self._company_number

    @company_number.setter
    def company_number(self, value: str) -> None:
        self._company_number = Validator.validate_company_number(value)

    def __str__(self) -> str:
        return (
            f"CompanyCustomer(ID: {self.customer_id}, Name: {self.name}, "
            f"Email: {self.email}, Phone: {self.phone}, "
            f"Company number: {self.company_number}, "
            f"Password: {self.get_password_masked()})"
        )
