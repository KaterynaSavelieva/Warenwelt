from datetime import date
from pydantic import Field, EmailStr, constr, BaseModel, ValidationError

#E-Mail-Adressen (gültiges Format)
#Telefonnummern (nur Zahlen, '+' erlaubt, 8-20 Stellen)
#Namen (nur Buchstaben, Leerzeichen und sinnvolle Sonderzeichen)
#Adressen (Buchstaben, Zahlen und sinnvolle Sonderzeichen
#Geburtsdatum (gültiges Format)
#Firmennummer (nur Zahlen, 5-15 Stellen)
class _Rules(BaseModel):
    email: EmailStr | None = None
    telefon: constr(pattern=r"^\+?\d{8,20}$")| None = None
    name: str | None = Field(default=None, max_length=55)
    adresse: str | None = Field(default=None, max_length=55)
    geburtsdatum: date| None = None
    firmennummer: constr(pattern=r"^\d{5,15}$") | None = None

class Validator:
    # @staticmethod
    # def f_validate_email(v: EmailStr | str) -> str:
    #     try:
    #         obj = _Rules(email=v)
    #         return str(obj.email)
    #     except ValidationError as err:
    #         msg = err.errors()[0].get("msg", str(err))
    #         raise ValueError(msg) from None
    #

    @staticmethod
    def f_validate_email(v: EmailStr | str) -> str:
        try:
            _Rules(email=v)
        except ValidationError as err:
            raise err
        return v

    @staticmethod
    def f_validate_telefon(v: str) -> str:
        try:
            _Rules(telefon=v)
        except ValidationError as err:
            raise err
        return v

    @staticmethod
    def f_validate_name(v: str) -> str:
        try:
            _Rules(name=v)
        except ValidationError as err:
            raise err
        return v

    @staticmethod
    def f_validate_adresse (v: str) -> str:
        try:
            _Rules(adresse=v)
        except ValidationError as err:
            raise err
        return v

    @staticmethod
    def f_validate_geburtsdatum(v:date) -> date:
        try:
            obj = _Rules(geburtsdatum=v)
            return obj.geburtsdatum
        except ValidationError as err:
            raise err


    @staticmethod
    def f_validate_firmennummer(v: int) -> int:
        try:
            _Rules(firmennummer=v)
        except ValidationError as err:
            raise err
        return v

    @staticmethod
    def f_validate_password(v: str) -> str:
        if len(v) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(c.isdigit() for c in v):
            raise ValidationError("Password must contain at least one digit")
        if not any(c.isdigit() for c in v):
            raise ValidationError("Password must contain at least one digit")
        return v




#Test Validierung
if __name__ == "__main__":
    print("Test validation...\n")

    # e-mail
    for val in ["badmail", "kateryna@mailat", "kateryna@mail.at"]:
        try:
            out = Validator.f_validate_email(val)
            print("OK (email):", out, "\n")
        except ValidationError as e:
            print("Fehle:", val, e, "\n")

    # телефон
    for tel in ["123", "+436601234567"]:
        try:
            out = Validator.f_validate_telefon(tel)
            print("OK (telefon):", out)
        except ValidationError as e:
            print("Fehler (telefon): ", tel, e, "\n")

    # фірмовий номер
    for nr in ["12A45", "12345"]:
        try:
            out = Validator.f_validate_firmennummer(nr)
            print("OK (firmennummer):", out)
        except ValidationError as e:
            print("Fehler?(firmennummer): ", nr, e, "\n")
