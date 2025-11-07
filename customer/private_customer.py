from datetime import date
from customer import Customer
from validator import Validator


class PrivateCustomer(Customer):
    def __init__(self, name: str, address: str, email: str, phone: str, password: str, birthdate: date | str):
        super().__init__(name, address, email, phone, password)
        self._birthdate = Validator.validate_birthdate(birthdate)

    # --- calculate age ---
    def calculate_age(self) -> int:
        today = date.today()
        age = today.year - self._birthdate.year
        if (today.month, today.day) < (self._birthdate.month, self._birthdate.day):
            age -= 1
        return age

    # --- property with validation ---
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
            f"Age: {self.calculate_age()}, "
            f"Password: {self.get_password_masked()})"
        )