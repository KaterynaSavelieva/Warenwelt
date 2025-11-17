from datetime import date
from typing import Optional
from .customer import Customer
from .validator import Validator


class PrivateCustomer(Customer):
    def __init__(
        self,
        name: str,
        address: Optional[str],
        email: str,
        phone: Optional[str],
        password: str,
        birthdate: date | str,
        customer_id: Optional[int] = None
    ):
        super().__init__(
            name=name,
            address=address,
            email=email,
            phone=phone,
            password=password,
            kind="private",
            customer_id=customer_id
        )
        self._birthdate = Validator.validate_birthdate(birthdate)

    def calculate_age(self) -> int:
        today = date.today()
        age = today.year - self._birthdate.year
        if (today.month, today.day) < (self._birthdate.month, self._birthdate.day):
            age -= 1
        return age

    @property
    def birthdate(self) -> date:
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value: date | str) -> None:
        self._birthdate = Validator.validate_birthdate(value)

    def __str__(self) -> str:
        return (
            f"PrivateCustomer(ID: {self.customer_id}, Name: {self.name}, "
            f"Email: {self.email}, Phone: {self.phone}, "
            f"Birthdate: {self.birthdate}, Age: {self.calculate_age()}, "
            f"Password: {self.get_password_masked()})"
        )
