from datetime import date
from pydantic import EmailStr, constr, BaseModel, ValidationError, field_validator
from typing import Optional, Literal  # 🔸 додано Literal

# Internal Pydantic model with all rules (types + regex)
class _Rules(BaseModel):
    email: EmailStr | None = None
    phone: constr(pattern=r"^\+?\d{8,20}$") | None = None
    name: constr(pattern=r"^[A-Za-zÄÖÜäöüß' -]{2,55}$") | None = None
    address: constr(pattern=r"^[A-Za-zÄÖÜäöüß0-9 ,./'-]{2,55}$") | None = None
    birthdate: date | None = None
    company_number: constr(pattern=r"^\d{5,15}$") | None = None
    password: Optional[str] = None
    kind: Literal["private", "company"] | None = None  # 🔸 додано

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str | None):
        """Simple password policy: >=8 chars, at least 1 digit and 1 letter."""
        if v is None:
            return v
        problems = []
        if len(v) < 8:
            problems.append("at least 8 characters")
        if not any(c.isdigit() for c in v):
            problems.append("at least one digit")
        if not any(c.isalpha() for c in v):
            problems.append("at least one letter")
        if problems:
            raise ValueError("Password: " + ", ".join(problems))
        return v


class Validator:
    """Thin wrapper around _Rules with short, user-friendly error messages."""

    @staticmethod
    def f_short_err(err: ValidationError, field_label: str):
        msg = err.errors()[0].get("msg", str(err))
        replacements = {
            "String should match pattern '^\\+?\\d{8,20}$'":
                "digits only, optional leading '+', length 8–20",
            "String should match pattern '^[A-Za-zÄÖÜäöüß' -]{2,55}$'":
                "letters only (A–Z, a–z, ä, ö, ü, ß), spaces, apostrophe or hyphen; length 2–55",
            "value is not a valid email address":
                "invalid email address (format: name@domain.com)",
            "String should match pattern '^\\d{5,15}$'":
                "digits only (length 5–15)",
            "Input should be a valid date or datetime, input is too short":
                "invalid date (format: YYYY-MM-DD)",
            "Input should be a valid date or datetime":
                "invalid date (format: YYYY-MM-DD)",
            "String should match pattern '^[A-Za-z0-9@#$%^&+=!?.]{8,50}$'":
                "8–50 characters, letters/digits/safe symbols (@#$%^&+=!?.)",
            "Input should be 'private' or 'company'":
                "must be 'private' or 'company'",
        }
        msg = replacements.get(msg, msg)
        raise ValueError(f"{field_label}: {msg}") from None


    @staticmethod
    def validate_email(v: EmailStr | str) -> str:
        try:
            obj = _Rules(email=v)
            return str(obj.email)
        except ValidationError as e:
            Validator.f_short_err(e, "Email")

    @staticmethod
    def validate_phone(v: str) -> str:
        try:
            _Rules(phone=v)
            return v
        except ValidationError as e:
            Validator.f_short_err(e, "Phone")

    @staticmethod
    def validate_name(v: str) -> str:
        try:
            _Rules(name=v)
            return v
        except ValidationError as e:
            Validator.f_short_err(e, "Name")

    @staticmethod
    def validate_address(v: str) -> str:
        try:
            _Rules(address=v)
            return v
        except ValidationError as e:
            Validator.f_short_err(e, "Address")

    @staticmethod
    def validate_birthdate(v: date | str) -> date:
        try:
            obj = _Rules(birthdate=v)
            return obj.birthdate
        except ValidationError as e:
            Validator.f_short_err(e, "Birthdate")

    @staticmethod
    def validate_company_number(v: str) -> str:
        try:
            _Rules(company_number=v)
            return v
        except ValidationError as e:
            Validator.f_short_err(e, "Company number")

    @staticmethod
    def validate_password(v: str) -> str:
        try:
            _Rules(password=v)
            return v
        except ValidationError as e:
            Validator.f_short_err(e, "Password")

    @staticmethod
    def validate_kind(v: str) -> str:
        try:
            _Rules(kind=v)
            return v
        except ValidationError as e:
            Validator.f_short_err(e, "Kind")


# test
if __name__ == "__main__":
    print("Test validation...\n")

    for val in ["badmail", "kateryna@mailat", "kateryna@mail.at"]:
        try:
            print("OK (email):", Validator.validate_email(val))
        except Exception as e:
            print("Error (email):", e)

    for tel in ["123", "+436601234567"]:
        try:
            print("OK (phone):", Validator.validate_phone(tel))
        except Exception as e:
            print("Error (phone):", e)

    for nr in ["12A45", "12345"]:
        try:
            print("OK (company_number):", Validator.validate_company_number(nr))
        except Exception as e:
            print("Error (company_number):", e)

    for pw in ["short", "password", "secret12", "123456789", "StrongPass1"]:
        try:
            print("OK (password):", "*" * len(Validator.validate_password(pw)))
        except Exception as e:
            print("Error (password):", e)

    for k in ["privat", "private", "company"]:
        try:
            print("OK (kind):", Validator.validate_kind(k))
        except Exception as e:
            print("Error (kind):", e)
