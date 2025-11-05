from datetime import date
from pydantic import Field, EmailStr, constr, BaseModel, ValidationError, field_validator

#E-Mail-Adressen (gültiges Format)
#Telefonnummern (nur Zahlen, '+' erlaubt, 8-20 Stellen)
#Namen (nur Buchstaben, Leerzeichen und sinnvolle Sonderzeichen)
#Adressen (Buchstaben, Zahlen und sinnvolle Sonderzeichen
#Geburtsdatum (gültiges Format)
#Firmennummer (nur Zahlen, 5-15 Stellen)
class _Rules(BaseModel):
    email: EmailStr | None = None
    telefon: constr(pattern=r"^\+?\d{8,20}$") | None = None
    name: constr(pattern=r"^[A-Za-zÄÖÜäöüß' -]{2,55}$") | None = None
    adresse: constr(pattern=r"^[A-Za-zÄÖÜäöüß0-9 ,./'-]{2,55}$") | None = None
    geburtsdatum: date | None = None
    firmennummer: constr(pattern=r"^\d{5,15}$") | None = None
    password: str  | None = None
    #password: constr(pattern=r"^[A-Za-z0-9@#$%^&+=!?.]{8,50}$") | None = None


    @field_validator("password")
    @classmethod
    def check_password(cls, v: str | None):
        if v is None:
            return v
        problems = []
        if len(v) < 8:
            problems.append("mindestens 8 Zeichnen")
        if not any(c.isdigit() for c in v):
            problems.append("mindestens eine Ziffer")
        if not any(c.isalpha() for c in v):
            problems.append("mindestens ein Buchstabe")
        if problems:
            raise ValueError("Passwort: " + ", ".join(problems))
        return v


# Зовнішній валідатор з короткими повідомленням
class Validator:
    @staticmethod
    def _short_err(err: ValidationError, feld: str):
        msg = err.errors()[0].get("msg", str(err))
        # Людські повідомлення
        replacements = {
            "String should match pattern '^\\+?\\d{8,20}$'":
                "nur Zahlen erlaubt, '+' am Anfang möglich, 8–20 Ziffern",
            "value is not a valid email address":
                "ungültige E-Mail-Adresse (Format: name@domain.at)",
            "String should match pattern '^\\d{5,15}$'":
                "nur Ziffern erlaubt (5–15 Stellen)",
            "Input should be a valid date or datetime":
                "ungültiges Datum (Format: JJJJ-MM-TT)",
            "String should match pattern '^[A-Za-z0-9@#$%^&+=!?.]{8,50}$":
                "mindestens 8 Zeichnen, mindestens eine Ziffer, mindestens ein Buchstabe"
        }
        if msg in replacements:
            msg = replacements[msg]

        raise ValueError(f"{feld}: {msg}") from None

    @staticmethod
    def f_validate_email(v: EmailStr | str) -> str:
        try:
            obj = _Rules(email=v)
            return str(obj.email)
        except ValidationError as e:
            Validator._short_err(e, "E-Mail")

    @staticmethod
    def f_validate_telefon(v: str) -> str:
        try:
            _Rules(telefon=v)
            return v
        except ValidationError as e:
            Validator._short_err(e, "Telefon")

    @staticmethod
    def f_validate_name(v: str) -> str:
        try:
            _Rules(name=v)
            return v
        except ValidationError as e:
            Validator._short_err(e, "Name")

    @staticmethod
    def f_validate_adresse(v: str) -> str:
        try:
            _Rules(adresse=v)
            return v
        except ValidationError as e:
            Validator._short_err(e, "Adresse")

    @staticmethod
    def f_validate_geburtsdatum(v: date | str) -> date:
        try:
            obj = _Rules(geburtsdatum=v)  # pydantic сам парсить "YYYY-MM-DD"
            return obj.geburtsdatum
        except ValidationError as e:
            Validator._short_err(e, "Geburtsdatum")

    @staticmethod
    def f_validate_firmennummer(v: str) -> str:  # <-- str, не int
        try:
            _Rules(firmennummer=v)
            return v
        except ValidationError as e:
            Validator._short_err(e, "Firmennummer")

    @staticmethod
    def f_validate_password(v: str) -> str:
        try:
            _Rules(password=v)
            return v
        except ValidationError as e:
            Validator._short_err(e, "Passwort")


#Test Validierung
if __name__ == "__main__":
    print("Test validation...\n")

    for val in ["badmail", "kateryna@mailat", "kateryna@mail.at"]:
        try:
            print("OK (email):", Validator.f_validate_email(val))
        except Exception as e:
            print("Fehler (email):", e)

    for tel in ["123", "+436601234567"]:
        try:
            print("OK (telefon):", Validator.f_validate_telefon(tel))
        except Exception as e:
            print("Fehler (telefon):", e)

    for nr in ["12A45", "12345"]:
        try:
            print("OK (firmennummer):", Validator.f_validate_firmennummer(nr))
        except Exception as e:
            print("Fehler (firmennummer):", e)

    for pw in ["short", "password", "secret12", "123456789", "StrongPass1"]:
        try:
            print("OK (passwort):", "*" *len(Validator.f_validate_password(pw)))
        except Exception as e:
            print("Fehler (passwort):", e)
