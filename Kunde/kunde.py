from validator import Validator

class Kunde:
    next_id=10001

    def __init__(self, name,adresse, email, telefon, password):
        #generirien
        self.id = Kunde.next_id
        Kunde.next_id += 1

        # validieren
        self.name=Validator.f_validate_name(name)
        self.adresse=Validator.f_validate_adresse(adresse)
        self.email=Validator.f_validate_email(email)
        self.telefon=Validator.f_validate_telefon(telefon)
        self.__password=Validator.f_validate_password(password) #← privat


# Einfache Getter/Setter mit Revalidierung hinzufügen
    def get_name (self):
        return self.name
    def set_name (self, name):
        self.name= Validator.f_validate_name(name)

    def get_adresse (self):
        return self.adresse
    def set_adresse (self, adresse):
        self.adresse=Validator.f_validate_adresse(adresse)

    def get_email (self):
        return self.email
    def set_email (self, email):
        self.email=Validator.f_validate_email(email)

    def get_telefon (self):
        return self.telefon
    def set_telefon (self, telefon):
        self.telefon=Validator.f_validate_telefon(telefon)

    def get_password (self):
        return "*" * len(self.__password)
    def set_password (self, password):
        self.__password=Validator.f_validate_password(password)

    def __str__(self):
        return (f"Kunde (ID: {self.id}, Name: {self.name}, Email: {self.email}, Telefon: {self.telefon}), Password: {self.get_password()})")
