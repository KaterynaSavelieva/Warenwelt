from datetime import date
from kunde import Kunde
from validator import Validator

class Privatkunde(Kunde):
    def __init__(self, name, adresse, email, telefon, password, geburtsdatum):
        super().__init__(name, adresse, email, telefon, password)
        self.geburtsdatum = Validator.f_validate_geburtsdatum(geburtsdatum)

    def f_berechne_alter (self):
        today = date.today()
        y = today.year - self.geburtsdatum.year
        if (today.month, today.day) < (self.geburtsdatum.month, self.geburtsdatum.day):
            y -= 1
        return y

    # Getter / Setter з повторною валідацією
    def get_geburtsdatum(self):
        return self.geburtsdatum
    def set_geburtsdatum(self, geburtsdatum):
        self.geburtsdatum = Validator.f_validate_geburtsdatum(geburtsdatum)

    def __str__(self):
        return (f"Privatkunde (ID: {self.id}), Name: {self.name}, "
                f"Email: {self.email}, Telefon: {self.telefon}, "
                f"Alter: {self.f_berechne_alter()}), Password: {self.get_password()}")