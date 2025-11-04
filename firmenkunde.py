from kunde import Kunde
from validator import Validator

class Firmenkunde(Kunde):
    def __init__(self, name, adresse, email, telefon, password, firmennummer):
        super().__init__(name, adresse, email, telefon, password)
        self.firmennummer = Validator.f_validate_firmennummer(firmennummer)

    def get_firmennummer(self):
        return self.firmennummer
    def set_firmennummer(self, firmennummer):
        self.firmennummer = Validator.f_validate_firmennummer(firmennummer)

    def __str__(self):
        return (f"Firmenkunde (ID: {self.id}, Name: {self.name}, "
                f"Email: {self.email}, Telefon: {self.telefon}, "
                f"Firmennummer: {self.firmennummer})")
