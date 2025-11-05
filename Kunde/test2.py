from pydantic import ValidationError
from kunde import Kunde
from privatkunde import Privatkunde
from firmenkunde import Firmenkunde

def run_case(title, factory):
    try:
        obj = factory() # Пункт 1: спроба створити об’єкт.
        print(f"OK  [{title}]: {obj}")
    except ValidationError as e:
        print(f"ERR [{title}]: {e}")
    except Exception as e:
        print(f"ERR [{title}]: {e}")

run_case("Kunde (правильні дані)",
         lambda: Kunde("Anna Schmidt", "Hauptstraße 5", "anna@mail.at",
                       "+436601234567", "StrongPass1"))

run_case("Privatkunde (правильні дані)",
         lambda: Privatkunde("Lena", "Ring 2", "lena@mail.at",
                             "+43660111222", "Passwort9", "1990-05-20"))

run_case("Firmenkunde (правильні дані)",
         lambda: Firmenkunde("ACME GmbH", "Industriestr. 10", "info@acme.at",
                             "+43720123456", "Secret12", "123456789"))

run_case("Kunde (помилковий e-mail)",
         lambda: Kunde("Anna Schmidt", "Hauptstraße 5", "annamail.at",
                       "+436601234567", "StrongPass1"))

run_case("Privatkunde (помилковий телефон)",
         lambda: Privatkunde("Lena", "Ring 2", "lena@mail.at",
                             "+43662222w0111222", "Passwort9", "1990-05-20"))

run_case("Firmenkunde (помилковий firmennummer)",
         lambda: Firmenkunde("ACME GmbH", "Industriestr. 10", "info@acme.at",
                             "+43720123456", "Seret12", "sdfd"))