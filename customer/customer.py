from validator import Validator
from typing import Optional

"""Verwendung von @property, weil dies der Python-typische („pythonic“) Weg ist, mit Attributen zu arbeiten.
Dadurch können Werte validiert oder geändert werden, ohne dass sich der Zugriff im Code ändert.
Der Code bleibt objektorientiert, sicher und besser lesbar."""

class Customer:
    next_id = 10001

    def __init__(self, name: str, address: str, email: str, phone: str, password: str, customer_id: Optional[int] = None):
        if customer_id is not None:
            self.customer_id = int(customer_id)
        else:
            self.customer_id = Customer.next_id
            Customer.next_id += 1

        # validate & assign
        self._name = Validator.validate_name(name)
        self._address = Validator.validate_address(address)
        self._email = Validator.validate_email(email)
        self._phone = Validator.validate_phone(phone)
        self.__password = Validator.validate_password(password)  # private

    # --- properties with re-validation ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = Validator.validate_name(value)

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        self._address = Validator.validate_address(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = Validator.validate_email(value)

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = Validator.validate_phone(value)

    # password: store privately; expose only masked
    def get_password_masked(self) -> str:
        return "*" * len(self.__password)

    def set_password(self, value: str) -> None:
        self.__password = Validator.validate_password(value)

    def __str__(self) -> str:
        return (
            f"Customer(ID: {self.customer_id}, Name: {self.name}, "
            f"Email: {self.email}, Phone: {self.phone}, "
            f"Password: {self.get_password_masked()})"
        )
