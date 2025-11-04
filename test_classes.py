from pydantic import ValidationError
from kunde import Kunde
from privatkunde import Privatkunde
from firmenkunde import Firmenkunde

print ("test")
k1 = Kunde("Anna Schmidt", "Hauptstraße 5", "anna@mail.at", "+436601234567", "StrongPass1")
print (k1)
p1 = Privatkunde("Lena", "Ring 2", "lena@mail.at", "+43660111222", "Passwort9", "1990-05-20")
print (p1)
f1 = Firmenkunde ("ACME GmbH", "Industriestr. 10", "info@acme.at", "+43720123456", "Secret12", "123456789")
print (f1)

k2 = Kunde("Anna Schmidt", "Hauptstraße 5", "annamail.at", "+436601234567", "StrongPass1")
print (k2)
p2 = Privatkunde("Lena", "Ring 2", "lena@mail.at", "+43662222w0111222", "Passwort9", "1990-05-20")
print (p2)
f2 = Firmenkunde ("ACME GmbH", "Industriestr. 10", "info@acme.at", "+43720123456", "Secret12", "sdfd")
print (f2)