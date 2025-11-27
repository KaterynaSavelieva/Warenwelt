from typing import Optional
from .validator import Validator


class Customer:
    next_id = 1

    def __init__(
        self,
        name: str,
        address: Optional[str],
        email: str,
        phone: Optional[str],
        password: str,
        kind: str,
        customer_id: Optional[int] = None
    ):
        if customer_id is not None:
            self.customer_id = int(customer_id)
        else:
            self.customer_id = Customer.next_id
            Customer.next_id += 1

        self._name = Validator.validate_name(name)
        self._address = Validator.validate_address(address)
        self._email = Validator.validate_email(email)
        self._phone = Validator.validate_phone(phone) if phone else None
        self._kind = Validator.validate_kind(kind)
        self.__password = Validator.validate_password(password)

    # --- properties with re-validation ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = Validator.validate_name(value)

    @property
    def address(self) -> str | None:
        return self._address

    @address.setter
    def address(self, value: str | None) -> None:
        if value is None:
            self._address = None
        else:
            self._address = Validator.validate_address(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = Validator.validate_email(value)

    @property
    def phone(self) -> str | None:
        return self._phone

    @phone.setter
    def phone(self, value: str | None) -> None:
        if value is None:
            self._phone = None
        else:
            self._phone = Validator.validate_phone(value)

    @property
    def kind(self) -> str:
        return self._kind

    @kind.setter
    def kind(self, value: str) -> None:
        self._kind = Validator.validate_kind(value)

    # --- password handling ---
    def get_password_masked(self) -> str:
        return "*" * len(self.__password)

    def set_password(self, value: str) -> None:
        self.__password = Validator.validate_password(value)

    def get_password(self) -> str:
        """Повертає справжній пароль (тільки якщо потрібно для збереження в БД)."""
        return self.__password

    def __str__(self) -> str:
        return (
            f"Customer(ID: {self.customer_id}, Name: {self.name}, "
            f"Kind: {self.kind}, Email: {self.email}, Phone: {self.phone}, "
            f"Password: {self.get_password_masked()})"
        )
